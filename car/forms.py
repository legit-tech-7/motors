from django import forms
from .models import Car, CarImage

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image', 'is_main']