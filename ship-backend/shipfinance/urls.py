from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home),  # 👈 FIX: home route added
    path('admin/', admin.site.urls),
    path('api/', include('finance.urls')),
]
