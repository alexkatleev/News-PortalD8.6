from celery import shared_task
import datetime
from django.conf import settings
from django.template.loader import render_to_string
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_email_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()
    title = post.title
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/news/{pk}',

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='alexander.katleev@yandex.ru',
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_notification():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dataCreations__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за Неделю',
        body='',
        from_email='alexander.katleev@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()