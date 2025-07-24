from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
                  path('users/', include('users.urls')),
                  path('listings/', include('listings.urls')),
                  path('', include('pages.urls')),  # For homepage and contact
                  path('', include('pages.urls')),
                  path('listings/', include('listings.urls')),
                  path('users/', include('users.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)