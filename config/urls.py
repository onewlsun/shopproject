from django.contrib import admin
from django.urls import path
from catalog.views import product_list, product_detail  # <- теперь эти функции точно есть
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)