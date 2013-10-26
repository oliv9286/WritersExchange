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
		a = 1
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


