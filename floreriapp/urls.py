from django.urls import path
from . import views

urlpatterns = [
    # ------------------ Principal / Autenticación ----------------------
    path('', views.login_pagina, name='login'),
    path('panel/', views.inicio, name='inicio'),
    
    # ------------------Flores----------------------
    path('flores/', views.listar_flores, name='listar_flores'),
    path('flores/crear/', views.crear_flor, name='crear_flor'),
    path('flores/<int:flor_id>/', views.detalle_flor, name='detalle_flor'),
    path('flores/<int:flor_id>/editar/', views.editar_flor, name='editar_flor'),
    path('flores/<int:flor_id>/eliminar/', views.eliminar_flor, name='eliminar_flor'),

    # ------------------Clientes----------------------
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),

    # ------------------Pedidos----------------------
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/<int:pedido_id>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),

    # ------------------Detalles de Pedido----------------------
    path('detalles/', views.listar_detalles, name='listar_detalles'),
    path('detalles/crear/', views.crear_detalle, name='crear_detalle'),
    path('detalles/<int:detalle_id>/eliminar/', views.eliminar_detalle, name='eliminar_detalle'),

    # --------------------
    # ----- API REST -----
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    
    # API Flores
    path('api/flores/', views.FlorApiView.as_view(), name='api_flores_lista'),
    path('api/flores/<int:id>/', views.FlorDetalleApiView.as_view(), name='api_flor_detalle'),

    # API Clientes
    path('api/clientes/', views.ClienteApiView.as_view(), name='api_clientes_lista'),
    path('api/clientes/<int:id>/', views.ClienteDetalleApiView.as_view(), name='api_cliente_detalle'),

    # API Pedidos
    path('api/pedidos/', views.PedidoApiView.as_view(), name='api_pedidos_lista'),
    path('api/pedidos/<int:id>/', views.PedidoDetalleApiView.as_view(), name='api_pedido_detalle'),

    # API Detalles de Pedido
    path('api/detalles/', views.DetallePedidoApiView.as_view(), name='api_detalles_lista'),
    path('api/detalles/<int:id>/', views.DetallePedidoDetalleApiView.as_view(), name='api_detalle_detalle'),
]