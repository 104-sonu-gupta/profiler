from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.profiles, name='profiles'),
    path('profile/<str:id>', views.individualprofile, name='user-profile'),
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

]