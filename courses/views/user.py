from django.views import generic
from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
        UserCreationForm,
        AuthenticationForm,
        UserChangeForm
        )
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator

from courses.models import TrainingUser
from courses.forms import TrainingUserCreationForm, TrainingUserProfileForm

#class UserSignup(generic.CreateView):
#    model = User
#    form_class = UserCreationForm
#    template_name = 'user/signup.html'
#    success_url = reverse_lazy('courses:index')
#
#    def get_context_data(self, **kwargs):
#        # Call the base implementation first to get a context
#        context = super(UserSignup, self).get_context_data(**kwargs)
#        return context
#
#    def form_valid(self, form):
#        return super(UserSignup, self).form_valid(form)


class UserSignup(generic.edit.CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('courses:index')
    template_name = 'user/signup.html'

    def get_context_data(self, **kwargs):
        # Callthe base implementation first to get the acontext
        context = super(UserSignup, self).get_context_data(**kwargs)
        context['traininguser_register_form'] = TrainingUserCreationForm()
        return context

    def form_valid(self, form):
        """
        If form is valid, save the associated model object
        """
        self.object = form.save()
        traininguser_form = TrainingUserCreationForm(data=self.request.POST)
        traininguser = traininguser_form.save(commit=False)
        traininguser.user = self.object
        traininguser.save()

        return HttpResponseRedirect(self.get_success_url())


def login_user(request):
    # If it's a HTTP POST, process form data
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])
            # Valid username or password
            if user is not None:
                if user.is_active:
                    # The user is valid and active, log the user in
                    # and send the user back to homepage
                    login(request, user)
                    return HttpResponseRedirect(reverse('courses:index'))

                else:
                    return HttpResponse('Your account [%s] is disable!' %
                                        user.get_username())
            # Invalid username or password
            else:
                return HttpResponse('Invalid username or password!')

        else:
            HttpResponse(login_form.errors)
    # Not a HTTP POST, render the Login Form
    else:
        login_form = AuthenticationForm()

    return render(request, 'user/login.html',
                {'login_form': login_form})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('courses:index'))


class UserProfileView(UpdateView):
    model = User
    template_name = 'user/profile.html'
    fields = ['username', 'email', 'first_name',
            'last_name']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Callthe base implementation first to get the acontext
        context = super(UserProfileView, self).get_context_data(**kwargs)

        context['traininguser_profile_form'] = TrainingUserProfileForm(
                                                 instance=self.object.traininguser)
        return context

    def form_valid(self, form):
        """
        Update associated model and redirect to the success_url
        """
        self.object = form.save()
        training_form = TrainingUserProfileForm(self.request.POST,
                                            instance=self.object.traininguser)
        try:
            training_form.save()
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        except ValueError:
            print(training_form.errors)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('courses:profile',
                            kwargs={'pk': self.request.user.id})
