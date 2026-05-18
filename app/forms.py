from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'nombre', 'apellidos', 'email', 'tipo_usuario', 'cif_nif', 'razon_social', 'direccion_fiscal', 'direccion_envio', 'telefono'
        ]

        labels = {
            'username': 'Nombre de usuario (ID para entrar)',
            'nombre': 'Nombre de pila',
            'email': 'Correo electrónico profesional',
            'cif_nif': 'CIF/NIF',
            'tipo_usuario': 'Tipo de Cliente (Particular/Empresa)'
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
            'cif_nif': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_fiscal': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'direccion_envio': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['tipo_usuario'].choices = [
                ('B2C', 'Particular (B2C)'),
                ('B2B', 'Empresa (B2B)'),
            ]

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'cantidad', 'categoria', 'origen', 'calibre', 'es_ecologico', 'precio_base', 'stock', 'imagenProducto'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'calibre': forms.TextInput(attrs={'class': 'form-control'}),
            'es_ecologico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagenProducto': forms.URLInput(attrs={'class': 'form-control'}),
        }
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellidos', 'email', 'tipo_usuario', 'cif_nif', 'razon_social', 'direccion_fiscal', 'direccion_envio', 'telefono', 'tarifa']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
            'cif_nif': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_fiscal': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'direccion_envio': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'tarifa': forms.Select(attrs={'class': 'form-select'}),
        }
    
class UsuarioNuevoForm(UsuarioForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UsuarioForm.Meta):
        fields = UsuarioForm.Meta.fields

class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['nombre_tarifa', 'porcentaje_descuento']
        widgets = {
            'nombre_tarifa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: VIP, Mayorista, Estándar'}),
            'porcentaje_descuento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01', 'min': '0', 'max': '100'}),
        }
        labels = {
            'nombre_tarifa': 'Nombre de la Tarifa',
            'porcentaje_descuento': 'Porcentaje de Descuento (%)'
        }

class AgregarCarritoForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control input-cantidad'  # Usamos nuestra clase CSS en vez de estilos en línea
        })
    )

class ActualizarCarritoForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control input-cantidad'  # Cambiado aquí también
        })
    )

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'estado']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class PedidoEditarForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class CompetidorForm(forms.ModelForm):
    class Meta:
        model = Competidor
        fields = ['nombre_competidor']
        widgets = {
            'nombre_competidor': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
class ProductoCompetidorForm(forms.ModelForm):
    class Meta:
        model = ProductoCompetidor
        fields = ['producto_san_blas', 'nombre', 'cantidad', 'origen', 'calibre', 'es_ecologico', 'precio_base', 'imagen_url']
        widgets = {
            'producto_san_blas': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'calibre': forms.TextInput(attrs={'class': 'form-control'}),
            'es_ecologico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'instrucciones', 'tiempo_preparacion', 'dificultad', 'imagenReceta']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'instrucciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'tiempo_preparacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'dificultad': forms.Select(attrs={'class': 'form-select'}),
            'imagenReceta': forms.URLInput(attrs={'class': 'form-control'}),
        }

class IngredienteRecetaForm(forms.ModelForm):
    class Meta:
        model = IngredienteReceta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
        }
        extra = 3

class AgregarSaldoForm(forms.Form):
    numero_tarjeta = forms.CharField(
        label='Número de Tarjeta',
        max_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0000 0000 0000 0000',
            'maxlength': '16',
        })
    )
    fecha_caducidad = forms.CharField(
        label='Fecha de Caducidad',
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY',
            'maxlength': '5',
        })
    )
    cvv = forms.CharField(
        label='CVV',
        max_length=4,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '***',
            'maxlength': '3',
        })
    )
    cantidad = forms.DecimalField(
        label='Cantidad a Agregar',
        min_value=1.00,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.10',
            'min': '1.00',
        })
    )
