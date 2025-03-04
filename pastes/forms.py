from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Paste

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class PasteForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 10,
                'class': 'form-control',
                'placeholder': 'Enter your paste content here...',
                'maxlength': 100000  # 100KB limit
            })
        }
