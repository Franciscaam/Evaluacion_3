from django.db import models

class Producto(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ecommerce_producto'

class Contacto(models.Model):
    TIPO_MENSAJE_CHOICES = [
        ('RECLAMO', 'Reclamo'),
        ('SUGERENCIA', 'Sugerencia'),
        ('FELICITACION', 'Felicitación'),
    ]

    nombres = models.CharField(max_length=180)
    apellido_paterno = models.CharField(max_length=180)
    apellido_materno = models.CharField(max_length=180)
    email = models.EmailField()
    tipo_mensaje = models.CharField(max_length=15, choices=TIPO_MENSAJE_CHOICES, default='RECLAMO')
    mensaje = models.TextField()

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} - {self.tipo_mensaje}"

    class Meta:
        db_table = 'ecommerce_contacto'

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user} - {self.product}'

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
