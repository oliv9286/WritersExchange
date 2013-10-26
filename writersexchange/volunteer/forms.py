from django.forms import ModelForm
from volunteer.models import Volunteer

class ApplicationForm(ModelForm):
	class Meta:
		model = Volunteer
		fields = ['name' ,'email' ,'phone' ,'address' ,'city' ,'province' ,'reference1name' ,'reference1email' ,'reference1phone',\
		'reference2name' ,'reference2email' ,'reference2phone' ,'experience' ,'availability' ]