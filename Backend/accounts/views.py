from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import redirect 
from django.conf import settings
import urllib

class GoogleLoginView(SocialLoginView):
    authentication_classes = (JWTTokenUserAuthentication,)
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.FRONTEND_URL + "google-login"
