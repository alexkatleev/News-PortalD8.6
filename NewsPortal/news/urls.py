from .views import *
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.conf import settings
from django.shortcuts import redirect
# Импортируем созданное нами представление
from .views import ( PostDetail, PostSearch,)
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', Posts.as_view()),
    path('authors/', AuthorsPage.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('post2/', PostsList.as_view()),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/',LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe')
]

