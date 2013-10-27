# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from volunteer.models import Volunteer, Event, Program
from volunteer.forms import ApplicationForm, UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from volunteer.management import *
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.auth.models import User
from volunteer.we_settings import NOTIFICATION_EMAIL
import calendar
from volunteer.json_conversion import *
import json
from django.core.context_processors import csrf
import datetime

def index(request):
    return render_to_response('volunteer/index.html')

@login_required
def apply(request):
  form = request.POST
  user = request.user
  new_application = Volunteer(name=user.first_name + " "+user.last_name, email=user.email, phone=form.get('phone-number'), address=form.get('street-address'), city=form.get('city'), province=form.get('province'), isApproved=False, \
    reference1name=form.get('ref1name'), reference1email=form.get('ref1email'), reference1phone=form.get('ref1phone'), \
    reference2name=form.get('ref2name'), reference2email=form.get('ref2email'), reference2phone=form.get('ref2phone'), \
    experience=form.get('id_experience'), availability=form.get('id_availability'))

  if (form):
    try:
      new_application.save()
    except IntegrityError, e:
      fail_msg = "Sorry, record shows that your previous application has not been proccessed, please be patient (:"
      return render_to_response('volunteer/apply.html', {'message': fail_msg})

    email = form.get('email')

    domain = request.META['HTTP_HOST']
    link = domain + "/applications/" + str(new_application.id) + "/"
    message = "To view the application, go to: " + link
    send_mail('Writer\'s Exchange Volunteer Application', message, 'from@example.com', [NOTIFICATION_EMAIL], fail_silently=False)

    success_msg = "Thank you for your application! We will notify you about your application status soon."
    return render_to_response('volunteer/apply.html', {'message': success_msg})
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

@permission_required("volunteer.admin")
def application_review(request,uid):
    if admin_is_logged_in():
        volunteer = get_object_or_404(Volunteer, id=uid)
        fieldList = generate_field_list(volunteer)
        return render_to_response(
                         'volunteer/apply_review.html',
                         {'display_fields':fieldList,
                          'forward_url':
                          '/application_result/' + str(uid)},
                         context_instance=RequestContext(request))
    else:
        return login_redirect(request)

@permission_required("volunteer.admin")
def application_result(request, uid):
    if admin_is_logged_in():
       volunteer = get_object_or_404(Volunteer, id=uid)
       try:
	 result = request.POST['result']
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

@login_required
def profile(request):
  user = request.user
  volunteer_profile = get_object_or_404(Volunteer, email=user.email)
  #if user's profile does not yet exist we should force them to direct to the application page

  if (not volunteer_profile):
    return redirect('apply')

  return render_to_response("volunteer/profile.html", {"profile":volunteer_profile},
                            context_instance=RequestContext(request))

@permission_required("volunteer.admin")
def application_list(request):
    if admin_is_logged_in():
       needingReview = Volunteer.objects.filter(isApproved__exact=False)
       applicationList = map(name_email_tuple, needingReview)
       return render_to_response('volunteer/apply_review_list.html',
                          {'applicationTuples':applicationList},
                          context_instance=RequestContext(request))
    else:
       return login_redirect(request)


def signup(request):

    if request.method == 'POST':
      try:
        form = UserForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password = form.cleaned_data['password'], \
              email=form.cleaned_data['email'], first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])
            
            user.save()

            new_user = authenticate(username=request.POST['username'],
                                password=request.POST['password'], email=request.POST['email'])
            login(request, new_user)
            return HttpResponseRedirect(reverse("apply"))
        else:
            return render_to_response('volunteer/register.html', {'form': form}, context_instance=RequestContext(request))
      except IntegrityError, e:
        return render_to_response("volunteer/register.html", {'form':UserForm(),
          "message":"this username has already been taken."})
    else:
            ''' user is not submitting the form, show them a blank registration form '''
            form = UserForm()
            context = {'form': form}
            return render_to_response('volunteer/register.html', context, context_instance=RequestContext(request))

@login_required
def month_events(request, year, month):
    year = int(year)
    month = int(month)
    endDateOfMonth = calendar.monthrange(year, month)[1]
    startDay = datetime.date(year, month, 1)
    endDay = datetime.date(year, month, endDateOfMonth)
    events = Event.objects.filter(date__gte=startDay, date__lte=endDay)
    jsonMap = events_to_month_info(events)
    return HttpResponse(json.dumps(jsonMap), content_type="application/json")

@login_required
def day_events(request, year, month, day):
    events = Event.objects.filter(date__year=year, date__month=month,
                                   date__day=day)
    jsonMap = events_to_day_info(events)
    return HttpResponse(json.dumps(jsonMap), content_type="application/json")

@login_required
def event_signup(request):
    try:
        evtId = request.POST['id']
    except KeyError:
        return HttpResponse(status=400)
    except ValueError:
        return HttpResponse(status=400)
    evt = Event.objects.filter(id__exact=evtId)
    if request.user.is_authenticated():
        volunteer = Volunteer.objects.filter(email__exact=request.user.email)
        volunteer.events.add(evt)
        volunteer.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@permission_required("volunteer.admin")
def volunteer_list(request):
	if admin_is_logged_in():
		volunteerList = Volunteer.objects.all()
		fieldNames = [x[0] for x in generate_field_list(volunteerList[0])]
		fieldValues = [[x[1] for x in generate_field_list(v)] for v in volunteerList]
		return render_to_response('volunteer/searchContent.htm',
                      {'dataset':volunteerList},
                      context_instance=RequestContext(request))
	else:
		return login_redirect(request)
@login_required
def volunteer_info(request, id):
	if admin_is_logged_in():
		volunteer =  get_object_or_404(Volunteer, id=id)
    	values = {'name': volunteer.name, 'email': volunteer.email, 'phoneNum': volunteer.phone, 'address': volunteer.address, 
    	'refName1': volunteer.reference1name, 'refPhone1': volunteer.reference1phone, 'refName2': volunteer.reference2name, 
    	'refPhone2': volunteer.reference2email, 'selfIntro': volunteer.experience}
    	return render_to_response('volunteer/volInfo.html', values, 
    		context_instance=RequestContext(request))

@login_required
def volunteer_info(request, id):
  if admin_is_logged_in():
    volunteer =  get_object_or_404(Volunteer, id=id)
    values = {'id':volunteer.id,'name': volunteer.name, 'email': volunteer.email, 'phoneNum': volunteer.phone, 'address': volunteer.address, 
    'refName1': volunteer.reference1name, 'refPhone1': volunteer.reference1phone, 'refName2': volunteer.reference2name, 
    'refPhone2': volunteer.reference2email, 'selfIntro': volunteer.experience, "adminView":True, "isApproved":volunteer.isApproved}
    return render_to_response('volunteer/volInfo.html', values, 
    	context_instance=RequestContext(request))
  else:
    volunteer = get_object_or_404(Volunteer, id=id)
    values["adminView":False]
    return render_to_response('volunteer/volInfo.html', values, 
      context_instance=RequestContext(request))

@permission_required("volunteer.admin")
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
            print request.POST['year']
            #read all values given in form
            name = request.POST['name']
            month = int(request.POST['month'])
            day = int(request.POST['day'])
            year = int(request.POST['year'])
            startHour = int(request.POST['sHour'])
            startMinute = int(request.POST['sMinute'])
            endHour = int(request.POST['fHour'])
            endMinute = int(request.POST['fMinute'])
            day = datetime.date(year, month, day)
            startDay = datetime.time(startHour, startMinute)
            endDay = datetime.time(endHour, endMinute)
        except KeyError:
            #something didn't exist in POST
            return render_to_response('volunteer/addEvents.html', err_with_csrf('This error should not have happened: did you change addEvents.html or views.py?'), context_instance=RequestContext(request))
        except ValueError as ve:
            return render_to_response('volunteer/addEvents.html', err_with_csrf('Something is formatted wrong: could not parse text fields.'), context_instance=RequestContext(request))
        evt = Event()
        evt.startTime = startDay
        evt.endTime = endDay
        evt.date = day
        evt.name = program_for_name(prog)
        evt.save()
        success_info = {'success_msg':'Event created.'} 
        success_info.update(csrf(request))
        return render_to_response('volunteer/addEvents.html', success_info, context_instance=RequestContext(request))

@login_required
def program_list(request):
    jsonMapList = map(program_to_json, Program.objects.all())
    return HttpResponse(json.dumps(jsonMapList), content_type="application/json")

@login_required
def add_event_endpoint(request):
    try:
	startHour = int(request.GET['startHour'])
	startMinute = int(request.GET['startMinute'])
	endHour = int(request.GET['endHour'])
	endMinute = int(request.GET['endMinute'])
        day = int(request.GET['day'])
        month = int(request.GET['month'])
        year = int(request.GET['year'])
        startTime = datetime.time(startHour, startMinute)
        endTime = datetime.time(endHour, endMinute)
        day = datetime.date(year, month, day)
    except ValueError:
	return HttpResponse("Value error: bad field value given", status=400)
    except KeyError:
	return HttpResponse("Key error: key not matched", status=400)
    if request.GET.get('programId') is None and request.GET.get('name') is None:
	return HttpResponse("No program given", status=400)
    elif request.GET.get('programId') is None:
        program = program_for_name(request.GET['name'])
    else:
	try:
	   program = Program.objects.get(id = id)
        except Program.DoesNotExist:
           return HttpResponse("Bad program id", status=400)
    evt = Event()
    evt.name = program
    evt.startTime = startTime
    evt.endTime = endTime
    evt.date = day
    evt.save()
    return HttpResponse(status=200)

@login_required
def program_events(request, programId):
    if request.method != "POST":
        program = get_object_or_404(Program, id=programId)
        evts = Event.objects.filter(name__exact=program)
        eventTuples = map(event_listitem_tuple, evts)
        return render_to_response("volunteer/program_event_list.html",
                       {'program_name':program.name, 'events':eventTuples},
                       context_instance=RequestContext(request))
    else:
        try:
            keys = request.POST.getlist('evt_id')
        except KeyError:
            return HttpResponse(status=400)
        volunteer = Volunteer.objects.get(email__exact=request.user.email)
        for k in keys:
            volunteer.events.add(Event.objects.get(id=k))
        return HttpResponse("Signed up for " + str(len(keys)) + " events")

@login_required
def event_info(request, evtId):
    event = get_object_or_404(Event, id=evtId)
    program = event.name
    volunteers = Volunteer.objects.filter(events__id__exact=evtId)

    evtTuple = event_listitem_tuple(event)   
 
    msgString = (program.name + " runs on " + evtTuple[1] + 
                " from " + evtTuple[2] + " until " + evtTuple[3] +
                " and has " + str(volunteers.count()) + " volunteers.")
    vTuples = map(name_email_id_tuple, volunteers)
    return render_to_response("volunteer/event_info.html",
                 {'message':msgString, 'volunteers':vTuples},
                 context_instance=RequestContext(request))

def logout_page(request):
    logout(request)
    return redirect('index')
