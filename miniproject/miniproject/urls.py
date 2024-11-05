
# from django.contrib import admin
# from django.urls import path,include
# from django.conf.urls.static import static
# from django.conf import settings

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',include('accounts.urls')),
#     path('product/',include('product.urls')),
#     path('admindashboard/', include('admindashboard.urls')),   
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('', include('accounts.urls')),  # Include accounts app URLs
    path('product/', include('product.urls')),  # Include product app URLs
    path('admindashboard/', include('admindashboard.urls')),  # Include admin dashboard URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in debug mode
