from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms

from courses.models import Course, Subject


class CourseList(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses_list'


class CourseCreate(CreateView):
    model = Course
    template_name = 'courses/course_create.html'
    #date_begin = forms.DateTimeField()
    #date_end = forms.DateTimeField(widget=forms.DateTimeInput)
    fields = '__all__'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CourseCreate, self).dispatch(*args, **kwargs)

class CourseDetail(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(CourseDetail, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the course's subjects
        context['subjects_list'] = self.get_object().subjects.all()
        return context


class CourseUpdate(UpdateView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/course_update.html'
    fields = '__all__'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CourseUpdate, self).dispatch(*args, **kwargs)
