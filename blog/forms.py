from django import forms
from .models import Post
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

class PostCreationForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'image', 'body', 'date_published']
		widgets = {
            "date_published": DateTimePickerInput()
        }