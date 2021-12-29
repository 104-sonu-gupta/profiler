from django.urls import path
from blogs import views

urlpatterns = [

    path('', views.blogs, name='posts'),
    
    path('single-post/<str:id>/', views.single_post, name='single-post'),
    
    path('create-post/', views.create_post, name='create-post'),
    
    path('my-posts/', views.user_posts, name='user-posts'),
    
    path('update-post/<str:id>/', views.edit_post, name='update-post'),
    
    path('delete-post/<str:id>/', views.delete_post, name='delete-post'),
    
    path('tag-view/<str:id>/', views.tags_view, name='tag-view'),
    
]
