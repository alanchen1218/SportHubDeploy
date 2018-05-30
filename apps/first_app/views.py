from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
import bcrypt
import json
import pprint
import requests
from .models import *
from django.template.defaulttags import register
from django.http import JsonResponse

  # the index function is called when root is visited
def index(request):
  return render(request, 'first_app/index.html')

def registration(request):
  errors = User.objects.nameValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
      request.session['first_name'] = request.POST['first_name']
      request.session['last_name'] = request.POST['last_name']
      request.session['email'] = request.POST['email']
      return redirect('/')
  else:
    pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    currentuser = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pwhash)

    request.session['first_name'] = request.POST['first_name']
    request.session['last_name'] = request.POST['last_name']
    request.session['id'] = currentuser.id
  
    return redirect('/success')

def login(request):
  errors = User.objects.loginValidator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/')
  else:

    currentuser = User.objects.get(email=request.POST['email'])

    request.session['first_name'] = currentuser.first_name
    request.session['last_name'] = currentuser.last_name
    request.session['id'] = currentuser.id
    return redirect('/success')
  

def success(request):

  return render(request, 'first_app/success.html')


def userprofile(request, userid):
  thisUser = User.objects.get(id=userid)
  context = {
    'user' : thisUser,
    'comments' : thisUser.comments.all()
  }

  return render(request, 'first_app/profile.html', context)

def follow(request, userid):
  if userid == request.session['id']:
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  

def nbaindex(request):
  request.session['currentsport'] = 'NBA'
  # The 'requests' library makes a get request to the API (the URL). You can 
  # also add parameters such as API keys. (The sport APIs that you are consuming 
  # are most likely going to be read-only, which means you can only 'get' their 
  # data. You cannot edit or delete their data.)
  # Helpful link: https://www.dataquest.io/blog/python-api-tutorial/
  # Original API URL with apikey: http://api.sportradar.us/nba/trial/v4/en/league/2018/04/01/changes.json?api_key=mq6dyvpqskzcadjg2rcp6u99
  
  # teams = ["583ecda6-fb46-11e1-82cb-f4ce4684ea4c","583ec825-fb46-11e1-82cb-f4ce4684ea4c"]
  #   for x in teams:
  #   response = requests.get("http://api.sportradar.us/nba/trial/v4/en/teams/{}/profile.json".format(x), params=headers)
  #   data = response.json()  # 'data' is a dictionary
  #   print("team:")
  #   pp = pprint.PrettyPrinter(indent=4)
  #   pp.pprint(data)

  headers = {'api_key': 'mq6dyvpqskzcadjg2rcp6u99'}
  response = requests.get("http://api.sportradar.us/nba/trial/v4/en/teams/583ec825-fb46-11e1-82cb-f4ce4684ea4c/profile.json", params=headers)
  data = response.json()

  player_names = []
  for players in data['players']:
    player_names.append(players['full_name'])

  # print(player_names)

  context = {
    'forums' : Forum.objects.all(),
    'players' : player_names,
    'name' : data['name']  
  }
  
  ### VIEW INDENTED DATA. Use 'data' to perform any operations on dataset ###
  # pp = pprint.PrettyPrinter(indent=4)
  # pp.pprint(data)

  return render(request, 'first_app/nbaindex.html', context)




def nbaforumcreate(request):
  
  return render(request, 'first_app/nbacreate.html')



def nbaprocess(request):
  if request.method =='POST':

    newnbaforum = Forum.objects.create(title = request.POST['discussion_name'], description = request.POST['discussion_desc'], created_by = User.objects.get(id= request.session['id']), related_sport = "NBA")

    return redirect('/nba')



def shownbaforum(request, id):
  
  request.session['forumid'] = id

  context = {
    'forum' : Forum.objects.get(id=id),
    'forum_comments' : Comment.objects.all()
  }
  return render(request, 'first_app/nbaforum.html', context)

def nba_comment_render(request):

  if request.method =='POST':

    Comment.objects.create(content = request.POST['forum_comment'], commented_by = User.objects.get(id=request.session['id']), commented_on = Forum.objects.get(id = request.session['forumid']))
  
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def nflindex(request):
  request.session['currentsport'] = 'NFL'
  headers = {'api_key': 'ckg35fd446kf6u83pjvvhdpd'}
  response = requests.get("http://api.sportradar.us/nfl-ot1/teams/f0e724b0-4cbf-495a-be47-013907608da9/profile.json?api_key=ckg35fd446kf6u83pjvvhdpd", params=headers)
  data = response.json()

  player_names = []
  for players in data['players']:
    player_names.append(players['name'])

  context = {
    'forums' : Forum.objects.all(),
    'players' : player_names,
    'name' : data['name']  
  }
  return render(request, 'first_app/nflindex.html', context)


def shownflforum(request, id):
  
  request.session['forumid'] = id

  context = {
    'forum' : Forum.objects.get(id=id),
    'forum_comments' : Comment.objects.all()
  }
  return render(request, 'first_app/nflforum.html', context)

def nflforumcreate(request):

  return render(request, 'first_app/nflcreate.html')

def nflprocess(request):
  if request.method =='POST':

    newnbaforum = Forum.objects.create(title = request.POST['discussion_name'], description = request.POST['discussion_desc'], created_by = User.objects.get(id= request.session['id']), related_sport = "NFL")

    return redirect('/nfl')


def nfl_comment_render(request):
  if request.method =='POST':

    Comment.objects.create(content = request.POST['forum_comment'], commented_by = User.objects.get(id=request.session['id']), commented_on = Forum.objects.get(id = request.session['forumid']))
  
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def mlbindex(request):
  request.session['currentsport'] = 'MLB'
  
  headers = {'api_key': '2mmcdj8876bpdacn9x8c8r79'}
  response = requests.get("http://api.sportradar.us/mlb/trial/v6.5/en/teams/a7723160-10b7-4277-a309-d8dd95a8ae65/profile.json?api_key=2mmcdj8876bpdacn9x8c8r79", params=headers)
  data = response.json()

  player_names = []
  for players in data['players']:
    player_names.append(players['full_name'])

  context = {
    'forums' : Forum.objects.all(),
    'players' : player_names,
    'name' : data['name']  
  }
  return render(request, 'first_app/mlbindex.html', context)

def showmlbforum(request, id):
  
  request.session['forumid'] = id

  context = {
    'forum' : Forum.objects.get(id=id),
    'forum_comments' : Comment.objects.all()
  }
  return render(request, 'first_app/mlbforum.html', context)

def mlbforumcreate(request):

  return render(request, 'first_app/mlbcreate.html')

def mlbprocess(request):
  if request.method =='POST':

    newnbaforum = Forum.objects.create(title = request.POST['discussion_name'], description = request.POST['discussion_desc'], created_by = User.objects.get(id= request.session['id']), related_sport = "MLB")

    return redirect('/mlb')

def mlb_comment_render(request):
  if request.method =='POST':

    Comment.objects.create(content = request.POST['forum_comment'], commented_by = User.objects.get(id=request.session['id']), commented_on = Forum.objects.get(id = request.session['forumid']))
  
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




#DELETETING COMMENT

def deletecomment(request, id):

  Comment.objects.get(id=id).delete()

  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))








def about(request):
  return render(request, 'first_app/about.html')

def music(request):
  return render(request, 'first_app/music.html')

def returnprev(request):

  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





def api(request):

  forums = list(Forum.objects.all().values())

  return JsonResponse({"forums":forums})



def commentsapi(request):

  comments = list(Comment.objects.all().values())

  return JsonResponse({"comments":comments})


def usersapi(request):

  users = list(User.objects.all().values())

  return JsonResponse({"users":users})