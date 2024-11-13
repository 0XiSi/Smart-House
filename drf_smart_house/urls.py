from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from home import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# router = routers.DefaultRouter()
# router.register(r'dh11s', views.DH11sViewSetApiView, 'dh11')
# router.register(r'relays', views.RelaysViewSetApiView, 'relay')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
