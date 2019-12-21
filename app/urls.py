from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('topic/<int:pk>', views.boardTopic, name='topic'),
    path('newTopic/<int:pk>', views.newTopic, name='newTopic'),
    path('topics_posts/<int:pk>/<int:topic_pk>', views.topics_post, name='topics_posts'),
    path('post_reply/<int:pk>/<int:topic_pk>/', views.reply_topic, name='post_reply'),
    # path('new_post',views.NewPostView.as_view(), name='new_post')
    path('posts/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit', views.PostUpdateView.as_view(), name='edit_post')
]