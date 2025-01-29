from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="BlogAPI Documentation",
      default_version='v1',  
      description="This project is a blog API built using. "
      "Django Rest Framework. It provides a RESTful API for creating, reading, updating, and deleting blog posts."
      "The API is documented using Swagger and supports multiple API endpoints for different operations."
      "The project follows standard professional guidelines for commit messages, API documentation, and code style."
      "NOTE: Every following  path starts with /api/.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/', include('api.urls')), 
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 