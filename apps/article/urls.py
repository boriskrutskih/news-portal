from django.urls import path
from .views import ArticleCreateView, ArticleDetailView, post_comment
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('article/create', login_required(ArticleCreateView.as_view(), login_url='signin'), name='article_create'),
    path('article/<slug:article_slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('comment/ajax/comment', post_comment, name='post_comment'),

]
