from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('', include('accounts.urls')), 
    path('product/', include(('product.urls', 'product'))), 
    path('admindashboard/', include('admindashboard.urls')), 
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('other/', include('other.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in debug mode
