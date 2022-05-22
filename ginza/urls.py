from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_url_patterns = [
    path('', include('product.urls')),
    path('auth/', include('user.urls')),
    path('admin/', admin.site.urls),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Ginza-Api Docs",
        default_version='v1',
        description="API 문서"
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)
urlpatterns = [
    path('', include('product.urls')),
    path('', include('user.urls')),
    # path('', include('order.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
