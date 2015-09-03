from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms

from courses.models import Course, Subject


class SubjectList(ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects_list'


class SubjectDetail(DetailView):
    model = Subject
    context_object_name = 'subject'
    template_name = 'subjects/subject_detail.html'


class SubjectCreate(CreateView):
    model = Subject
    template_name = 'subjects/subject_create.html'
    fields = '__all__'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SubjectCreate, self).dispatch(*args, **kwargs)


class SubjectUpdate(UpdateView):
    model = Subject
    fields = '__all__'
    template_name = 'subjects/subject_update.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SubjectUpdate, self).dispatch(*args,**kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first
        context = super(SubjectUpdate, self).get_context_data(**kwargs)
        context['subject'] = self.object
        return context
