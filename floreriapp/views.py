from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Flor, Cliente, Pedido, DetallePedido

# ----- LOGIN -----
def login_pagina(request):
    return render(request, 'floreriapp/login.html')

# ----- INICIO -----
def inicio(request):
    flores = Flor.objects.all()
    return render(request, 'floreriapp/inicio.html', {'flores': flores})

# ----- FLORES -----
def listar_flores(request):
    flores = Flor.objects.all()
    return render(request, 'floreriapp/listar_flores.html', {'flores': flores})

def crear_flor(request):
    return render(request, 'floreriapp/crear_flor.html')

def detalle_flor(request, flor_id):
    flor = get_object_or_404(Flor, id=flor_id)
    return render(request, 'floreriapp/detalle_flor.html', {'flor': flor}) 

def editar_flor(request, flor_id):
    flor = get_object_or_404(Flor, id=flor_id)
    return render(request, 'floreriapp/editar_flor.html', {'flor': flor})

def eliminar_flor(request, flor_id):
    flor = get_object_or_404(Flor, id=flor_id)
    return render(request, 'floreriapp/eliminar_flor.html', {'flor': flor})


# ----- CLIENTES -----
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'floreriapp/listar_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    return render(request, 'floreriapp/crear_cliente.html')

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'floreriapp/detalle_cliente.html', {'cliente': cliente})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'floreriapp/editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'floreriapp/eliminar_cliente.html', {'cliente': cliente})


# ----- PEDIDOS -----
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'floreriapp/listar_pedidos.html', {'pedidos': pedidos})

def crear_pedido(request):
    clientes = Cliente.objects.all()
    return render(request, 'floreriapp/crear_pedido.html', {'clientes': clientes, 'estados': Pedido.ESTADOS})

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'floreriapp/detalle_pedido.html', {'pedido': pedido})

def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    clientes = Cliente.objects.all()
    return render(request, 'floreriapp/editar_pedido.html', {
        'pedido': pedido,
        'clientes': clientes,
        'estados': Pedido.ESTADOS
    })

def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'floreriapp/eliminar_pedido.html', {'pedido': pedido})


# ----- DETALLES DE PEDIDO -----
def listar_detalles(request):
    detalles = DetallePedido.objects.all()
    return render(request, 'floreriapp/listar_detalles.html', {'detalles': detalles})

def crear_detalle(request):
    pedidos = Pedido.objects.all()
    flores = Flor.objects.all()
    return render(request, 'floreriapp/crear_detalle.html', {'pedidos': pedidos, 'flores': flores})

def eliminar_detalle(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    return render(request, 'floreriapp/eliminar_detalle.html', {'detalle': detalle})


# --------------------
# ----- API REST -----
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            token, creado = Token.objects.get_or_create(user=usuario)
            return Response({
                'mensaje': 'Autenticación correcta',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Usuario o contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)


# ----------------------
# ----- API FLORES -----
class FlorApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        flores = Flor.objects.all()
        datos = []
        for f in flores:
            datos.append({
                'id': f.id,
                'nombre': f.nombre,
                'descripcion': f.descripcion,
                'color': f.color,
                'precio': f.precio,
                'stock': f.stock,
                'disponible': f.disponible
            })
        return Response(datos, status=status.HTTP_200_OK)

    def post(self, request):
        nombre = request.data.get('nombre', '').strip()
        descripcion = request.data.get('descripcion', '').strip()
        color = request.data.get('color', '').strip()
        precio_str = request.data.get('precio', '0')
        stock_str = request.data.get('stock', '0')
        disponible = request.data.get('disponible', True)

        errores = []
        if not nombre or not descripcion or not color:
            errores.append("Todos los campos de texto son obligatorios.")
        
        try:
            precio = int(precio_str)
            if precio <= 0:
                errores.append("El precio debe ser mayor a 0.")
        except ValueError:
            errores.append("El precio debe ser un número válido.")

        try:
            stock = int(stock_str)
            if stock < 0:
                errores.append("El stock no puede ser negativo.")
        except ValueError:
            errores.append("El stock debe ser un número entero.")

        if errores:
            return Response({'errores': errores}, status=status.HTTP_400_BAD_REQUEST)

        flor = Flor.objects.create(
            nombre=nombre, descripcion=descripcion, color=color,
            precio=precio, stock=stock, disponible=disponible
        )
        return Response({
            'mensaje': 'Flor creada correctamente',
            'flor': {
                'id': flor.id, 'nombre': flor.nombre, 'descripcion': flor.descripcion,
                'color': flor.color, 'precio': flor.precio, 'stock': flor.stock, 'disponible': flor.disponible
            }
        }, status=status.HTTP_201_CREATED)


class FlorDetalleApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        flor = get_object_or_404(Flor, id=id)
        return Response({
            'id': flor.id, 'nombre': flor.nombre, 'descripcion': flor.descripcion,
            'color': flor.color, 'precio': flor.precio, 'stock': flor.stock, 'disponible': flor.disponible
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        flor = get_object_or_404(Flor, id=id)
        flor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        flor = get_object_or_404(Flor, id=id)
        nombre = request.data.get('nombre', '').strip()
        descripcion = request.data.get('descripcion', '').strip()
        color = request.data.get('color', '').strip()
        precio_str = request.data.get('precio', '0')
        stock_str = request.data.get('stock', '0')
        disponible = request.data.get('disponible')

        errores = []
        if not nombre or not descripcion or not color or disponible is None:
            errores.append("Todos los campos son obligatorios.")

        try:
            precio = int(precio_str)
            if precio <= 0:
                errores.append("El precio debe ser mayor a 0.")
        except ValueError:
            errores.append("El precio debe ser un número válido.")

        try:
            stock = int(stock_str)
            if stock < 0:
                errores.append("El stock no puede ser negativo.")
        except ValueError:
            errores.append("El stock debe ser un número entero.")

        if errores:
            return Response({'errores': errores}, status=status.HTTP_400_BAD_REQUEST)

        flor.nombre = nombre
        flor.descripcion = descripcion
        flor.color = color
        flor.precio = precio
        flor.stock = stock
        flor.disponible = disponible
        flor.save()

        return Response({'mensaje': 'Flor actualizada correctamente'}, status=status.HTTP_200_OK)


# ------------------------
# ----- API CLIENTES -----
class ClienteApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clientes = Cliente.objects.all()
        datos = []
        for c in clientes:
            datos.append({
                'id': c.id,
                'nombre': c.nombre,
                'email': c.email,
                'telefono': c.telefono,
                'direccion': c.direccion
            })
        return Response(datos, status=status.HTTP_200_OK)

    def post(self, request):
        nombre = request.data.get('nombre', '').strip()
        email = request.data.get('email', '').strip()
        telefono = request.data.get('telefono', '').strip()
        direccion = request.data.get('direccion', '').strip()

        errores = []
        if not nombre or not email or not telefono or not direccion:
            errores.append("Todos los campos del cliente son obligatorios.")
        if "@" not in email or "." not in email:
            errores.append("Debe ingresar un correo electrónico válido.")

        if errores:
            return Response({'errores': errores}, status=status.HTTP_400_BAD_REQUEST)

        cliente = Cliente.objects.create(nombre=nombre, email=email, telefono=telefono, direccion=direccion)
        return Response({
            'mensaje': 'Cliente creado correctamente',
            'cliente': {'id': cliente.id, 'nombre': cliente.nombre, 'email': cliente.email, 'telefono': cliente.telefono, 'direccion': cliente.direccion}
        }, status=status.HTTP_201_CREATED)


class ClienteDetalleApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        c = get_object_or_404(Cliente, id=id)
        return Response({'id': c.id, 'nombre': c.nombre, 'email': c.email, 'telefono': c.telefono, 'direccion': c.direccion}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        c = get_object_or_404(Cliente, id=id)
        c.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        c = get_object_or_404(Cliente, id=id)
        nombre = request.data.get('nombre', '').strip()
        email = request.data.get('email', '').strip()
        telefono = request.data.get('telefono', '').strip()
        direccion = request.data.get('direccion', '').strip()

        errores = []
        if not nombre or not email or not telefono or not direccion:
            errores.append("Todos los campos son obligatorios.")
        if "@" not in email or "." not in email:
            errores.append("Ingrese un correo válido.")

        if errores:
            return Response({'errores': errores}, status=status.HTTP_400_BAD_REQUEST)

        c.nombre = nombre
        c.email = email
        c.telefono = telefono
        c.direccion = direccion
        c.save()
        return Response({'mensaje': 'Cliente actualizado correctamente'}, status=status.HTTP_200_OK)


# -----------------------
# ----- API PEDIDOS -----
class PedidoApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pedidos = Pedido.objects.all()
        datos = []
        for p in pedidos:
            datos.append({
                'id': p.id,
                'cliente_id': p.cliente.id,
                'cliente_nombre': p.cliente.nombre,
                'fecha_pedido': p.fecha_pedido,
                'direccion_entrega': p.direccion_entrega,
                'estado': p.estado,
                'total': p.total
            })
        return Response(datos, status=status.HTTP_200_OK)

    def post(self, request):
        cliente_id = request.data.get('cliente_id')
        fecha_pedido = request.data.get('fecha_pedido')
        direccion_entrega = request.data.get('direccion_entrega', '').strip()
        estado = request.data.get('estado', 'Pendiente')
        total = request.data.get('total', 0)

        if not cliente_id or not fecha_pedido or not direccion_entrega:
            return Response({'error': 'Faltan campos obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        cliente = get_object_or_404(Cliente, id=cliente_id)
        pedido = Pedido.objects.create(
            cliente=cliente, fecha_pedido=fecha_pedido,
            direccion_entrega=direccion_entrega, estado=estado, total=total
        )
        return Response({'mensaje': 'Pedido creado correctamente', 'id': pedido.id}, status=status.HTTP_201_CREATED)


class PedidoDetalleApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        p = get_object_or_404(Pedido, id=id)
        return Response({
            'id': p.id,
            'cliente_id': p.cliente.id,
            'fecha_pedido': p.fecha_pedido,
            'direccion_entrega': p.direccion_entrega,
            'estado': p.estado,
            'total': p.total
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        p = get_object_or_404(Pedido, id=id)
        p.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        p = get_object_or_404(Pedido, id=id)
        cliente_id = request.data.get('cliente_id')
        fecha_pedido = request.data.get('fecha_pedido')
        direccion_entrega = request.data.get('direccion_entrega')
        estado = request.data.get('estado')
        total = request.data.get('total')

        if not cliente_id or not fecha_pedido or not direccion_entrega or not estado or total is None:
            return Response({'error': 'Debes enviar todos los campos'}, status=status.HTTP_400_BAD_REQUEST)

        p.cliente = get_object_or_404(Cliente, id=cliente_id)
        p.fecha_pedido = fecha_pedido
        p.direccion_entrega = direccion_entrega
        p.estado = estado
        p.total = total
        p.save()
        return Response({'mensaje': 'Pedido actualizado correctamente'}, status=status.HTTP_200_OK)


# ----------------------------------
# ----- API DETALLES DE PEDIDO -----
class DetallePedidoApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        detalles = DetallePedido.objects.all()
        datos = []
        for d in detalles:
            datos.append({
                'id': d.id,
                'pedido_id': d.pedido.id,
                'flor_id': d.flor.id,
                'flor_nombre': d.flor.nombre,
                'cantidad': d.cantidad,
                'precio_unitario': d.precio_unitario
            })
        return Response(datos, status=status.HTTP_200_OK)

    def post(self, request):
        pedido_id = request.data.get('pedido_id')
        flor_id = request.data.get('flor_id')
        cantidad = request.data.get('cantidad', 1)
        precio_unitario = request.data.get('precio_unitario', 0)

        if not pedido_id or not flor_id:
            return Response({'error': 'Se requiere pedido_id y flor_id'}, status=status.HTTP_400_BAD_REQUEST)

        pedido = get_object_or_404(Pedido, id=pedido_id)
        flor = get_object_or_404(Flor, id=flor_id)

        detalle = DetallePedido.objects.create(
            pedido=pedido, flor=flor, cantidad=cantidad, precio_unitario=precio_unitario
        )
        return Response({'mensaje': 'Detalle registrado', 'id': detalle.id}, status=status.HTTP_201_CREATED)


class DetallePedidoDetalleApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        d = get_object_or_404(DetallePedido, id=id)
        return Response({
            'id': d.id, 'pedido_id': d.pedido.id, 'flor_id': d.flor.id,
            'cantidad': d.cantidad, 'precio_unitario': d.precio_unitario
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        d = get_object_or_404(DetallePedido, id=id)
        d.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        d = get_object_or_404(DetallePedido, id=id)
        pedido_id = request.data.get('pedido_id')
        flor_id = request.data.get('flor_id')
        cantidad = request.data.get('cantidad')
        precio_unitario = request.data.get('precio_unitario')

        if not pedido_id or not flor_id or cantidad is None or precio_unitario is None:
            return Response({'error': 'Debes enviar todos los campos'}, status=status.HTTP_400_BAD_REQUEST)

        d.pedido = get_object_or_404(Pedido, id=pedido_id)
        d.flor = get_object_or_404(Flor, id=flor_id)
        d.cantidad = cantidad
        d.precio_unitario = precio_unitario
        d.save()
        return Response({'mensaje': 'Detalle actualizado correctamente'}, status=status.HTTP_200_OK)