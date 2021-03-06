"""vision_space URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from dj_rest_auth.registration.views import VerifyEmailView
from accounts.views import GoogleLoginView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('dj_rest_auth.urls')),
    path('api/v1/account/signup/', include('dj_rest_auth.registration.urls')),
    path('api/v1/account/google/', GoogleLoginView.as_view(), name="google_login"),
    path('api/v1/account/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api/v1/account/allauth/', include('allauth.urls'), name='socialaccount_signup'),
    path('api/v1/board/', include('board.urls')),
    path('api/v1/file/', include('file.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
