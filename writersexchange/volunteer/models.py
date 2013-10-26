from django.db import models

# Create your models here.
class Volunteers(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	phone = models.IntegerField(default=0)
	address = models.CharField(max_length=500)
	city = models.CharField(max_length=50)
	province = models.CharField(max_length=20)
	isApproved = models.BooleanField()
	reference1name = models.CharField(max_length=200)
	reference1email = models.CharField(max_length=200)
	reference1phone = models.IntegerField(default=0)
	reference2name = models.CharField(max_length=200)
	reference2email = models.CharField(max_length=200)
	reference2phone = models.CharField(default=0)
	experience = models.CharField(max_length=2500)
	availability = models.CharField(max_length=2500)