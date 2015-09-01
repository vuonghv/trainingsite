from django.views import generic
from django.utils import timezone


from courses.models import Course


class IndexView(generic.ListView):
    """
    Using class-based view to display the index page
    """
    context_object_name = 'courses_list'
    template_name = 'courses/index.html'

    def get_queryset(self):
        """
        Retrieve all courses that have finished yet.
        """
        return Course.objects.filter(date_end__gt=timezone.now())
