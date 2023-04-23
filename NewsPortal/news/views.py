
from django.views import View
from django.core.mail import send_mail
from datetime import datetime

from .models import Appointment
from  django.views.generic.base import View
from .models import *
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import PostForm
from .models import Post, PostCategory, Author,Category
from .filters import PostFilter
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render, reverse
from django.contrib.auth.decorators import login_required



class PostDetail(LoginRequiredMixin,View):
    def get(self, request, pk):
        ps = Post.objects.get(id=pk)
        return render(request, "news/posts.html", {'ps':ps})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# def news_page_list(request):
#     """ Представление для вывода страницы с новостями """
#     newslist = Post.objects.all().order_by('-rating')[:5]
#     return render(request, 'news/news.html', {'newslist': newslist})

class Posts(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    ordering = ['-rating']
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 5
    permission_required = ('news.add_post','news.change_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class AuthorsPage(LoginRequiredMixin, ListView):
    model = Author  # queryset = Author.objects.all()
    context_object_name = "Authors"
    template_name = 'news/authors.html'


class PostsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post2
    ordering = '-time_in'
    template_name = 'news/posts2.html'
    context_object_name = 'posts'
    paginate_by = 5
    permission_required = ('news.add_post','news.change_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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


class CategoryListView(Posts):
    models = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-rating')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы подписались на категорию: '
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'вы отписались от категории: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='alexander.katleev@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('appointments:make_appointment')