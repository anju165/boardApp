"""boardAppV3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('boardAppV3/', include('app.urls')),
    path('boardAppV3/signup', include('account.urls')),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout',auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("", views.home, name="home"),
    path('boardAppV3/reset', include('account.urls')),
    path('boardAppV3/reset/<uidb64>/<token>/', include('account.urls')),
    path('boardAppV3/reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name = 'password_reset_done.html'
    ), name = 'password_reset_done'),
    path('boardAppV3/reset/complete', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'password_reset_complete.html'
    ), name = 'password_reset_complete')
]
