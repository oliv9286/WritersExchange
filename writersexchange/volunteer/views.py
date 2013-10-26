# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from volunteer.models import Volunteer
from volunteer.forms import ApplicationForm
from django import forms
from volunteer.management import *
def index(request):
    return render_to_response('volunteer/index.html')

def apply(request):
    form = ApplicationForm(request.POST)
    if form.is_valid():
        new_application = form.save()
        new_application.save()
        email = form.cleaned_data['email']
        volunteer = get_object_or_404(Volunteer, email=email)

        return HttpResponse("Thank you for applying, we will notify you through email when your application has been")
    else: 
            return render_to_response('volunteer/apply.html',
                                                    {'application_form': form},
                                                    context_instance=RequestContext(request))

def application_review(request,name):
    if admin_is_logged_in():
        volunteer = get_object_or_404(Volunteer, name=name)
        fieldList = [("Name", volunteer.name), ("Email", volunteer.email), 
            ("Phone #", volunteer.phone), ("Address", volunteer.address), 
            ("City", volunteer.city), ("Province", volunteer.province), 
            ("Reference #1", volunteer.reference1name), 
            ("Reference #1 Email", volunteer.reference1email),
            ("Reference #1 Phone", volunteer.reference1phone),
            ("Reference #2", volunteer.reference2name),
            ("Reference #2 Email", volunteer.reference2email),
            ("Reference #2 Phone", volunteer.reference2phone),
            ("Experience", volunteer.experience),
            ("Availability", volunteer.availability)]
        return render_to_response(
                         'volunteer/apply_review.html',
                         {'display_fields':fieldList,
                          'forward_url':
                          '/application_result/' + name},
                         context_instance=RequestContext(request))
    else:
        login_redirect(request)
def application_result(request, name):
    if admin_is_logged_in():
       volunteer = get_object_or_404(Volunteer, name=name)
       try:
	 result = result.POST['result']
       except KeyError:
         raise Http404    #TODO display a failure page
       if result == 'Approve':
         approve_application(volunteer)
         return render_to_response('volunteer/apply_review_confirm.html',
                                   {'result':'approved'}, 
                                   context_instance=RequestContext(request))
       else:
         reject_application(volunteer)
         return render_to_response('volunteer/apply_review_confirm.html',
                                   {'result':'rejected'}, 
                                   context_instance=RequestContext(request))
    else:
        login_redirect(request)
# def confirmation(request, email):
#     match_volunteer = get_object_or_404(Volunteer, email==email)
#     return render_to_response('volunteer/confirm.html',
#                             {'applicant':match_volunteer},
#                             context_instance=RequestContext(request))


def login_redirect(request):
    return render_to_response('volunteer/login.html', {},
                              context_instance=RequestContext(request))

