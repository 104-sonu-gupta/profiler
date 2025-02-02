from django.urls import path
from .import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),

    path('projects/', views.getProjects),

    path('projects/<str:id>', views.getProject),

    path('projects/<str:id>/vote/', views.voteProject),

    # path('remove-tag/', views.removeTagFromProject),
]
