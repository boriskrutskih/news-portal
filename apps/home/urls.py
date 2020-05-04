from django.urls import path

from apps.home.views import ArticleList

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
]
