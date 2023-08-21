from django.contrib import admin
from django.urls import include, path
from django.urls import re_path

from django.conf import settings
from django.conf.urls.static import static

# from todo_api import urls as todo_urls

from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


from .views import login_view, otp_view, main_view, logout_view, scrapping_view
# from allauth.account.views import LoginView
# from allauth.account.views import SignupView
# from allauth.account.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('authentications.urls')),
    # path('api/schema', SpectacularAPIView.as_view(), name="schema"),
    # path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
    
    
    # path('', main_view, name="main"),
    path("__reload__/", include("django_browser_reload.urls")),






    # path('accounts/', include('allauth.urls')),
    # path('accounts/login', LoginView.as_view(), name="account_login"),
    # path('accounts/signup', SignupView.as_view(), name="account_signup"),
    # path('accounts/logout', LogoutView.as_view(), name="account_logout"),

    
    # path("accounts/", include("accounts.urls")),
    # path('api-auth/', include('rest_framework.urls')),
    # path('todos/', include(todo_urls)),
    # path('api-token-auth/', obtain_auth_token),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/', include('user_api.urls')),

    # path('authentications/', include('authentications.urls')),
    # path(r'^', include('authentications.urls')),



]
