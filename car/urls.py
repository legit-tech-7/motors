from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Car Management
    path('', views.car_list, name='car_list'),
    path('cars/add/', views.add_car, name='add_car'),
    path('cars/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:car_id>/delete/', views.delete_car, name='delete_car'),
     path("cars/<int:pk>/", views.car_detail, name="car_detail"),
    
    # Image Management
    path('cars/<int:car_id>/images/', views.add_car_images, name='add_car_images'),
    path('images/<int:image_id>/set-main/', views.set_main_image, name='set_main_image'),
    path('images/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    path('reports/export-csv/', views.export_cars_csv, name='export_cars_csv'),
    
    # Settings
    path('settings/', views.settings, name='settings'),
    path('contact/', views.contact, name='contact'),
]