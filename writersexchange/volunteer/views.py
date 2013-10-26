# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from volunteer.models import Volunteer
from volunteer.forms import ApplicationForm, UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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






