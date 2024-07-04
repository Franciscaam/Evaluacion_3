from django import forms
from ecommerce.models import Contacto
from .models import Producto
from .models import Categoria, Proveedor

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'email', 'tipo_mensaje', 'mensaje']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['name', 'image', 'sale_price', 'description']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'email', 'telefono', 'direccion']
