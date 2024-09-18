from django import forms
from .models import TodoList, Task
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        if not re.search(r'[A-Za-z]', password1):
            raise ValidationError("Password must contain at least one letter (a-z or A-Z)")

        return password2

class ResPass(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['title']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'priority', 'completed', 'due']
        widgets = {'due': forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD (H:M)'}),
                   'name': forms.TextInput(attrs={'placeholder': 'Necessary'})}
