from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Profile, Category, Plan, Task

# ===========================
# AUTH FORMS
# ===========================
class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use. Please use a different email.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))


# ===========================
# CATEGORY FORM
# ===========================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


# ===========================
# PLAN FORM
# ===========================
class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'plan_type', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


# ===========================
# TASK FORM
# ===========================
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['day_number', 'title', 'description', 'estimated_time', 'task_date']
        widgets = {
            'day_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'task_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


# ===========================
# PROFILE FORM
# ===========================
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'phone', 'address']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
