from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TrainingUser(User):
    date_updated = models.DateTimeField()
    study_status = models.BooleanField()
    supervision = models.BooleanField()
    
    # Using string 'Course' because class Course is NOT defined.
    courses = models.ManyToManyField('Course', through='UserCourse')
    subjects = models.ManyToManyField('Subject', through='UserSubject')
    tasks = models.ManyToManyField('Task', through='UserTask')

    def __str__(self):
        return self.first_name + self.last_name


class Course(models.Model):
    name = models.TextField()
    description = models.TextField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.TextField()
    description = models.TextField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.TextField()
    description = models.TextField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_begin = models.DateTimeField()
    deadline = models.DateTimeField()
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
