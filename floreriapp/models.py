from django.db import models

class Flor(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    color = models.CharField(max_length=50)
    precio = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)


class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Preparación', 'En Preparación'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField()
    direccion_entrega = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    total = models.IntegerField(default=0)


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    flor = models.ForeignKey(Flor, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.IntegerField()