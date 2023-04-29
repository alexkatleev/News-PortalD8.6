from datetime import datetime
from django.db.models import Sum
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.cache import cache

world = 'WD'
politic = 'PL'
business = 'BS'
health = 'HL'
culture = 'CL'
society = 'SC'
accidents = 'AC'
sport = 'SP'
it = 'IT'
science = 'SN'
economy = 'EC'

OPTIONS_CATEGORY = [
    (world, 'Мир'),
    (politic, 'Политика'),
    (business, 'Бизнес'),
    (health, 'Здоровье'),
    (culture, 'Культура'),
    (society, 'Общество'),
    (accidents, 'Проишествия'),
    (sport, 'Спорт'),
    (it, 'ИТ'),
    (science, 'Наука'),
    (economy, 'Экономика')]

article = 'AR'
news = 'NW'

OPTIONS_POST = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Author(models.Model):
    """
    Модель Author
    имеет следующие поля:
    -<portalUser> связь «один к одному» с встроенной моделью пользователей User;
    - <ratingAuthor> рейтинг пользователя.
    """
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        """
        - update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого метода.
        Он состоит из следующего:
        -суммарный рейтинг каждой статьи автора умножается на 3;
        -суммарный рейтинг всех комментариев автора;
        -суммарный рейтинг всех комментариев к статьям автора.
        """

        postR = self.post_set.all().aggregate(postRating=Sum('rating'))
        p_R = 0
        p_R += postR.get('postRating')

        commentR = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        c_R = 0
        c_R += commentR.get('commentRating')

        self.ratingAuthor = p_R * 3 + c_R
        self.save()

    def __str__(self):
        return f"{self.authorUser}"


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, default=0)
    categoryType = models.CharField(max_length=2, choices=OPTIONS_POST, default=article)
    dataCreations = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def get_absolute_url(self):
        return f'/news/{self, id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        """
        - preview() модели Post, который возвращает начало статьи
        (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
        """
        return self.text[0:128] + '...'

    def __str__(self):
        dataf = 'Post from {}'.format(self.dataCreations.strftime('%d.%m.%Y %H:%M'))
        return f"{dataf},{self.author},{self.title}"

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/post/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    """
    Модель PostCategory
    Промежуточная модель для связи «многие ко многим»:
    - <postThrough>     связь «один ко многим» с моделью Post;
    - <categoryThrough> связь «один ко многим» с моделью Category.
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.category.title()


class Comment(models.Model):
    """
    Модель Comment
    Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
    Модель будет иметь следующие поля:
    - <commentPost>  связь «один ко многим» с моделью Post;
    - <userPost>     связь «один ко многим» со встроенной моделью User
                    (комментарии может оставить любой пользователь, необязательно автор);
    - <text>         текст комментария;
    - <dataCreation> дата и время создания комментария;
    - <rating>       рейтинг комментария.
    """
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    userPost = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        """
        - like()    который увеличивает рейтинг на единицу.
        """
        self.rating += 1
        self.save()

    def dislike(self):
        """
        - dislike() который уменьшают рейтинг на единицу.
        """
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.dataCreation}, {self.userPost}"


class Post2(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    view = models.CharField(max_length=2, choices=OPTIONS_POST, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    text = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return f'{self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'
