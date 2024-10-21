from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('converter.urls')),
    path('admin/', admin.site.urls),
]
