from django.urls import path
from .views import login_view, logout_view, signup_view
    
urlpatterns = [
    path('api/login/', login_view),
    path('api/logout/', logout_view),
    path('api/signup/', signup_view),
]