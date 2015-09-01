from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.user.login_user, name='login'),
    url(r'^logout/$', views.user.logout_user, name='logout'),
    url(r'^signup/$', views.user.UserSignup.as_view(), name='signup'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.user.UserProfileView.as_view(), name='profile'),
    url(r'^courses/$', views.course.CourseList.as_view(), name='courses'),
    url(r'^course/(?P<pk>[0-9]+)/$', views.course.CourseDetail.as_view(), name='course-detail'),
    url(r'^courses/new/$', views.course.CourseCreate.as_view(), name='create-course'),
    url(r'^subjets/$', views.subject.SubjectList.as_view(), name='subjects'),
    url(r'^subject/(?P<pk>[0-9]+)/$', views.subject.SubjectDetail.as_view(), name='subject-detail'),
]
