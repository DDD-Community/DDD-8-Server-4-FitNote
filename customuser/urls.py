from django.contrib import admin
from django.urls import path, include

# drf-yasg
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# 기본 Url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('dj_rest_auth.registration.urls')),
    path('hypeboy/', include('hypeboy.urls')),
    path('attention/', include('attention.urls')),
]

# 스키마 뷰 셋팅
schema_view = get_schema_view(
  openapi.Info(
    title="fit note API 문서",
    default_version='0.0.1',
    terms_of_service="https://www.google.com/policies/terms/",
  ),
  public=True,
  permission_classes=(permissions.AllowAny,),
  patterns = urlpatterns,
)

# drf_yasg url 
urlpatterns += [
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]