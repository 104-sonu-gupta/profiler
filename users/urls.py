from django.urls import path
from users import views

urlpatterns = [

    path('', views.profiles, name='profiles'),
    path('profile/<str:id>', views.individualprofile, name='user-profile'),

]
