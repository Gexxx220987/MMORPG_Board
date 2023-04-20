from django.conf import settings
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'author', 'created_at')
    list_filter = ('author', 'category')
    search_fields = ('title', 'text')


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'post', 'author', 'status', 'created_at')
    list_filter = ('author', 'post')
    search_fields = ('text',)
    list_editable = ('text', 'post', 'author', 'status')


def send_news_email(modeladmin, request, queryset): # request — инфо о запросе; queryset — объекты, выделенные галочками
    if queryset:
        queryset = queryset.order_by('pk')

        html_content = render_to_string(
            'board/news_send_email.html',
            {
                'request': request,
                'news_list': queryset,
            }
        )

        for user in User.objects.all():
            if user.email:
                msg = EmailMultiAlternatives(
                    subject='Новости от "Доска Объявлений"',
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()


send_news_email.short_description = 'Разослать новости'


class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'author', 'created_at')
    list_filter = ('author',)
    search_fields = ('title', 'content')
    list_editable = ('title', 'content', 'author')
    actions = [send_news_email]


admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Category)