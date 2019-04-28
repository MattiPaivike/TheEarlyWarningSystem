from django import forms
from .models import CustomUser, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from main_app.models import Software, Version
from django.core.mail import EmailMessage
from datetime import timezone, datetime, timedelta

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model =  CustomUser
        fields = ['email', 'password1', 'password2']

    #Override of save method for saving both User and Profile objects
    def save(self, datas):
        u = CustomUser.objects.create_user(datas['email'],
                                     datas['password1'])
        u.is_active = False
        u.save()
        profile=Profile()
        profile.user=u
        profile.activation_key=datas['activation_key']
        profile.key_expires=datetime.now(timezone.utc) + timedelta(days=2)
        profile.sent_keys=0
        profile.save()
        return u


apps = Version.objects.all()


class ProfileUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        User_name = CustomUser.objects.get(email=str(self.request.user))
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for app in apps:
            field_name = str(app.software)
            #if user has subscribed set checkbox to true
            if User_name.subscriptions_set.filter(app_subscriptions=str(app.software)).exists():
                self.fields[field_name] = forms.BooleanField(required=False, initial=True)
            else:
                self.fields[field_name] = forms.BooleanField(required=False)
