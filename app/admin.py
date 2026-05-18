from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(Tarifa)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Competidor)
admin.site.register(ProductoCompetidor)
admin.site.register(Receta)
admin.site.register(IngredienteReceta)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
admin.site.register(CarritoGuardado)

class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('tipo_usuario', 'tarifa', 'telefono', 'direccion_envio', 'cif_nif', 'razon_social', 'direccion_fiscal', 'saldo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('tipo_usuario', 'tarifa', 'telefono', 'direccion_envio', 'cif_nif', 'razon_social', 'direccion_fiscal', 'saldo')}),
    )

admin.site.register(Usuario, UsuarioAdmin)