from django.shortcuts import render, redirect, get_object_or_404
from .models import Flor, Cliente, Pedido, DetallePedido

def inicio(request):
    flores = Flor.objects.all()
    return render(request, 'floreriapp/inicio.html', {
        'flores': flores
    })

#-----------------------------------------------------------
# FLORES
#-----------------------------------------------------------
def listar_flores(request):
    flores = Flor.objects.all()
    return render(request, 'floreriapp/listar_flores.html', {'flores': flores})

def crear_flor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        color = request.POST.get('color', '').strip()
        precio_str = request.POST.get('precio', '0')
        stock_str = request.POST.get('stock', '0')
        disponible = request.POST.get('disponible', False) == 'on'

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
            return render(request, 'floreriapp/crear_flor.html', {'errores': errores})

        Flor.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            color=color,
            precio=precio,
            stock=stock,
            disponible=disponible
        )
        return redirect('listar_flores')
    return render(request, 'floreriapp/crear_flor.html')

def detalle_flor(request, flor_id):
    flor = get_object_or_404(Flor, id=flor_id)
    return render(request, 'floreriapp/detalle_flor.html', {'flor': flor}) 

def editar_flor(request, flor_id):
    flor = get_object_or_404(Flor, id=flor_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        color = request.POST.get('color', '').strip()
        precio_str = request.POST.get('precio', '0')
        stock_str = request.POST.get('stock', '0')
        disponible = request.POST.get('disponible', False) == 'on'

        errores = []
        if not nombre or not descripcion or not color:
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
            return render(request, 'floreriapp/editar_flor.html', {'flor': flor, 'errores': errores})

        flor.nombre = nombre
        flor.descripcion = descripcion
        flor.color = color
        flor.precio = precio
        flor.stock = stock
        flor.disponible = disponible
        flor.save()
        return redirect('listar_flores')
    return render(request, 'floreriapp/editar_flor.html', {'flor': flor})

def eliminar_flor(request, flor_id):
    flor = get_object_or_404(Flor, id=flor_id)
    if request.method == 'POST':
        flor.delete()
        return redirect('listar_flores')
    return render(request, 'floreriapp/eliminar_flor.html', {'flor': flor})

#-----------------------------------------------------------
# CLIENTE
#-----------------------------------------------------------
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'floreriapp/listar_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()

        errores = []
        if not nombre or not email or not telefono or not direccion:
            errores.append("Todos los campos del cliente son obligatorios.")
        if "@" not in email or "." not in email:
            errores.append("Debe ingresar un correo electrónico válido.")

        if errores:
            return render(request, 'floreriapp/crear_cliente.html', {'errores': errores})

        Cliente.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion
        )
        return redirect('listar_clientes')
    return render(request, 'floreriapp/crear_cliente.html')

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'floreriapp/detalle_cliente.html', {'cliente': cliente})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()

        errores = []
        if not nombre or not email or not telefono or not direccion:
            errores.append("Todos los campos son obligatorios.")
        if "@" not in email or "." not in email:
            errores.append("Ingrese un correo válido.")

        if errores:
            return render(request, 'floreriapp/editar_cliente.html', {'cliente': cliente, 'errores': errores})

        cliente.nombre = nombre
        cliente.email = email
        cliente.telefono = telefono
        cliente.direccion = direccion
        cliente.save()
        return redirect('listar_clientes')
    return render(request, 'floreriapp/editar_cliente.html', {'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'floreriapp/eliminar_cliente.html', {'cliente': cliente})

#-----------------------------------------------------------
# PEDIDO
#-----------------------------------------------------------
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'floreriapp/listar_pedidos.html', {'pedidos': pedidos})

def crear_pedido(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        fecha_pedido = request.POST.get('fecha_pedido')
        direccion_entrega = request.POST.get('direccion_entrega', '').strip()
        estado = request.POST.get('estado', 'Pendiente')
        total = request.POST.get('total', 0)

        cliente = get_object_or_404(Cliente, id=cliente_id)

        Pedido.objects.create(
            cliente=cliente,
            fecha_pedido=fecha_pedido,
            direccion_entrega=direccion_entrega,
            estado=estado,
            total=total
        )
        return redirect('listar_pedidos')

    clientes = Cliente.objects.all()
    return render(request, 'floreriapp/crear_pedido.html', {'clientes': clientes, 'estados': Pedido.ESTADOS})

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'floreriapp/detalle_pedido.html', {'pedido': pedido})

def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        pedido.cliente = get_object_or_404(Cliente, id=cliente_id)
        pedido.fecha_pedido = request.POST.get('fecha_pedido')
        pedido.direccion_entrega = request.POST.get('direccion_entrega')
        pedido.estado = request.POST.get('estado')
        pedido.total = request.POST.get('total')
        pedido.save()
        return redirect('listar_pedidos')

    clientes = Cliente.objects.all()
    return render(request, 'floreriapp/editar_pedido.html', {
        'pedido': pedido,
        'clientes': clientes,
        'estados': Pedido.ESTADOS
    })

def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('listar_pedidos')
    return render(request, 'floreriapp/eliminar_pedido.html', {'pedido': pedido})

#-----------------------------------------------------------
# DETALLE PEDIDO
#-----------------------------------------------------------
def listar_detalles(request):
    detalles = DetallePedido.objects.all()
    return render(request, 'floreriapp/listar_detalles.html', {'detalles': detalles})

def crear_detalle(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido')
        flor_id = request.POST.get('flor')
        cantidad = request.POST.get('cantidad', 1)
        precio_unitario = request.POST.get('precio_unitario', 0)

        pedido = get_object_or_404(Pedido, id=pedido_id)
        flor = get_object_or_404(Flor, id=flor_id)

        DetallePedido.objects.create(
            pedido=pedido,
            flor=flor,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        return redirect('listar_detalles')
    pedidos = Pedido.objects.all()
    flores = Flor.objects.all()
    return render(request, 'floreriapp/crear_detalle.html', {'pedidos': pedidos, 'flores': flores})

def eliminar_detalle(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    if request.method == 'POST':
        detalle.delete()
        return redirect('listar_detalles')
    return render(request, 'floreriapp/eliminar_detalle.html', {'detalle': detalle})