# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from volunteer.models import Volunteer, Event, Program
from volunteer.forms import ApplicationForm, UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django import forms
from volunteer.management import *
from django.core.mail import send_mail
from volunteer.we_settings import NOTIFICATION_EMAIL
import calendar
from volunteer.json_conversion import *
import datetime
import json

def index(request):
    return render_to_response('volunteer/index.html')

def apply(request):
	form = ApplicationForm(request.POST)
	if form.is_valid():
		new_application = form.save()
		new_application.save()
		email = form.cleaned_data['email']
		volunteer = get_object_or_404(Volunteer, email=email)
                # Send email about new applicant to NOTIFICATION_EMAIL
                # Get link to application for body of email
                # TODO: Change request.META['HTTP_HOST'] to a constant?
                domain = request.META['HTTP_HOST']
                link = domain + "/applications/" + str(volunteer.id) + "/"
                # Create message body with link to application
                message = "To view the application, go to: " + link
                # TODO: set EMAIL_BACKEND in settings file to the actual email backend
                # TODO: change 'from@example.com' to actual address to send from
                send_mail('Writer\'s Exchange Volunteer Application', message, 'from@example.com', [NOTIFICATION_EMAIL], fail_silently=False)
		return HttpResponse("Thank you for applying, we will notify you through email when your application has been reviewed.")
	else: 
	    return render_to_response('volunteer/apply.html',
                          {'application_form': form},
                          context_instance=RequestContext(request))
# generates a list of data

def query(request):

	volunteer = Volunteer.objects.all()

	return render_to_response('volunteer/searchContent.htm',
						   {'dataset' : volunteer}, 
						   context_instance=RequestContext(request))

def signinpage(request):

	return render_to_response('volunteer/login.html')


def signin(request):
	if request.method == POST:
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        if user.is_active:
	            login(request, user)
	            # Redirect to a success page.
	            return redirect("apply")
	        else:
	            # Return a 'disabled account' error message
	            return HttpResponse('disabled accout')
	    else:
	        # Return an 'invalid login' error message.
	        return HttpResponse('invalid login')


def application_review(request,name):
    if admin_is_logged_in():
        volunteer = get_object_or_404(Volunteer, name=name)
        fieldList = generate_field_list(volunteer)
        return render_to_response(
                         'volunteer/apply_review.html',
                         {'display_fields':fieldList,
                          'forward_url':
                          '/application_result/' + name},
                         context_instance=RequestContext(request))
    else:
        return login_redirect(request)

def application_result(request, name):
    if admin_is_logged_in():
       volunteer = get_object_or_404(Volunteer, name=name)
       try:
	 result = request.GET['result']
       except KeyError:
         raise Http404    #TODO display a failure page
       if result == 'Approve':
         approve_application(volunteer)
         return render_to_response('volunteer/volConfirm.html',
                                   {'result':True, 'name':volunteer.name}, 
                                   context_instance=RequestContext(request))
       else:
         reject_application(volunteer)
         return render_to_response('volunteer/volConfirm.html',
                                   {'result':False, 'name':volunteer.name}, 
                                   context_instance=RequestContext(request))
    else:
        return login_redirect(request)

def application_list(request):
    if admin_is_logged_in():
       needingReview = Volunteer.objects.filter(isApproved__exact=False)
       applicationList = map(name_email_tuple, needingReview)
       return render_to_response('volunteer/apply_review_list.html',
                          {'applicationTuples':applicationList},
                          context_instance=RequestContext(request))
    else:
       return login_redirect(request)

# def confirmation(request, email):
#     match_volunteer = get_object_or_404(Volunteer, email==email)
#     return render_to_response('volunteer/confirm.html',
#                             {'applicant':match_volunteer},
#                             context_instance=RequestContext(request))

def signup(request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("index"))
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(username=form.cleaned_data['username'], password = form.cleaned_data['password'], \
                	email=form.cleaned_data['email'])
                user.save()

                new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'], email=request.POST['email'])
                login(request, new_user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render_to_response('volunteer/register.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show them a blank registration form '''
                form = UserForm()
                context = {'form': form}
                return render_to_response('volunteer/register.html', context, context_instance=RequestContext(request))

def month_events(request, year, month):
    #for end of month filtering
    year = int(year)
    month = int(month)
    endDateOfMonth = calendar.monthrange(year, month)[1]
    startDay = datetime.date(year, month, 1)
    endDay = datetime.date(year, month, endDateOfMonth)
    events = Event.objects.filter(date__gte=startDay, date__lte=endDay)
    jsonMap = events_to_month_info(events)
    return HttpResponse(json.dumps(jsonMap), content_type="application/json")

def day_events(request, year, month, day):
    events = Event.objects.filter(date__year=year, date__month=month,
                                   date__day=day)
    jsonMap = events_to_day_info(events)
    return HttpResponse(json.dumps(jsonMap), content_type="application/json")

def event_signup(request):
    try:
        evtId = request.POST['id']
    except KeyError:
        return HttpResponse(status=400)
    except ValueError:
        return HttpResponse(status=400)
    evt = Event.objects.filter(id__exact=evtId)
    if request.user.is_authenticated():
        uid = request.session['user_id']
        volunteer = Volunteer.objects.filter(id__exact=uid)
        volunteer.events.add(evt)
        volunteer.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
