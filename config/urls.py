
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from catalog import views as catalog_views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('catalog.urls', 'catalog'), namespace='catalog')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', catalog_views.register_view, name='register'),
    path('', catalog_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True  
    ), name='login'),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
    path('register/', accounts_views.register, name='register'),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)