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
from django.core.context_processors import csrf
import datetime

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
@login_required
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


def volunteer_list(request):
	if admin_is_logged_in():
		volunteerList = Volunteer.objects.all()
		fieldNames = [x[0] for x in generate_field_list(volunteerList[0])]
		fieldValues = [[x[1] for x in generate_field_list(v)] for v in volunteerList]
		return render_to_response('volunteer/volunteerList.html',
                      {'header_list': fieldNames, 'data_table':fieldValues},
                      context_instance=RequestContext(request))
	else:
		return login_redirect(request)

def volunteer_info(request, id):
	if admin_is_logged_in():
		volunteer =  get_object_or_404(Volunteer, id=id)
    	values = {'name': volunteer.name, 'email': volunteer.email, 'phoneNum': volunteer.phone, 'address': volunteer.address, 
    	'refName1': volunteer.reference1name, 'refPhone1': volunteer.reference1phone, 'refName2': volunteer.reference2name, 
    	'refPhone2': volunteer.reference2email, 'selfIntro': volunteer.experience}
    	return render_to_response('volunteer/volInfo.html', values, 
    		context_instance=RequestContext(request))

def add_event(request):
    def err_with_csrf(msg):
        val_dict = {'err_msg':msg}
        val_dict.update(csrf(request))
        return val_dict

    if request.method != "POST":
        #Send client to event creation page
        if admin_is_logged_in():
            tup = {}
            tup.update(csrf(request))
            return render_to_response('volunteer/addEvents.html', tup, context_instance=RequestContext(request))
        else:
            return login_redirect(request)
    else:
        try:
            print request.POST
            print request.POST['month'][0]
            name = request.POST['name']
            month = int(request.POST['month'][0])
            day = int(request.POST['day'][0])
            year = int(request.POST['year'][0])
            startHour = int(request.POST['sHour'][0])
            startMinute = int(request.POST['sMinute'][0])
            endHour = int(request.POST['fHour'][0])
            endMinute = int(request.POST['fMinute'][0])
            day = datetime.date(year, month, day)
            startDay = datetime.time(startHour, startMinute)
            endDay = datetime.time(endHour, endMinute)
        except KeyError:
            return render_to_response('volunteer/addEvents.html', err_with_csrf('This error should not have happened: did you change addEvents.html or views.py?'), context_instance=RequestContext(request))
        except ValueError as ve:
            print ve
            return render_to_response('volunteer/addEvents.html', err_with_csrf('Something is formatted wrong: could not parse text fields.'), context_instance=RequestContext(request))
        evt = Event()
        evt.startTime = startDay
        evt.endTime = endDay
        evt.date = day
        programs = Program.objects.filter(name__exact=name)
        if len(programs) == 0:
            prog = Program()
            prog.name = name
            prog.save()
        else:
            prog = programs[0]
        evt.name = prog
        evt.save()
        success_info = {'success_msg':'Event created.'} 
        success_info.update(csrf(request))
        return render_to_response('volunteer/addEvents.html', success_info, context_instance=RequestContext(request))
