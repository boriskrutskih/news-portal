from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.views.generic import CreateView, DetailView
from .models import Article, Comment
from django.core import serializers
from django.http import JsonResponse
from .forms import ArticleForm, CommentForm
from .tasks import send_comment_notification


class ArticleCreateView(SuccessMessageMixin, CreateView):
    form_class = ArticleForm
    template_name = 'forms/article_create.html'
    success_url = '/article/create'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        success_message = 'Статья успешно добавлена! И появится после одобрения модератором'
        if self.request.user.is_superuser or self.request.user.is_staff:
            success_message = 'Статья успешно добавлена!'
        return success_message


class ArticleDetailView(DetailView):
    model = Article
    slug_field = 'article_slug'
    slug_url_kwarg = 'article_slug'
    template_name = 'article/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'article': self.object.pk})
        context['comments'] = Comment.objects.filter(article=self.object.pk).order_by('-created_at')

        return context


def post_comment(request):
    if request.is_ajax and request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [instance, ])

            mail_subject = 'У вас новый комментарий'
            message = render_to_string('new_comment_message.txt', {
                'article_title': instance.article.title,
                'article_url': instance.article.article_slug,
                'domain': get_current_site(request)
            })
            to_email = instance.article.author.email
            send_comment_notification.delay(mail_subject, message, to_email)

            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": "", }, status=400)
