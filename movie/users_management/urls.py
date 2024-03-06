from django.urls import path
from .views import *

app_name = 'users_management'
urlpatterns = [

    path('register/', SignUp.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('user_profile/<slug:user_slug>/', UserProfileView.as_view(), name='user_profile'),
]
