from . import views
from django.urls import path, re_path

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin', ),
    path('logout', views.logout_user, name='logout'),
    path('profile', views.user_profile, name='profile'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
]
