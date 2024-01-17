from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from datetime import datetime


# Create your models here.


class Appointment(models.Model):
    date = models.DateField()
    client_name = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'


class Author_news(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self) -> object:
        return f'{self.authorUser}'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category_news(models.Model):
    name = models.CharField(max_length=256, unique=True)
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}'


class Post_news(models.Model):
    author = models.ForeignKey(Author_news, on_delete=models.CASCADE, verbose_name='Автор')
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    title = models.CharField(max_length=256, verbose_name='Наименование')
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.title} | {self.author}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


