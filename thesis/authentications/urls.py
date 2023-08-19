from django.urls import include, path
from . import views

urlpatterns = [
    path('authentications/', views.auths, name='authentications'),
    path('mongo_auth/', include('mongo_auth.urls')),
    ]