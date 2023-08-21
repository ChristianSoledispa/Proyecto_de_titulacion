# from django.urls import include, path
# from . import views

# urlpatterns = [
#     path('authentications/', views.auths, name='authentications'),
#     path('mongo_auth/', include('mongo_auth.urls')),
#     ]


from django.urls import re_path, path
from .views import AuthenticationAPI, ScrappingAPI
 
urlpatterns = [ 
    path('api/auths', AuthenticationAPI.authentication_list),
    path('api/auths/<int:pk>', AuthenticationAPI.authentication_detail),
    path('api/auths/superuser', AuthenticationAPI.authentication_list_is_superuser),
    path('login/', ScrappingAPI.login_view, name="login"),
    path('otp/', ScrappingAPI.otp_view, name="otp"),
    path('logout/', ScrappingAPI.logout_view, name="logout"),
    path('scrapping/<id_client>', ScrappingAPI.scrapping_user_view, name="scrapping"),
    path('scrapping/website/<id_client>', ScrappingAPI.scrapping_web_view, name="website_scrapping"),
    path('api/scrapping/<id_client>', ScrappingAPI.api_scrapping_user_view, name="api_scrapping"),
    path('api/scrapping/website/<id_client>', ScrappingAPI.api_scrapping_website_view, name="api_website_scrapping"),
]
