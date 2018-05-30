from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),   # This line has changed! Notice that urlpatterns is a list, the comma is in
    url(r'registration$', views.registration),
    url(r'login$', views.login),
    url(r'success$', views.success),


    url(r'mlb$', views.mlbindex),
    url(r'^mlb_forum/(?P<id>\d+)$', views.showmlbforum),
    url(r'^mlb_create_forum$', views.mlbforumcreate),
    url(r'^mlb_forum_process$', views.mlbprocess),
    url(r'^mlb_comment_render$', views.mlb_comment_render),



    url(r'nfl$', views.nflindex),
    url(r'^nfl_forum/(?P<id>\d+)$', views.shownflforum),
    url(r'^nfl_create_forum$', views.nflforumcreate),
    url(r'^nfl_forum_process$', views.nflprocess),
    url(r'^nfl_comment_render$', views.nfl_comment_render),


    url(r'nba$', views.nbaindex),
    url(r'^nba_create_forum$', views.nbaforumcreate),
    url(r'^nba_forum_process$', views.nbaprocess),
    url(r'^nba_forum/(?P<id>\d+)$', views.shownbaforum),
    url(r'^nba_comment_render$', views.nba_comment_render),


    url(r'^profiles/(?P<userid>\d+)$', views.userprofile),


    url(r'^followProcess/(?P<userid>\d+)$', views.follow),



    url(r'^delete/(?P<id>\d+)$', views.deletecomment),



    url(r'music$', views.music),


    url(r'about$', views.about),
    url(r'return_previous', views.returnprev),


    url(r'^api$', views.api),
    url(r'^commentsapi$', views.commentsapi),
    url(r'^usersapi$', views.usersapi)
]  