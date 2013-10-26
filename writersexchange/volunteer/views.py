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

def index(request):
    return render_to_response('volunteer/index.html')

def apply(request):
	form = ApplicationForm(request.POST)
	if form.is_valid():
		new_application = form.save()
		new_application.save()
		email = form.cleaned_data['email']
		volunteer = get_object_or_404(Volunteer, email=email)
                # Send email to NOTIFICATION_EMAIL about new applicant.
                # TODO: replace '' with message body
                # TODO: set EMAIL_BACKEND in settings file to the actual email backend
                # TODO: change 'from@example.com' to actual address to send from
                send_mail('Writer\'s Exchange Volunteer Application', '', 'from@example.com', [NOTIFICATION_EMAIL], fail_silently=False)
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

def register(request):
	uf = UserForm(request.POST, prefix='user')
	# upf = UserProfileForm(request.POST, prefix="userprofile")
	if uf.is_valid() and upf.is_valid():
		user = uf.save()
		user.save()
		# UserProfileForm = upf.save(commit=False)
		# userprofile.user = user
		# userprofile.save()
		return HttpResponseRedirect('index')
	else:
		uf = UserForm(prefix='user')
		# upf = UserProfileForm(prefix='userprofile')
	return render_to_response('volunteer/register.html',
								dict(userform=uf,
                                     context_instance=RequestContext(request)))


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


def login_redirect(request):
    return render_to_response('volunteer/login.html', {},
                              context_instance=RequestContext(request))

