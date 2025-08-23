from django.contrib import admin
from .models import Car, CarImage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price', 'condition', 'sold')
    list_filter = ('condition', 'sold', 'make')
    search_fields = ('make', 'model', 'description')
    inlines = [CarImageInline]

admin.site.register(CarImage)