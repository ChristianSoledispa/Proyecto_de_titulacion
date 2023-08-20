# from django.urls import include, path
# from . import views

# urlpatterns = [
#     path('authentications/', views.auths, name='authentications'),
#     path('mongo_auth/', include('mongo_auth.urls')),
#     ]


from django.urls import re_path 
from . import views 
 
urlpatterns = [ 
    re_path(r'^api/auths$', views.authentication_list),
    re_path(r'^api/auths/(?P<pk>[0-9]+)$', views.authentication_detail),
    re_path(r'^api/auths/superuser$', views.authentication_list_is_superuser)
]
