# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from volunteer.models import Volunteer
from volunteer.forms import ApplicationForm
from django import forms

def index(request):
	return render_to_response('volunteer/index.html')

def apply(request):
	form = ApplicationForm(request.POST)
	if form.is_valid():
		new_application = form.save()
		new_application.save()
		email = form.cleaned_data['email']
		volunteer = get_object_or_404(Volunteer, email==email)

		return HttpResponse("Thank you for applying, we will notify you through email when your application has been")
	else: 
	    return render_to_response('volunteer/apply.html',
                          {'application_form': form},
                          context_instance=RequestContext(request))

# def confirmation(request, email):
# 	match_volunteer = get_object_or_404(Volunteer, email==email)
# 	return render_to_response('volunteer/confirm.html',
# 							{'applicant':match_volunteer},
# 							context_instance=RequestContext(request))




