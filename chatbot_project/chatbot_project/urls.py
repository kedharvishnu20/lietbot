from django.contrib import admin
from django.urls import path, include  # Import 'include' for app URLs

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('', include('chatbot.urls')),  # Include all routes from the 'chatbot' app
]
