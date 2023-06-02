from django.urls import path
from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import LogList

urlpatterns = [
    path('logs/', LogList.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
