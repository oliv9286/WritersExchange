from django.forms import ModelForm, Form
from django import forms
from volunteer.models import Volunteer
from django.contrib.auth.models import User


class ApplicationForm(ModelForm):
	class Meta:
		model = Volunteer
		fields = ['name' ,'email' ,'phone' ,'address' ,'city' ,'province' ,'reference1name' ,'reference1email' ,'reference1phone',\
		'reference2name' ,'reference2email' ,'reference2phone' ,'experience' ,'availability' ]

class UserForm(forms.Form):
	username = forms.CharField(max_length=30, required=True)
	password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput())
	email = forms.EmailField(required=True)
	if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
	firstname = forms.CharField(max_length=20, required=True)
	lastname = forms.CharField(max_length=20, required=True)
