# from django.urls import include, path
# from . import views

# urlpatterns = [
#     path('authentications/', views.auths, name='authentications'),
#     path('mongo_auth/', include('mongo_auth.urls')),
#     ]


from django.urls import re_path 
from . import views 
 
urlpatterns = [ 
    re_path('api/auths', views.AuthenticationAPI.authentication_list),
    re_path('api/auths/<int:pk>', views.AuthenticationAPI.authentication_detail),
    re_path('api/auths/superuser', views.AuthenticationAPI.authentication_list_is_superuser)
]
