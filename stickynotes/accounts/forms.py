from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    # avatar = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = (
        'username',
        'email',
        'password1',
        'password2',
        # 'avatar')
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        # user.avatar = self.cleaned_data['avatar']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'password'
            # 'avatar')
            )
