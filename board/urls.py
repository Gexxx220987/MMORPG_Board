from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('posts/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('posts/create/', PostCreate.as_view(), name='post_create'),
    path('profile/', Profile.as_view(), name='profile'),
    path('replies/', ReplyList.as_view(), name='replies'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail')
]
