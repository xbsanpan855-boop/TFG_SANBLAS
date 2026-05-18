from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),

    path('registro/', views.registro_view, name='registro'),

    # URLS de categorias
    path('categoria/', views.CategoriaListaView.as_view(), name='categoria_lista'),
    path('categoria/nueva', views.CategoriaNuevaView.as_view(), name='categoria_nueva'),
    path('categoria/editar/<int:pk>/', views.CategoriaEditarView.as_view(), name='categoria_editar'),
    path('categoria/eliminar/<int:pk>/', views.CategoriaEliminarView.as_view(), name='categoria_eliminar'),

    # URLS de productos
    path('producto/', views.ProductoListaView.as_view(), name='producto_lista'),
    path('producto/nuevo/', views.ProductoNuevoView.as_view(), name='producto_nuevo'),
    path('producto/editar/<int:pk>/', views.ProductoEditarView.as_view(), name='producto_editar'),
    path('producto/eliminar/<int:pk>/', views.ProductoEliminarView.as_view(), name='producto_eliminar'),
    path('producto/<int:pk>/', views.ProductoDetalleView.as_view(), name='producto_detalle'),
    
    # URLS de usuarios
    path('usuario/', views.UsuarioListaView.as_view(), name='usuario_lista'),
    path('usuario/nuevo/', views.UsuarioNuevoView.as_view(), name='usuario_nuevo'),
    path('usuario/editar/<int:pk>/', views.UsuarioEditarView.as_view(), name='usuario_editar'),
    path('usuario/eliminar/<int:pk>/', views.UsuarioEliminarView.as_view(), name='usuario_eliminar'),

    # URLS de tarifas
    path('tarifa/', views.TarifaListaView.as_view(), name='tarifa_lista'),
    path('tarifa/nueva/', views.TarifaNuevaView.as_view(), name='tarifa_nueva'),
    path('tarifa/editar/<int:pk>/', views.TarifaEditarView.as_view(), name='tarifa_editar'),
    path('tarifa/eliminar/<int:pk>/', views.TarifaEliminarView.as_view(), name='tarifa_eliminar'),

    # URLS de carrito y compras
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:pk>/', views.agregar_al_carrito, name='agregar_carrito'),
    path('carrito/actualizar/<int:pk>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:pk>/', views.eliminar_del_carrito, name='eliminar_carrito'),
    path('carrito/comprar/', views.procesar_compra, name='procesar_compra'),


    path('pedido/detalle/<str:pk>/', views.pedido_detalle, name='pedido_detalle'),

    # URLS de pedidosas
    path('pedido/', views.PedidoListaView.as_view(), name='pedido_lista'),
    path('pedido/nuevo/', views.PedidoNuevoView.as_view(), name='pedido_nuevo'),
    path('pedido/editar/<str:pk>/', views.pedido_editar, name='pedido_editar'),
    path('pedido/eliminar/<str:pk>/', views.pedido_eliminar, name='pedido_eliminar'),

    path('pedido/propios/', views.ver_mis_pedidos, name='pedido_propios'),


    # URLS de competidores
    path('competidor/', views.CompetidorListaView.as_view(), name='competidor_lista'),
    path('competidor/nuevo/', views.CompetidorNuevoView.as_view(), name='competidor_nuevo'),
    path('competidor/<int:pk>/', views.CompetidorDetalleView.as_view(), name='competidor_detalle'),
    path('competidor/editar/<int:pk>/', views.CompetidorEditarView.as_view(), name='competidor_editar'),
    path('competidor/eliminar/<int:pk>/', views.CompetidorEliminarView.as_view(), name='competidor_eliminar'),

    # URLS productos competidores
    path('producto_competidor/nuevo/', views.ProductoCompetidorNuevoView.as_view(), name='producto_competidor_nuevo'),
    path('producto_competidor/editar/<int:pk>/', views.ProductoCompetidorEditarView.as_view(), name='producto_competidor_editar'),
    path('producto_competidor/eliminar/<int:pk>/', views.producto_competidor_eliminar, name='producto_competidor_eliminar'),

    # URLS de analisis IA
    path('generar-ia/<str:pk>/', views.generar_comparativa_ia, name='generar_comparativa_ia'),


    # URLS de recetas
    path('receta/', views.RecetaListaView.as_view(), name='receta_lista'),
    path('receta/nueva/', views.RecetaNuevaView.as_view(), name='receta_nueva'),
    path('receta/<int:pk>/', views.RecetaDetalleView.as_view(), name='receta_detalle'),
    path('receta/editar/<int:pk>/', views.RecetaEditarView.as_view(), name='receta_editar'),
    path('receta/eliminar/<int:pk>/', views.RecetaEliminarView.as_view(), name='receta_eliminar'),

    path('ingrediente_receta/nuevo/<int:receta_pk>/', views.IngredienteRecetaNuevoView.as_view(), name='ingrediente_receta_nuevo'),
    path('ingrediente_receta/editar/<int:pk>/', views.IngredienteRecetaEditarView.as_view(), name='ingrediente_receta_editar'),
    path('ingrediente_receta/eliminar/<int:pk>/', views.ingrediente_receta_eliminar, name='ingrediente_receta_eliminar'),


    # URLS de facturas
    path('pedido/factura/<str:pk>/pdf/', views.exportar_factura_pdf, name='exportar_factura_pdf'),

    # URLS de saldo
    path('saldo/agregar/', views.agregar_saldo, name='agregar_saldo'),

    # URLS de panel admin
    path('panel/admin/', views.panel_admin, name='panel_admin'),
]
