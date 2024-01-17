from django.contrib import admin
from .models import Appointment, Author_news, Category_news, Post_news
# Register your models here.
admin.site.register(Appointment)
admin.site.register(Author_news)
admin.site.register(Category_news)
admin.site.register(Post_news)
