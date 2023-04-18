from django.http import HttpResponseNotFound
from django.shortcuts import render
from  django.views.generic.base import View
from .models import *
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, PostCategory, Author,Category
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Post, PostCategory, Author,Category

from .filters import PostFilter
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
# BaseRegisterForm
class AuthorsPage(LoginRequiredMixin, ListView):
    model = Author  # queryset = Author.objects.all()
    context_object_name = "Authors"
    template_name = 'news/authors.html'
    paginate_by = 2

class PostDetail(LoginRequiredMixin,View):
    def get(self, request, pk):
        ps = Post.objects.get(id=pk)
        return render(request, "news/posts.html", {'ps':ps})



def news_page_list(request):
    """ Представление для вывода страницы с новостями """

    newslist = Post.objects.all().order_by('-rating')[:5]
    return render(request, 'news/news.html', {'newslist': newslist})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class PostsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post2
    ordering = '-time_in'
    template_name = 'news/posts2.html'
    context_object_name = 'posts'
    paginate_by = 5
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# class PostDetail(DetailView):
#     model = Post2
#     template_name = 'post.html'
#     context_object_name = 'post'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = ('news.add_post','news.change_post')
    # // customizeformview
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/create/':
                post.view = 'NW'
            elif path_info == '/articles/create/':
                post.view = 'AR'
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    permission_required = ('news.add_post', 'news.change_post')
    success_url = 'edit/'
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте редактирования
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDelete(LoginRequiredMixin, DeleteView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'news/news.html'
# class BaseRegisterView(CreateView):
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'
# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'protect/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
#         return context