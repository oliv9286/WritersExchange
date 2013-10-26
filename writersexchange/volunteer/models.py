from django.db import models

# Create your models here.
class Volunteer(models.Model):
        name = models.CharField(max_length=200, null=False)
        email = models.EmailField(max_length=100, unique = True, primary_key=True, null=False)
        phone = models.CharField(max_length=10, blank=False, null=False)
        address = models.CharField(max_length=500, null=False)
        city = models.CharField(max_length=50, null=False)
        province = models.CharField(max_length=20, null=False)
        isApproved = models.BooleanField(default=False, null=False, default=False)
        hasCrimCheck = models.BooleanField(default=False, null=False, default=False)
        hasTraining = models.BooleanField(default=False, null=False, default=False)
        reference1name = models.CharField(max_length=200, null=False)
        reference1email = models.EmailField(max_length=200, null=False)
        reference1phone = models.CharField(max_length=10, null=False)
        reference2name = models.CharField(max_length=200, null=False)
        reference2email = models.EmailField(max_length=200, null=False)
        reference2phone = models.CharField(max_length = 10, null=False)
        experience = models.CharField(max_length=2500, null=False)
        availability = models.CharField(max_length=2500, null=False)

        events = ManyToManyField(Event)

        def is_approved(self):
                return self.isApproved

        def hasCrimCheck(self):
                return self.hasCrimCheck

        def hasTraining(self):
                return self.hasTraining

class Event(models.Model):
        date = models.DateField(auto_now=False, auto_now_add=False null=False)
        startTime = models.TimeField(auto_now=False, auto_now_add=False, null=False)
        endTime = models.TimeField(auto_now=False, auto_now_add=False, null=False)
        name = models.CharField(max_length=200, null=False)

        program = models.ForeignKey(Program)

class Program(models.Model):
        name = models.CharField(max_length=200, null=False)