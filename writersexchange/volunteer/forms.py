from django.forms import ModelForm
from volunteer.models import Volunteer
from django.contrib.auth.models import User


class ApplicationForm(ModelForm):
	class Meta:
		model = Volunteer
		fields = ['name' ,'email' ,'phone' ,'address' ,'city' ,'province' ,'reference1name' ,'reference1email' ,'reference1phone',\
		'reference2name' ,'reference2email' ,'reference2phone' ,'experience' ,'availability' ]

class UserForm(ModelForm):
	class Meta:
		model = User