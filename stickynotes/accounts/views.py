# https://wsvincent.com/django-user-authentication-tutorial-signup/
# https://simpleisbetterthancomplex.com/series/2017/09/25/a-complete-beginners-guide-to-django-part-4.html
from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login

from.forms import RegisterForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        # does not display email field for some reason
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
