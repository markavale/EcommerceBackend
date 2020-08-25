from django.urls import path
from .views import registration_view, user_properties_view, ChangePassword#, update_user_view
from rest_framework.authtoken.views import obtain_auth_token # built in view
app_name = 'user'


urlpatterns = [

    path('register/', registration_view, name='registration'),
    path('login/', obtain_auth_token, name='login'),
    path('properties/', user_properties_view, name='properties'),
    path('change-password/', ChangePassword.as_view(), name='change-password')
    #path('properties/update/', update_user_view, name='update-user'),
]