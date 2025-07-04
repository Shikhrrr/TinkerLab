from django import forms
from .models import StudentUser, BookingRequest, Item
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    SEMESTER_CHOICES = [(i, str(i)) for i in range(1, 9)]
    DEPT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('IT', 'Information Technology'),
        ('CHE', 'Chemical Engineering'),
        ('BT', 'Biotechnology'),
        ('MT', 'Metallurgy'),
        ('AE', 'Aerospace Engineering'),
        ('PIE', 'Production and Industrial Engineering'),
        ('OTHER', 'Other'),
    ]

    semester = forms.ChoiceField(choices=SEMESTER_CHOICES)
    department = forms.ChoiceField(choices=DEPT_CHOICES)

    class Meta:
        model = StudentUser
        fields = ['username', 'email', 'roll', 'semester', 'department', 'profile_image', 'password1', 'password2']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = StudentUser
        fields = ['profile_image', 'username', 'department']

class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['purpose', 'duration_days']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_id', 'title', 'description', 'quantity', 'available', 'image', 'location']
