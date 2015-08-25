from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import timezone

from .forms import UserForm, TrainingUserForm

# Create your views here.

def index(request):
    return render(request, 'courses/index.html', {'user': request.user})

def login_user(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Using Django's Authentication System
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # the user is valid and active, log the user in
                # and send the user back to homepage
                login(request, user)
                return HttpResponseRedirect(reverse('courses:index'))
            else:
                return HttpResponse('Your account [%s] is disable!' %
                                    user.get_username())
        else:
            return HttpResponse('Invalid username or password!')

    else:
        return render_to_response('courses/login.html', {}, context)
    
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('courses:index'))

def signup_user(request):
    # Get the request's context
    context = RequestContext(request)

    # A boolean value for telling the template whether the
    # registration was successful.
    registered = False

    # If it's a HTTP POST, process form data
    if request.method == 'POST':
        # Gathering form data   
        user_form = UserForm(data=request.POST)
        training_form = TrainingUserForm(data=request.POST)

        if user_form.is_valid() and training_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Hash the password and update user object
            user.set_password(user.password)
            user.save()
            
            # Delays saving the model until ready to avoid integrity problems
            # by set commit=False
            training = training_form.save(commit=False)
            training.user = user
            
            # Save the TrainingUser model
            training.save()
            registered = True
        else:
            print(user_form.errors, training_form.errors)
            
    # Not a HTTP POST, so render our form using two ModelForm instances
    else:
        user_form = UserForm()
        training_form = TrainingUserForm()
    
    # Render the template depending on the context
    return render_to_response(
            'courses/register.html',
            {
                'user_form': user_form,
                'training_form': training_form,
                'register': registered
            },
            context)
            
