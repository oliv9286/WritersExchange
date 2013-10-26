# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from volunteer.models import Volunteer
from volunteer.forms import ApplicationForm
from django import forms
from django.core.mail import send_mail

def index(request):
	return render_to_response('volunteer/index.html')

def apply(request):
	form = ApplicationForm(request.POST)
	if form.is_valid():
		new_application = form.save()
		new_application.save()
		email = form.cleaned_data['email']
		volunteer = get_object_or_404(Volunteer, email=email)
                # Send email to Stacy to inform her of new applicant
                # TODO: replace '' with message body
                # TODO: set EMAIL_BACKEND in settings file to the actual email backend
                # TODO: change 'from@example.com' to actual address to send from
                # TODO: change 'stacey@mailinator.com' to Stacey's email
                send_mail('New Volunteer Application', '', 'from@example.com', ['stacey@mailinator.com'], fail_silently=False)
		return HttpResponse("Thank you for applying, we will notify you through email when your application has been reviewed.")
	else: 
	    return render_to_response('volunteer/apply.html',
                          {'application_form': form},
                          context_instance=RequestContext(request))
# def confirmation(request, email):
# 	match_volunteer = get_object_or_404(Volunteer, email==email)
# 	return render_to_response('volunteer/confirm.html',
# 							{'applicant':match_volunteer},
# 							context_instance=RequestContext(request))

#UNTESTED
 def get_all_programs(request):
	programs = Program.object.all().values('name').orderby('name')
	return render_to_response('volunteer/filterEvents.html')
							{'programs':programs}
#UNTESTED							
 def get_events_on_day(request):
	events = Program.object.filter(request['submitDay']).aggregate(date.weekday())
	return render_to_response('volunteer/selectEvents.html')
							{'programs':events}
	




