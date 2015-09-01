from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
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
