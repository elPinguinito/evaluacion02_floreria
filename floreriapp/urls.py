from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # -----------------------------------------------------------
    # FLORES
    # -----------------------------------------------------------
    path('flores/', views.listar_flores, name='listar_flores'),
    path('flores/crear/', views.crear_flor, name='crear_flor'),
    path('flores/<int:flor_id>/', views.detalle_flor, name='detalle_flor'),
    path('flores/<int:flor_id>/editar/', views.editar_flor, name='editar_flor'),
    path('flores/<int:flor_id>/eliminar/', views.eliminar_flor, name='eliminar_flor'),

    # -----------------------------------------------------------
    # CLIENTE
    # -----------------------------------------------------------
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),

    # -----------------------------------------------------------
    # PEDIDO
    # -----------------------------------------------------------
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/<int:pedido_id>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),

    # -----------------------------------------------------------
    # DETALLE PEDIDO
    # -----------------------------------------------------------
    path('detalles/', views.listar_detalles, name='listar_detalles'),
    path('detalles/crear/', views.crear_detalle, name='crear_detalle'),
    path('detalles/<int:detalle_id>/eliminar/', views.eliminar_detalle, name='eliminar_detalle'),
]