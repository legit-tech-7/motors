from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    
    # Change this line to match what you need:
    path('login/', auth_views.LoginView.as_view(template_name='car/login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(next_page='car_list'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)