# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from volunteer.models import Volunteer
from volunteer.forms import ApplicationForm, UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django import forms
from volunteer.management import *
from django.core.mail import send_mail
from volunteer.we_settings import NOTIFICATION_EMAIL

def index(request):
    return render_to_response('volunteer/index.html')

def apply(request):
  form = request.POST
  new_application = Volunteer(name=form.get('name'), email=form.get('email-address'), phone=form.get('phone-number'), address=form.get('street-address'), city=form.get('city'), province=form.get('province'), isApproved=False, \
    reference1name=form.get('ref1name'), reference1email=form.get('ref1email'), reference1phone=form.get('ref1phone'), \
    reference2name=form.get('ref2name'), reference2email=form.get('ref2email'), reference2phone=form.get('ref2phone'), \
    experience=form.get('id_experience'), availability=form.get('id_availability'))

  if (form):
    
    new_application.save()
    email = form.get('email')

    return HttpResponse("Success!")
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



