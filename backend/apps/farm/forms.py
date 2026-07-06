from django import forms
from apps.products.models import Farm, Product

class FarmRegistrationForm(forms.ModelForm):
    image_file = forms.FileField(required=False, label='Chọn ảnh từ thiết bị')

    class Meta:
        model = Farm
        fields = ['name', 'tax_code', 'phone', 'email', 'region', 'province', 'description', 'image_url', 'business_license']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProductForm(forms.ModelForm):
    image_file = forms.FileField(required=False, label='Chọn ảnh từ thiết bị')

    class Meta:
        model = Product
        fields = ['category', 'name', 'price', 'unit', 'badge', 'image_url', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
