from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'article_slug', 'description', 'moderation', 'created_at', 'updated_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'body', 'created_at')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
