from django.urls import path
from rest_framework.authtoken import views

from .views import LogList

urlpatterns = [
    path('logs/', LogList.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
]
