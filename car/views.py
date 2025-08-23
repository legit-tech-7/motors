from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum  # Add this import at the top of your views.py

import csv
from .models import Car, CarImage
from .forms import CarForm, CarImageForm

@login_required
def dashboard(request):
    cars = Car.objects.all()
    total_cars = cars.count()
    active_cars = cars.filter(sold=False).count()
    total_value = cars.filter(sold=False).aggregate(Sum('price'))['price__sum'] or 0
    
    context = {
        'total_cars': total_cars,
        'active_cars': active_cars,
        'total_value': total_value,
        'recent_cars': cars.order_by('-date_added')[:5],
    }
    return render(request, 'car/dashboard.html', context)


def car_list(request):
    cars = Car.objects.all().order_by('-date_added')
    return render(request, 'car/car_list.html', {'cars': cars})

@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            messages.success(request, 'Car added successfully! Add images now.')
            return redirect('add_car_images', car_id=car.id)
    else:
        form = CarForm()
    
    return render(request, 'car/add_car.html', {'form': form})

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car updated successfully!')
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    
    return render(request, 'car/edit_car.html', {'form': form, 'car': car})

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Car deleted successfully!')
        return redirect('car_list')
    
    return render(request, 'car/delete_car.html', {'car': car})

@login_required
def add_car_images(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = CarImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.car = car
            
            # If this is the first image, make it main automatically
            if not CarImage.objects.filter(car=car).exists():
                image.is_main = True
                
            image.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('add_car_images', car_id=car.id)
    else:
        form = CarImageForm()
    
    # Simple version - show images in upload order (no ordering)
    images = CarImage.objects.filter(car=car)
    
    return render(request, 'car/add_car_images.html', {
        'car': car,
        'form': form,
        'images': images,
    })

@login_required
def set_main_image(request, image_id):
    image = get_object_or_404(CarImage, id=image_id)
    # Set all images for this car as not main first
    CarImage.objects.filter(car=image.car).update(is_main=False)
    # Set this one as main
    image.is_main = True
    image.save()
    messages.success(request, 'Main image set successfully!')
    return redirect('add_car_images', car_id=image.car.id)

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(CarImage, id=image_id)
    car_id = image.car.id
    image.delete()
    messages.success(request, 'Image deleted successfully!')
    return redirect('add_car_images', car_id=car_id)

@login_required
def reports(request):
    return render(request, 'car/reports.html')

@login_required
def export_cars_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cars_inventory.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Make', 'Model', 'Year', 'Price', 'Condition', 'Status'])
    
    cars = Car.objects.all()
    for car in cars:
        status = "Sold" if car.sold else "Available"
        writer.writerow([
            car.make,
            car.model,
            car.year,
            car.price,
            car.get_condition_display(),
            status
        ])
    
    return response

@login_required
def settings(request):
    return render(request, 'car/settings.html')




def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    images = car.images.all()  # Ordered by 'order'
    main_image = images.filter(is_main=True).first() or images.first()
    return render(request, "car/car_detail.html", {
        "car": car,
        "main_image": main_image,
        "images": images,
    })

from django.shortcuts import render

def contact(request):
    return render(request, 'car/contact.html')
