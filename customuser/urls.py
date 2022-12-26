from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_url_patterns = [
  path('api/note/', include('notes.urls')),
  path('api/member/', include('members.urls')),
  path('accounts/', include('dj_rest_auth.urls')),
  # path('accounts/', include('dj_rest_auth.registration.urls')),
  # path('accounts/', include('allauth.urls')),
  # path('accounts/', include('accounts.urls')),
]

schema_view = get_schema_view(
  openapi.Info(
    title="fit note API 문서",
    default_version='0.0.1',
    terms_of_service="https://www.google.com/policies/terms/",
  ),
  public=True,
  permission_classes=(permissions.AllowAny,),
  patterns=schema_url_patterns,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('api/note/', include('notes.urls')),
    path('api/member/', include('members.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('dj_rest_auth.registration.urls')),
]