from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView, # generate token based on user
    TokenRefreshView, # Generate refresh token
)

urlpatterns = [
    path('',views.getRoutes, name='routes'),
    path('projects/',views.getProjects),
    path('projects/<str:pk>/',views.getProject),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

