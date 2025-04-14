from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.authtoken import views

# Версия API
API_VERSION = settings.API_VERSION


urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{API_VERSION}/', include('api.urls')),
    path(f'api/{API_VERSION}/token-auth/', views.obtain_auth_token),
    path('orders/', include('orders.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
