from .views import *
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (PostDetail, PostSearch,)
from django.contrib.auth.views import LoginView, LogoutView
# from .views import IndexView

urlpatterns = [
    # path('', IndexView.as_view()),
    path('', cache_page(60)(Posts.as_view())),
    path('authors/', AuthorsPage.as_view()),
    path('post/<int:pk>/', cache_page(300)(PostDetail.as_view())),
    path('post2/', PostsList.as_view()),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
]
