from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, SigninForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import logout
from .models import User
from .tasks import send_activation_email
from .tokens import account_activation_token
from django.contrib import messages


@login_required(login_url='signin')
def user_profile(request):
    return render(request, 'profile.html')


@login_required(login_url='signin')
def logout_user(request):
    logout(request)
    return redirect('/')


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(user_profile)
            else:
                messages.error(request, "Email или пароль неправильный")
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активаци аккаунта'
            message = render_to_string('activate_account.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_activation_email.delay(mail_subject, message, to_email)

            messages.success(request,
                             "Спасибо за регистрацию, мы отправили вам письмо на почту для активации аккаунта!")
            logout(request)
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(user_profile)
    else:
        return HttpResponse('Activation link is invalid!')
