from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class TrainingUser(models.Model):
    # Automatically set this field to now
    # every time the object is saved or first created.
    date_updated = models.DateTimeField(auto_now=True)
    study_status = models.BooleanField(default=False)
    supervision = models.BooleanField(default=False)
    website = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    github = models.CharField(max_length=255, blank=True)

    # Connect with User, so we can reuse Django's Authentication System
    user = models.OneToOneField(User)
    
    # Using string 'Course' because class Course is NOT defined.
    courses = models.ManyToManyField('Course', through='UserCourse')
    subjects = models.ManyToManyField('Subject', through='UserSubject')
    tasks = models.ManyToManyField('Task', through='UserTask')

    def __str__(self):
        return self.user.get_full_name()


class Course(models.Model):
    name = models.TextField()
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_begin = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses:course-detail', kwargs={'pk': self.pk})


class Subject(models.Model):
    name = models.TextField()
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_begin = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.TextField()
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_begin = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True)
    subject = models.ForeignKey(Subject)

    def __str__(self):
        return self.name


class UserCourse(models.Model):
    date_joined = models.DateTimeField()
    student = models.ForeignKey(TrainingUser)
    course = models.ForeignKey(Course)


class UserSubject(models.Model):
    grade = models.FloatField()
    student = models.ForeignKey(TrainingUser)
    subject = models.ForeignKey(Subject)


class UserTask(models.Model):
    grade = models.FloatField()
    date_submitted = models.DateTimeField()
    student = models.ForeignKey(TrainingUser)
    task = models.ForeignKey(Task)
