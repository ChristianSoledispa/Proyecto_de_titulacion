# from django.urls import include, path
# from . import views

# urlpatterns = [
#     path('authentications/', views.auths, name='authentications'),
#     path('mongo_auth/', include('mongo_auth.urls')),
#     ]


from django.urls import path
from .views import AuthenticationAPI, ScrappingAPI
 
urlpatterns = [ 
    path('api/auths', AuthenticationAPI.authentication_list),
    path('api/auths/<int:pk>', AuthenticationAPI.authentication_detail),
    path('api/auths/superuser', AuthenticationAPI.authentication_list_is_superuser),
    path('login/', ScrappingAPI.login_view, name="login"),
    path('signup/', ScrappingAPI.signup_view, name="signup"),
    path('logout/', ScrappingAPI.logout_view, name="logout"),
    path('scrapping/<id_client>', ScrappingAPI.scrapping_view, name="scrapping"),
    # path('scrapping/website/<id_client>', ScrappingAPI.scrapping_web_view, name="website_scrapping"),
    path('scrapping/history/<id_client>', ScrappingAPI.scrapping_history_view, name="history_scrapping"),
    path('api/scrapping/<id_client>', ScrappingAPI.api_scrapping_user_view, name="api_scrapping"),
    path('api/scrapping/website/<id_client>', ScrappingAPI.api_scrapping_website_view, name="api_website_scrapping"),
    path('api/scrapping/history/<id_client>', ScrappingAPI.api_scrapping_history_view, name="api_history_scrapping"),
    path('', ScrappingAPI.main_view, name='main'),
]
