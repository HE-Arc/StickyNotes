# https://wsvincent.com/django-user-authentication-tutorial-signup/
# https://simpleisbetterthancomplex.com/series/2017/09/25/a-complete-beginners-guide-to-django-part-4.html
from django.shortcuts import render, redirect
from django.contrib.auth import login as authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages

from django.utils.decorators import method_decorator

from.forms import RegisterForm, EditProfileForm

# Create your views here.

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # does not display email field for some reason
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                authenticate(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
        else:
            form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    else:
        messages.info(request, 'You already have an account!')
        return redirect('home')

@login_required
def my_profile_page(request):
    user = {'user': request.user }
    return render(request, 'profiles/profile.html', {'profile_user': user})

"""@login_required
def profile_page(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'profile_user': user})"""

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
        return redirect('my_profile_page')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'profiles/edit_profile.html', args)
