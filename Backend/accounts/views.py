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

# def kakao_login(request):
#     app_rest_api_key = settings.SOCIAL_AUTH_KAKAO_CLIENT_ID
#     redirect_uri = "http://127.0.0.1:8000/account/login/kakao/callback"
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
#     )

# def kakao_callback(request):                                                                  
#     params = urllib.parse.urlencode(request.GET)
#     return redirect(f'http://127.0.0.1:3000/account/login/kakao/callback?{params}')

# def kakao_auth_handler(request):
#     pass

