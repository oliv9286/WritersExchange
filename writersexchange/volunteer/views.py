# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from volunteer.models import Volunteer
from django import forms

def index(request):
	return redirect('/apply')

def apply(request):

	return render(request, 'volunteer/apply.html')

def submit_application(request):
	if request.POST:
		v = Volunteer(request.POST.get('name'), request.POST.get('email'), phone=request.POST.get('phone'), address=request.POST.get('address'), \
		 city=request.POST.get('city'), province=request.POST.get('province'), isApproved=False, reference1name=request.POST.get('r1name'), \
		 reference1email=request.POST.get('r1email'), reference1phone=request.POST.get('r1phone'), reference2name=request.POST.get('r2name'), \
		 reference2email=request.POST.get('r2email'), reference2phone=request.POST.get('r2phone'))

		v.save()
		return HttpResponse("Success")

	return HttpResponse("Fail")




