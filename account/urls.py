from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.signup, name='signup'),
    path('reset',auth_views.PasswordResetView.as_view(
        template_name = 'password_reset.html',
        email_template_name = 'password_reset_email.html',
        subject_template_name = 'password_reset_subject.txt'
    ), name = 'reset'),
    path('password_reset_confirm',auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm')
]