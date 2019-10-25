from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^login/$',login,name="login"),
    url(r'^reg/$',reg,name='reg'),
    url(r'^music/$',music,name='music'),
    url(r"^sport/$",sport,name="sport"),
    url(r'^story/$',story,name='story'),
    url(r"^story_dir/$",story_dir,name='story_dir'),
    url(r"^story_dir/p(\d+)/$",story_dirp),
    url(r"^story_text/$",story_text),
    url(r"^photo/$",photo,name='photo'),
    url(r"^logout/$",logout,name='logout'),
    url(r"^publish/$",publish,name="publish"),
    url(r"^content/$",content,name="content"),
    url(r"^comment/$",comment,name="comment"),
    url(r"^reply/$",cmt_reply,name="reply"),
    url(r"^rreply/$",rpl_reply,name="rel_reply"),
    url(r'^',index,name='index'),
]

