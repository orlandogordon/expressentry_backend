from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from .models import Submission, User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'avatar', 'bio', 'twitter', 'linkedin', 'github', 'website' ]

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['demo', 'details']
        widgets = {
            "details": Textarea(attrs={"cols": 40, "rows": 5}),
        }

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']