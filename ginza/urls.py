from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('product.urls')),
    path('', include('user.urls')),
    path('', include('order.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
]
