from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import timezone

from .forms import UserForm, TrainingUserForm
from .forms import UserProfileForm, TrainingUserProfileForm
from .models import Course, TrainingUser

# Create your views here.

def index(request):
    # Retrieve the top 5 only
    course_list = Course.objects.order_by('date_begin')[:5]
    context = {'courses': course_list}
    return render(request, 'courses/index.html', context)

def login_user(request):
    # Only process data when receive a POST request
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
        return render(request, 'courses/login.html')
    
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('courses:index'))

def signup_user(request):
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
    return render(request, 'courses/register.html',
                {
                    'user_form': user_form,
                    'training_form': training_form,
                    'register': registered
                })
            
@login_required
def profile(request):
    user = request.user
    training_user = user.traininguser

    # update user's data if user click update profile button
    if request.method == 'POST':
        user_form = UserProfileForm(data=request.POST,
                                    instance=user)
        training_form = TrainingUserProfileForm(data=request.POST,
                                            instance=training_user)
        
        if user_form.is_valid() and training_form.is_valid():
            user_form.save()
            training_form.save()

            # Why cannot update field 'date_update' by using following statement?
            #training_form.fields['date_updated'].widget.attrs['value'] = training_user.date_updated
            # So need to reload the page by HttpResponseRedirect
            return HttpResponseRedirect(reverse('courses:profile'))

    # if GET request or something else, show user's information
    else:
        user_form = UserProfileForm(initial={
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name})

        training_form = TrainingUserProfileForm(initial={
                        'study_status': training_user.study_status,
                        'website': training_user.website,
                        'facebook': training_user.facebook,
                        'twitter': training_user.twitter,
                        'github': training_user.github,
                        'date_updated': training_user.date_updated})

    training_form.fields['date_updated'].widget.attrs['readonly'] = True
    return render(request, 'courses/user_profile.html',
                {'user_form': user_form, 'training_form': training_form})
