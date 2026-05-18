from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from decimal import Decimal

# Create your models here.

# USUARIOS Y TARIFAS

class Tarifa(models.Model):
    nombre_tarifa = models.CharField(max_length=20)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Tarifa: {self.nombre_tarifa} ({self.porcentaje_descuento}%)"

class Usuario(AbstractUser):
    class TIPO_USUARIO(models.TextChoices):
        B2C = 'B2C'
        B2B = 'B2B'
        ADMIN = 'ADMIN'

    idUsuario = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)

    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO.choices, default=TIPO_USUARIO.B2C)

    # Datos contacto/envio
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion_envio = models.TextField(blank=True, null=True)

    tarifa = models.ForeignKey(Tarifa, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuarios_tarifa")


    # Empresas
    cif_nif = models.CharField(max_length=20, blank=True, null=True)
    razon_social = models.CharField(max_length=100, blank=True, null=True)
    direccion_fiscal = models.TextField(blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Saldo
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def clean(self):
        # Usuario normal no tenga datos de empresas por error
        if self.tipo_usuario == self.TIPO_USUARIO.B2C:
            if self.cif_nif or self.razon_social:
                self.cif_nif = None
                self.razon_social = None

        # Empresa debera tener cif obligatoriamente
        if self.tipo_usuario == self.TIPO_USUARIO.B2B and not self.cif_nif:
            raise ValidationError("Si el usuario es una empresa (B2B) debe tener un CIF/NIF asignado.")
        
    def __str__(self):
        return f"Usuario {self.nombre}, {self.apellidos} - Tipo: {self.tipo_usuario}"
    


    # CATEGORIAS Y PRODUCTOS
class Categoria(models.Model):
    idCategoria = models.CharField(max_length=30)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"Categoría: {self.nombre}"
    

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    cantidad = models.TextField(blank=True, null=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos_categoria")

    # Detalles producto
    origen = models.CharField(max_length=50, blank=True, null=True)
    calibre = models.CharField(max_length=50, blank=True, null=True)
    es_ecologico = models.BooleanField(default=False)

    # Precios y stock
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    # IMAGEN
    imagenProducto = models.URLField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"Producto: {self.nombre} (Origen: {self.origen})"




    # COMPETIDORES Y SUS PRODUCTOS

class Competidor(models.Model):
    idCompetidor = models.CharField(max_length=30)
    nombre_competidor = models.CharField(max_length=50)

    def __str__(self):
        return f"Competidor: {self.nombre_competidor}"
    
class ProductoCompetidor(models.Model):
    idProdCompetidor = models.CharField(max_length=30)

    competidor = models.ForeignKey(Competidor, on_delete=models.CASCADE, related_name="productos_del_competidor")


    producto_san_blas = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="comparativas_competidores")

    nombre = models.CharField(max_length=50)
    cantidad = models.TextField(blank=True, null=True)

    # Datos para comparativas
    origen = models.CharField(max_length=50, blank=True, null=True)
    calibre = models.CharField(max_length=50, blank=True, null=True)
    es_ecologico = models.BooleanField(default=False)

    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    imagen_url = models.URLField(max_length=500, blank=True, null=True)

    analisis_ia = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} de {self.competidor.nombre_competidor}"



    # GASTRONOMIA (RECETAS)

class Receta(models.Model):
    class Dificultad(models.TextChoices):
        BAJA = 'BAJA', 'Baja'
        MEDIA = 'MEDIA', 'Media'
        ALTA = 'ALTA', 'Alta'

    idReceta = models.CharField(max_length=30)
    titulo = models.CharField(max_length=80)
    instrucciones = models.TextField()
    tiempo_preparacion = models.IntegerField(help_text="Tiempo en minutos")

    dificultad = models.CharField(max_length=10, choices=Dificultad.choices, default=Dificultad.BAJA)

    imagenReceta = models.URLField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"Receta: {self.titulo} (Dificultad: {self.dificultad})"
    

class IngredienteReceta(models.Model):
    idIngrediente = models.CharField(max_length=30)

    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="ingredientes_de_receta")

    # Referencia al producto
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="recetas_donde_aparece")

    cantidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} para {self.receta.titulo}"



    # Pedidos y carritos

class Pedido(models.Model):
    class EstadoPedido(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADO = 'PAGADO', 'Pagado'
        ENVIADO = 'ENVIADO', 'Enviado'
        ENTREGADO = 'ENTREGADO', 'Entregado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    idPedido = models.CharField(max_length=30)


    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos_usuario")

    fecha_pedido = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(max_length=20, choices=EstadoPedido.choices, default=EstadoPedido.PENDIENTE)

    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pdf_factura = models.FileField(upload_to='facturas/', blank=True, null=True)

    def __str__(self):
        return f"PEdido {self.idPedido} - Cliente: {self.usuario.nombre} ({self.estado})"
    
    # 1. SOLUCIÓN COMPLEMENTARIA PARA LA FACTURA (Doble capa de seguridad)
    def obtener_total_real(self):
        """Calcula el total en tiempo real sumando las líneas si el campo guardado es 0"""
        if self.total_pedido == 0:
            return sum(linea.calcular_subtotal() for linea in self.lineas_pedido.all())
        return self.total_pedido

    # 2. MÉTODO PARA TU VISTA DE COMPRA
    def actualizar_total(self):
        """Suma las líneas creadas y guarda el total real en la base de datos"""
        self.total_pedido = sum(linea.calcular_subtotal() for linea in self.lineas_pedido.all())
        self.save()

    def calcular_cantidad_descontada(self):
        """Calcular cuanto dinero se ha ahorrado en este pedido"""
        total_original_catalogo = sum(
            (linea.producto.precio_base * linea.cantidad) for linea in self.lineas_pedido.all()
        )

        ahorro = Decimal(total_original_catalogo) - Decimal(self.obtener_total_real())
        return round(ahorro, 2)
    
    
    def obtener_base_imponible(self):
        """Calcula la base imponible quitando el 10% de IVA al total real"""
        total = float(self.obtener_total_real())
        # El cálculo matemático exacto para desglosar un 10% de IVA es: Total / 1.10
        return round(total / 1.10, 2)

    def obtener_cuota_iva(self):
        """Calcula cuántos euros son solo de IVA"""
        total = float(self.obtener_total_real())
        return round(total - self.obtener_base_imponible(), 2)
    

class LineaPedido(models.Model):
    idLinea = models.CharField(max_length=30)

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="lineas_pedido")

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="ventas_producto")

    cantidad = models.IntegerField()

    precio_unitario_aplicado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido {self.pedido.idPedido}"
    
    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario_aplicado
    
    def calcular_cuota_iva(self):
        """Calcula el IVA de esta línea (10% del subtotal)"""
        subtotal = self.calcular_subtotal()
        total_sin_iva = round(subtotal / Decimal('1.10'), 2)
        return round(subtotal - total_sin_iva, 2)

# CARRITO DE COMPRAS

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="carrito")

    def __str__(self):
        return f"Carrito de {self.usuario.nombre}"

    def calcular_total_sin_descuento(self):
        """Calcula el total sin aplicar descuentos"""
        return sum(item.calcular_subtotal() for item in self.items_carrito.all())

    def calcular_descuento_aplicado(self):
        """Calcula el descuento basado en la tarifa del usuario"""
        if self.usuario.tarifa:
            return self.calcular_total_sin_descuento() * (self.usuario.tarifa.porcentaje_descuento / 100)
        return 0

    def calcular_total_con_descuento(self):
        """Calcula el total con descuento aplicado"""
        return self.calcular_total_sin_descuento() - self.calcular_descuento_aplicado()


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items_carrito")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="items_en_carritos")
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    def calcular_subtotal(self):
        """Calcula el subtotal de este item"""
        return self.producto.precio_base * self.cantidad
    


class CarritoGuardado(models.Model):
    idCarrito = models.CharField(max_length=30)

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="carritos_guardados")

    nombre_carrito = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Carrito: {self.nombre_carrito} de {self.usuario.nombre}"

