from django.urls import path
from projects import views

urlpatterns = [

    path('', views.projects, name='projects'),
    
    path('project/<id>/', views.project, name='single-project'),
    
    path('create-project/', views.createProject, name='create-project'),
    
    path('update-project/<id>/', views.updateProject, name='update-project'),
    
    path('delete-project/<id>/', views.deleteProject, name='delete-project'),
]
