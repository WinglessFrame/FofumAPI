from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # login / register
    path('api-auth/', include('rest_framework.urls', namespace='auth')),
    # forum api
    path('forum/api/', include('Forum.api.urls', namespace='forum-api')),
    # JWT AUTH
    path('auth/', include('accounts.api.urls', namespace='jwt-auth/register')),
    # DOCS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
