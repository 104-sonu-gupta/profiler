from django.urls import path
from users import views

urlpatterns = [

    
    path('', views.profiles, name='profiles'),
    
    path('profile/<str:id>', views.individualprofile, name='user-profile'),

    path('register/', views.registerUser, name='register'),
    
    path('login/', views.loginPage, name='login'),
    
    path('logout/', views.logoutPage, name='logout'),
    
    path('account/', views.userAccount, name='account'),
    
    path('account/edit-account/', views.editAccount, name='edit-account'),
    
    path('account/add-skill/', views.addSkill, name='add-skill'),

    path('account/edit-skill/<id>', views.editSkill, name='edit-skill'),
    
    path('account/delete-skill/<id>', views.deleteSkill, name='delete-skill'),
    
    path('account/inbox', views.inbox, name='inbox'),
    
    path('account/inbox/message/<str:id>', views.viewMessage, name='view-message'),

    path('send-message/<str:pk>', views.sendMessage, name='send-message'),

]