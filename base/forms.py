from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Issue

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'password1', 'password2']


class IssueCreationForm(ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'
        exclude = ['status', 'participants']

class IssueUpdateForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['name', 'description', 'assignee', 'status']

