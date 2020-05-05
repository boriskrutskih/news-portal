from django.db import models

from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from easy_thumbnails.fields import ThumbnailerImageField
from apps.user.models import User


class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    article_slug = AutoSlugField(populate_from='title', allow_unicode=True, always_update=True, verbose_name='Ссылка')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    body = RichTextField(blank=True, null=False)
    image = models.FileField()
    moderation = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.author.is_superuser or self.author.is_staff:
            self.moderation = True
        super(Article, self).save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=1000)
    body = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.article} on {self.author}"

    class Meta:
        verbose_name_plural = 'Комментарии'
