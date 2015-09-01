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

class UserSignup(generic.CreateView):
    model = User
    #fields = ['username', 'email', 'twitter']
    form_class = UserCreationForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('courses:index')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserSignup, self).get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        """
        training_user = TrainingUser.objects.create()
        training_user.save()
        form.instance.training_user = training_user
        """
        return super(UserSignup, self).form_valid(form)


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
    #form_class = UserChangeForm
    fields = ['username', 'email', 'first_name',
            'last_name', 'date_joined']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('courses:profile',
                            kwargs={'pk': self.request.user.id})
