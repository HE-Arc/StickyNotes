# https://wsvincent.com/django-user-authentication-tutorial-signup/
# https://simpleisbetterthancomplex.com/series/2017/09/25/a-complete-beginners-guide-to-django-part-4.html
from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm

from.forms import RegisterForm

# Create your views here.

"""class Register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/register.html'"""

def register(request):
    if request.method == 'POST':
        # does not display email field for some reason
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
