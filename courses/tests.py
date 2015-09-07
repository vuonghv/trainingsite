import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from courses.models import Course


class CourseViewTests(TestCase):
    def test_index_view_with_no_courses(self):
        """
        If no courses exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('courses:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['courses_list'], [])
        self.assertContains(response, 'There is NO courses')

    def test_index_view_with_a_ended_course(self):
        """
        Courses finished should be not displayed
        """
        Course.objects.create(
                name='A random course',
                description='end in the past',
                date_end=(timezone.now() + datetime.timedelta(-2)))
        
        response = self.client.get(reverse('courses:index'))
        self.assertContains(response, 'There is NO courses')

    def test_index_view_with_a_not_end_course(self):
        """
        Courses that hasn't ended yet should be displayed
        """
        Course.objects.create(
                name='A random course',
                description='end in the past',
                date_end=(timezone.now() + datetime.timedelta(+3)))
        
        response = self.client.get(reverse('courses:index'))
        self.assertNotContains(response, 'There is NO courses')


class CourseDetailTests(TestCase):
    pass
