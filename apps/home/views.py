from django.shortcuts import render
from django.views.generic import ListView, DetailView

from apps.article.models import Article


class ArticleList(ListView):
    model = Article
    template_name = 'index.html'
    ordering = '-created_at'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(moderation=True).order_by('-created_at')
        return context

