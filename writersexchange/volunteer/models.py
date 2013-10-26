from django.db import models

# Create your models here.
class Volunteer(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=100, unique = True, primary_key=True)
	phone = models.IntegerField(default=0)
	address = models.CharField(max_length=500)
	city = models.CharField(max_length=50)
	province = models.CharField(max_length=20)
	isApproved = models.BooleanField(default=False)
	reference1name = models.CharField(max_length=200)
	reference1email = models.EmailField(max_length=200)
	reference1phone = models.CharField(max_length=10)
	reference2name = models.CharField(max_length=200)
	reference2email = models.EmailField(max_length=200)
	reference2phone = models.CharField(max_length = 10)
	experience = models.CharField(max_length=2500)
	availability = models.CharField(max_length=2500)

	def is_approved(self):
		return self.isApproved



