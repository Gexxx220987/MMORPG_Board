from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    category = models.ForeignKey(
        'Category',
        related_name='posts',
        verbose_name='Категория',
        on_delete=models.PROTECT,
        blank=False
    )
    author = models.ForeignKey(
        User,
        related_name='posts',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('board:post_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Reply(models.Model):
    STATUSES = [
        ('C', 'Создан'),
        ('A', 'Принят'),
        ('R', 'Отклонен'),
    ]

    text = models.CharField('Отклик', max_length=100)
    status = models.CharField(
        'Статус', max_length=1,
        choices=STATUSES, default='C'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reply',
        verbose_name='Объявление',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reply',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_at']

    def __str__(self):
        return self.text


class News(models.Model):
    title = models.CharField('Новость', max_length=100)
    content = RichTextUploadingField('Содержание')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('board:news_detail', kwargs={'pk': self.pk})
