# TE QUIEOR MÁS QUE A NADIE NIÑOOOOOOO (MI NIÑO, MÁS BIEN)
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
import requests
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required, user_passes_test
import os

# Create your views here.

def inicio(request):
    return render(request, 'app/inicio.html')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'app/registro.html', {'form': form})


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE CATEGORIAS
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Lista
class CategoriaListaView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'app/categoria_lista.html'
    context_object_name = 'categorias'

# Nueva (solo permisos)
class CategoriaNuevaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Categoria
    fields = ['nombre']
    template_name = 'app/categoria_crud.html'
    success_url = reverse_lazy('categoria_lista')
    context_object_name = 'categoria'

    def test_func(self):
        return self.request.user.is_staff
    
# Editar (solo permisos)
class CategoriaEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Categoria
    fields = ['nombre']
    template_name = 'app/categoria_crud.html'
    success_url = reverse_lazy('categoria_lista')
    context_object_name = 'categoria'

    def test_func(self):
        return self.request.user.is_staff
    
# Eliminar (solo permisos)
class CategoriaEliminarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Categoria
    template_name = 'app/categoria_confirmar_eliminar.html'
    success_url = reverse_lazy('categoria_lista')
    context_object_name = 'categoria'

    def test_func(self):
        return self.request.user.is_staff
    
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE PRODUCTOS
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Lista
class ProductoListaView(ListView):
    model = Producto
    template_name = 'app/producto_lista.html'
    context_object_name = 'productos'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()

        nombre = self.request.GET.get("input_nombre")
        categoria = self.request.GET.get("select_categoria")
        min_precio = self.request.GET.get("input_min")
        max_precio = self.request.GET.get("input_max")

        if nombre:
            queryset = queryset.filter(nombre__icontains = nombre)
        
        if categoria:
            queryset = queryset.filter(categoria_id = categoria)

        if min_precio:
            queryset = queryset.filter(precio_base__gte = min_precio)

        if max_precio:
            queryset = queryset.filter(precio_base__lte = max_precio)
        
        return queryset.order_by('nombre')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        contexto['categorias'] = Categoria.objects.all()
        contexto['filtros'] = self.request.GET

        return contexto

# Nueva (solo permissos)
class ProductoNuevoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'app/producto_crud.html'
    success_url = reverse_lazy('producto_lista')
    context_object_name = 'producto'

    def test_func(self):
        return self.request.user.is_staff
    
# Editar (solo permisoso)
class ProductoEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'app/producto_crud.html'
    success_url = reverse_lazy('producto_lista')
    context_object_name = 'producto'

    def test_func(self):
        return self.request.user.is_staff
    
# Eliminar (solo permisos)
class ProductoEliminarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Producto
    template_name = 'app/producto_confirmar_eliminar.html'
    success_url = reverse_lazy('producto_lista')
    context_object_name = 'producto'

    def test_func(self):
        return self.request.user.is_staff

# Detalle producto
class ProductoDetalleView(DetailView):
    model = Producto
    template_name = 'app/producto_detalle.html'
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['comparativa_competidores'] = self.object.comparativas_competidores.all()
        return contexto


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE USUARIOS
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class UsuarioListaView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'app/usuario_lista.html'
    paginate_by = 10
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_staff

class UsuarioNuevoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Usuario
    form_class = UsuarioNuevoForm
    template_name = 'app/usuario_crud.html'
    context_object_name = 'usuarios'
    success_url = reverse_lazy('usuario_lista')

    def test_func(self):
        return self.request.user.is_staff
    
    # Guardamos el usuario con la contraseña hasheada (no texto plano)
    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        return redirect(self.success_url)

class UsuarioEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'app/usuario_crud.html'
    context_object_name = 'usuarios'
    success_url = reverse_lazy('usuario_lista')

    def test_func(self):
        return self.request.user.is_staff

class UsuarioEliminarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    template_name = 'app/usuario_confirmar_eliminar.html'
    context_object_name = 'usuarios'
    success_url = reverse_lazy('usuario_lista')

    def test_func(self):
        return self.request.user.is_staff


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE TARIFAS
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Lista
class TarifaListaView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Tarifa
    template_name = 'app/tarifa_lista.html'
    context_object_name = 'tarifas'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff

# Nueva (solo permisos)
class TarifaNuevaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'app/tarifa_crud.html'
    success_url = reverse_lazy('tarifa_lista')
    context_object_name = 'tarifa'

    def test_func(self):
        return self.request.user.is_staff

# Editar (solo permisos)
class TarifaEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'app/tarifa_crud.html'
    success_url = reverse_lazy('tarifa_lista')
    context_object_name = 'tarifa'

    def test_func(self):
        return self.request.user.is_staff

# Eliminar (solo permisos)
class TarifaEliminarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tarifa
    template_name = 'app/tarifa_confirmar_eliminar.html'
    success_url = reverse_lazy('tarifa_lista')
    context_object_name = 'tarifa'

    def test_func(self):
        return self.request.user.is_staff

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE CARRITO DE COMPRAS
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
@login_required
def ver_carrito(request):
    """Vista para ver el contenido del carrito"""
    try:
        carrito = request.user.carrito
    except Carrito.DoesNotExist:
        carrito = Carrito.objects.create(usuario=request.user)

    return render(request, 'app/carrito.html', {
        'carrito': carrito,
        'items': carrito.items_carrito.all()
    })

@login_required
def agregar_al_carrito(request, pk):
    """Vista para agregar un producto al carrito"""

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = AgregarCarritoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']

            # Obtener o crear carrito del usuario
            try:
                carrito = Carrito.objects.get(usuario=request.user)
            except Carrito.DoesNotExist:
                carrito = Carrito.objects.create(usuario=request.user)

            # Verificar si el producto ya está en el carrito
            try:
                productoCarrito = ItemCarrito.objects.get(carrito=carrito, producto=producto)
                # El producto existe, sumamos
                productoCarrito.cantidad += cantidad
                productoCarrito.save()
            except ItemCarrito.DoesNotExist:
                # El producto no existe, lo agregamos
                productoCarrito = ItemCarrito.objects.create(
                    carrito=carrito, 
                    producto=producto, 
                    cantidad=cantidad
                )

            messages.success(request, f'{producto.nombre} agregado al carrito.')
            return redirect('producto_lista')

    else:
        form = AgregarCarritoForm()

    return render(request, 'app/agregar_carrito.html', {
        'form': form,
        'producto': producto
    })

@login_required
def actualizar_carrito(request, pk):
    """Vista para actualizar la cantidad de un item en el carrito"""
    productoCarrito = get_object_or_404(ItemCarrito, pk=pk, carrito__usuario=request.user)

    if request.method == 'POST':
        form = ActualizarCarritoForm(request.POST)
        if form.is_valid():
            nueva_cantidad = form.cleaned_data['cantidad']

            if nueva_cantidad > 0:
                productoCarrito.cantidad = nueva_cantidad
                productoCarrito.save()
                messages.success(request, 'Cantidad actualizada.')
            else:
                productoCarrito.delete()
                messages.success(request, 'Producto eliminado del carrito.')

    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, pk):
    """Vista para eliminar un item del carrito"""
    productoCarrito = get_object_or_404(ItemCarrito, pk=pk, carrito__usuario=request.user)
    productoCarrito.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('ver_carrito')

@login_required
def procesar_compra(request):
    """Vista para procesar la compra y convertir el carrito en pedido"""
    try:
        carrito = request.user.carrito
        items = carrito.items_carrito.all()

        if not items:
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('ver_carrito')

        # Calcula total del carrito con tarifas/descuento
        total_con_descuento = carrito.calcular_total_con_descuento()

        # Verifica que tenga saldo suficiente
        if request.user.saldo < total_con_descuento:
            messages.error(request, 'No tienes suficiente saldo para completar la compra.')
            return redirect('ver_carrito')

        # Hay stock del producto
        for item in items:
            if item.producto.stock < item.cantidad:
                messages.error(request, f'No hay suficiente stock de {item.producto.nombre}. Stock disponible: {item.producto.stock}')
                return redirect('ver_carrito')

        # Procesamos transaccion 
        # Crear el pedido
        try:
            usuario = request.user
            usuario.saldo -= total_con_descuento
            usuario.save()

            pedido = Pedido.objects.create(
                idPedido=f"PED-{request.user.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                fecha_pedido = timezone.now(),
                usuario=usuario,
                estado=Pedido.EstadoPedido.PAGADO,
                total_pedido=total_con_descuento
            )

            # Crear las líneas del pedido
            for linea in items:
                precio_unitario = linea.producto.precio_base
                if usuario.tarifa:
                    precio_unitario -= (linea.producto.precio_base * (usuario.tarifa.porcentaje_descuento / 100))

                LineaPedido.objects.create(
                    idLinea=f"LIN-{pedido.idPedido}-{linea.producto.id}",
                    pedido=pedido,
                    producto=linea.producto,
                    cantidad=linea.cantidad,
                    precio_unitario_aplicado=precio_unitario
                )

                producto = linea.producto
                producto.stock -= linea.cantidad
                producto.save()

            # Vaciar el carrito
            items.delete()

            messages.success(request, f'Compra realizada exitosamente. Número de pedido: {pedido.idPedido}')
            return redirect('pedido_detalle', pk=pedido.idPedido)
        except Exception as e:
            print(f"Error al procesar compra: {e}")
            messages.error(request, 'Problema al procesar el pago de tu pedido. Inténtalo de nuevo.')
            return redirect('ver_carrito')

    except Carrito.DoesNotExist:
        messages.error(request, 'No tienes un carrito activo.')
        return redirect('producto_lista')





@login_required
def pedido_detalle(request, pk):
    """Vista para ver el detalle de un pedido"""
    pedido = get_object_or_404(Pedido, idPedido=pk, usuario=request.user)

    return render(request, 'app/pedido_detalle.html', {
        'pedido': pedido,
        'lineas': pedido.lineas_pedido.all()
    })
    
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE PEDIDO
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class PedidoListaView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Pedido
    template_name = 'app/pedido_lista.html'
    context_object_name = 'pedidos'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff
    
class PedidoNuevoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'app/pedido_crud.html'
    context_object_name = 'pedido'
    success_url = reverse_lazy('pedido_lista')

    def test_func(self):
        return self.request.user.is_staff

def pedido_editar(request, pk):

    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para editar pedidos.')
        return redirect('pedido_lista')

    pedido = get_object_or_404(Pedido, idPedido = pk)

    if request.method == 'POST':
        form = PedidoEditarForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido actualizado correctamente.")
            return redirect('pedido_detalle', pk=pedido.idPedido)
    else:
        form = PedidoEditarForm(instance=pedido)
    
    return render(request, 'app/pedido_crud.html', {'form': form, 'pedido': pedido})


def pedido_eliminar(request, pk):

    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar pedidos.')
        return redirect('pedido_lista')

    pedido = get_object_or_404(Pedido, idPedido=pk)

    pedido.delete()
    messages.success(request, "Pedido eliminado correctamente.")

    return redirect('pedido_lista')

# Ver pedidos propios
def ver_mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    return render(request, 'app/pedido_propios.html', {'pedidos': pedidos})



# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE COMPETIDOR
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Lista competidor
class CompetidorListaView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Competidor
    template_name = 'app/competidor_lista.html'
    context_object_name = 'competidores'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff
    
# Detalle competidor
class CompetidorDetalleView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Competidor
    template_name = 'app/competidor_detalle.html'
    context_object_name = 'competidor'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['productos_competidor'] = self.object.productos_del_competidor.all()
        return contexto
    
# Crear competidor
class CompetidorNuevoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Competidor
    form_class = CompetidorForm
    template_name = 'app/competidor_crud.html'
    context_object_name = 'competidor'
    success_url = reverse_lazy('competidor_lista')

    def test_func(self):
        return self.request.user.is_staff
    
# Editar competidor
class CompetidorEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Competidor
    form_class = CompetidorForm
    template_name = 'app/competidor_crud.html'
    context_object_name = 'competidor'
    success_url = reverse_lazy('competidor_lista')

    def test_func(self):
        return self.request.user.is_staff
    
# Eliminar competidor
class CompetidorEliminarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Competidor
    template_name = 'app/competidor_confirmar_eliminar.html'
    context_object_name = 'competidor'
    success_url = reverse_lazy('competidor_lista')

    def test_func(self):
        return self.request.user.is_staff
    
class CompetidorDetalleView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Competidor
    template_name = 'app/competidor_detalle.html'
    context_object_name = 'competidor'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['productos_competidor'] = self.object.productos_del_competidor.all()
        return contexto
    

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE PRODUCTOS DE COMPETIDOR
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# Nuevo producto competidor
class ProductoCompetidorNuevoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ProductoCompetidor
    form_class = ProductoCompetidorForm
    template_name = 'app/producto_competidor_crud.html'
    context_object_name = 'producto_competidor'
    success_url = reverse_lazy('competidor_lista')

    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        competidor_pk = self.request.GET.get('competidor')
        if competidor_pk:
            competidor = get_object_or_404(Competidor, pk=competidor_pk)
            form.instance.competidor = competidor
        return super().form_valid(form)

    
class ProductoCompetidorEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProductoCompetidor
    form_class = ProductoCompetidorForm
    template_name = 'app/producto_competidor_crud.html'
    context_object_name = 'producto_competidor'
    success_url = reverse_lazy('competidor_lista')

    def test_func(self):
        return self.request.user.is_staff
    

def producto_competidor_eliminar(request, pk):

    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar productos de competidores.')
        return redirect('competidor_lista')

    producto_competidor = get_object_or_404(ProductoCompetidor, pk=pk)

    producto_competidor.delete()
    messages.success(request, "Producto del competidor eliminado correctamente.")

    return redirect('competidor_lista')

# MODULO COMPARATIVA DE PRODUCTOS DE COMPETIDORES CON INGELIGENCIA ARTIFICIAL (OPENAI)
def generar_comparativa_ia(request, pk):

    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar productos de competidores.')
        return redirect('inicio')

    producto_competidor = get_object_or_404(ProductoCompetidor, pk=pk)
    producto_san_blas = producto_competidor.producto_san_blas

    # 1. Tu clave y la URL directa de Google
    API_KEY = os.environ.get('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    # 2. El texto que le enviamos a la IA
    prompt = f"""
        Eres un analista experto agrícola para la empresa "San Blas". 
        Compara nuestro producto con el de la competencia y redacta una breve conclusión
        para ayudar al cliente a decidirse por nosotros. Deberas calcular el precio final de ambos productos teniendo en cuenta la cantidad.

        Nuestro producto (San Blas):
        - Nombre: {producto_san_blas.nombre}
        - Precio final(de la cantidad): {producto_san_blas.precio_base}€
        - Cantidad: {producto_san_blas.cantidad}
        - Ecológico: {"Sí" if producto_san_blas.es_ecologico else "No"}
        - Origen: {producto_san_blas.origen}

        Producto de la competencia ({producto_competidor.competidor.nombre_competidor}):
        - Nombre: {producto_competidor.nombre}
        - Precio final(de la cantidad): {producto_competidor.precio_base}€
        - Cantidad: {producto_competidor.cantidad}
        - Ecológico: {"Sí" if producto_competidor.es_ecologico else "No"}
        - Origen: {producto_competidor.origen}
        Resalta la calidad, el precio o el factor ecológico si es mejor que el competidor, 
        o justifica por qué nuestro producto sigue siendo una buena opción aunque el competidor 
        tenga alguna ventaja. 
        REGLAS ESTRICTAS:
        1. RESPONDE CON UN MAXIMO DE 80 PALABRAS CON LA CONCLUSION, NO HAGAS UN ANALISIS EXTENSO, SOLO UNA CONCLUSION BREVE Y CLARA PARA EL CLIENTE. 
        2. PROHIBIDO USAR "*". 
        """

    # 3. El formato exacto que pide Google
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        # 4. Hacemos la llamada directa a internet
        response = requests.post(url, json=payload)
        datos = response.json() # Convertimos la respuesta a diccionario

        # 5. Buceamos en la respuesta para sacar solo el texto
        texto_ia = datos['candidates'][0]['content']['parts'][0]['text']
        
        # 6. Lo guardamos en tu base de datos
        producto_competidor.analisis_ia = texto_ia
        producto_competidor.save()
        
        messages.success(request, "¡Análisis de IA generado con éxito!")

    except Exception as e:
        # Si falla, imprimimos la respuesta de Google para ver qué pasa
        print(f"ERROR PYTHON: {e}")
        messages.error(request, "No se pudo conectar con la IA en este momento.")

    return redirect('producto_detalle', pk=producto_san_blas.pk)


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# VIEWS DE RECETAS/INGREDIENTES
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# View lista recetas
class RecetaListaView(ListView):
    model = Receta
    template_name = 'app/receta_lista.html'
    context_object_name = 'recetas'
    paginate_by = 10


# View crear receta 
class RecetaNuevaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'app/receta_crud.html'
    success_url = reverse_lazy('receta_lista')
    context_object_name = 'receta'

    def test_func(self):
        return self.request.user.is_staff

# View detalle receta
class RecetaDetalleView(DetailView):
    model = Receta
    template_name = 'app/receta_detalle.html'
    context_object_name = 'receta'

# View editar receta
class RecetaEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'app/receta_crud.html'
    success_url = reverse_lazy('receta_lista')
    context_object_name = 'receta'

    def test_func(self):
        return self.request.user.is_staff

# View eliminar receta
class RecetaEliminarView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Receta
    template_name = 'app/receta_confirmar_eliminar.html'
    success_url = reverse_lazy('receta_lista')
    context_object_name = 'receta'

    def test_func(self):
        return self.request.user.is_staff
    
# Añadir ingrediente a receta
class IngredienteRecetaNuevoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = IngredienteReceta
    form_class = IngredienteRecetaForm
    template_name = 'app/ingrediente_receta_crud.html'
    context_object_name = 'ingrediente_receta'
    success_url = reverse_lazy('receta_lista')

    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        receta_pk = self.kwargs.get('receta_pk')
        if receta_pk:
            receta = get_object_or_404(Receta, pk=receta_pk)
            form.instance.receta = receta
        return super().form_valid(form)
    
class IngredienteRecetaEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = IngredienteReceta
    form_class = IngredienteRecetaForm
    template_name = 'app/ingrediente_receta_crud.html'
    context_object_name = 'ingrediente_receta'
    success_url = reverse_lazy('receta_lista')

    def test_func(self):
        return self.request.user.is_staff
    
def ingrediente_receta_eliminar(request, pk):

    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar ingredientes de recetas.')
        return redirect('receta_lista')

    ingrediente = get_object_or_404(IngredienteReceta, pk=pk)
    ingrediente.delete()
    messages.success(request, "Ingrediente eliminado correctamente.")
    return redirect('receta_lista')


# IMPRIMIR FACTURAS
def exportar_factura_pdf(request, pk):
    pedido = get_object_or_404(Pedido, idPedido=pk)

    if pedido.usuario != request.user and not request.user.is_staff:
        return HttpResponse("No tienes permiso para ver esta factura.", status=403)
    
    if request.user.tipo_usuario != 'B2B' and not request.user.is_staff:
        return HttpResponse("Las facturas en PDF solo están disponibles para clientes B2B.", status=403)
    
    template = get_template('app/factura_pdf.html')

    lineas_de_este_pedido = pedido.lineas_pedido.all()

    contexto = {
        'pedido': pedido,
        'lineas': lineas_de_este_pedido,
        'empresa': {
            'nombre': 'Frutos Secos San Blas S.L.',
            'cif': 'B-12345678',
            'direccion': 'Calle Nuez, 67, Montequinto, Sevilla',
            'email': 'administracion@sanblas.com',
        }
    }

    html = template.render(contexto)
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename="Factura_SanBlas_{pedido.idPedido}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar la factura PDF", status=500)
    
    return response


# Agregar saldo
@login_required
def agregar_saldo(request):
    if request.method == 'POST':
        form = AgregarSaldoForm(request.POST)
        if form.is_valid():
            try: 
                usuario = request.user
                cantidad_a_agregar = form.cleaned_data['cantidad']
                usuario.saldo += cantidad_a_agregar
                usuario.save()

                messages.success(request, f'Se han agregado {cantidad_a_agregar}€ a tu saldo. Saldo actual: {usuario.saldo}€')
                return redirect('inicio')
            except Exception as e:
                messages.error(request, 'Ocurrió un error al agregar saldo. Inténtalo de nuevo.')
                return redirect('inicio')
    else:
        form = AgregarSaldoForm()

    return render(request, 'app/agregar_saldo.html', {'form': form})


# URL panel de admin
def panel_admin(request):
    if not request.user.is_staff:
        return HttpResponse("No tienes permiso para acceder a esta página.", status=403)
    
    return render(request, 'app/panel_admin.html')