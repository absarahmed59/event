"""
URL configuration for Events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', views.home, name='home'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('services/', views.services, name='services'),
    path('package/<int:package_id>/', views.package, name='package'),
    # path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('servicepage/', views.make_service)
    path('booking_proposal/<int:service_id>/', views.booking_proposal, name='booking_proposal'),
    path('create_service/', views.create_service, name='create_service'),
    path('confirm_booking/<int:booking_id>/', views.confirm_booking, name='confirm'),
    path('reject_booking/<int:booking_id>/', views.reject_booking, name='reject'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('confirm_booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('reject_booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
