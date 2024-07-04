from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Producto, Contacto, Categoria, Proveedor, Cart
from .forms import ProductoForm, CategoriaForm, ProveedorForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
import transbank.webpay.webpay_plus.transaction as webpay_plus

# Configuración de Webpay Plus
webpay_plus.Transaction.commerce_code = '597055555532'
webpay_plus.Transaction.api_key = '597055555532'
webpay_plus.Transaction.environment = 'INTEGRATION'

def iniciar_pago(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    buy_order = str(request.session.session_key)
    session_id = str(request.session.session_key)
    amount = total
    return_url = request.build_absolute_uri(reverse('confirmar_pago'))

    response = webpay_plus.Transaction.create(buy_order, session_id, amount, return_url)
    return redirect(response['url'] + '?token_ws=' + response['token'])

def confirmar_pago(request):
    token = request.GET.get('token_ws')
    try:
        response = webpay_plus.Transaction.commit(token)
    except Exception as e:
        return render(request, 'error.html', {'message': str(e)})

    if response['status'] == 'AUTHORIZED':
        request.session['cart'] = {}
        return redirect('resultado_pago')
    else:
        return redirect('ver_carrito')

def resultado_pago(request):
    return render(request, 'resultado_pago.html')

# Función de verificación de administrador
def admin_check(user):
    return user.is_superuser  # Verifica si el usuario es un administrador

# Vistas de administración
@login_required
@user_passes_test(admin_check)
def custom_admin_page(request):
    return render(request, 'admin_panel/admin.html')

@login_required
@user_passes_test(admin_check)
def manage_products(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductoForm()
    products = Producto.objects.all()
    return render(request, 'admin_panel/manage_products.html', {'form': form, 'products': products})

@login_required
@user_passes_test(admin_check)
def manage_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categoria')
    else:
        form = CategoriaForm()
    categorias = Categoria.objects.all()
    return render(request, 'admin_panel/manage_categoria.html', {'form': form, 'categorias': categorias})

@login_required
@user_passes_test(admin_check)
def update_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('manage_categoria')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'admin_panel/update_categoria.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def delete_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('manage_categoria')
    return render(request, 'admin_panel/delete_categoria.html', {'categoria': categoria})

@login_required
@user_passes_test(admin_check)
def manage_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_proveedor')
    else:
        form = ProveedorForm()
    proveedores = Proveedor.objects.all()
    return render(request, 'admin_panel/manage_proveedor.html', {'form': form, 'proveedores': proveedores})

@login_required
@user_passes_test(admin_check)
def update_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('manage_proveedor')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'admin_panel/update_proveedor.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def delete_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('manage_proveedor')
    return render(request, 'admin_panel/delete_proveedor.html', {'proveedor': proveedor})

# Vistas de usuarios
def index(request):
    return render(request, 'index.html')

def funkopop(request):
    products = Producto.objects.all()
    return render(request, 'funkopop.html', {'products': products})

def contacto(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        email = request.POST.get('email')
        tipo_mensaje = request.POST.get('tipo_mensaje')
        mensaje = request.POST.get('mensaje')
        Contacto.objects.create(
            nombres=nombres,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            email=email,
            tipo_mensaje=tipo_mensaje,
            mensaje=mensaje
        )
        return redirect('contacto_gracias')
    return render(request, 'contacto.html')

def contacto_gracias(request):
    return render(request, 'contacto_gracias.html')

def ruleta(request):
    return render(request, 'ruleta.html')

# Vistas de carrito
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        product = Producto.objects.get(id=producto_id)
        cart = request.session.get('cart', {})

        if producto_id in cart:
            cart[producto_id]['quantity'] += 1
        else:
            cart[producto_id] = {
                'name': product.name,
                'price': float(product.sale_price),
                'quantity': 1,
                'image': product.image.url
            }

        request.session['cart'] = cart
        return redirect('funkopop')


def ver_carrito(request):
    cart = request.session.get('cart', {})
    carrito_items = []
    total = 0
    for product_id, item in cart.items():
        product = Producto.objects.get(id=product_id)
        total += product.sale_price * item['quantity']
        carrito_items.append({
            'product': product,
            'quantity': item['quantity'],
        })
    return render(request, 'cart.html', {'carrito_items': carrito_items, 'total': total})

def actualizar_carrito(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id]['quantity'] = quantity
            request.session['cart'] = cart

        return redirect('ver_carrito')

def eliminar_del_carrito(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})

        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

        return redirect('ver_carrito')

# Vistas de autenticación y registro
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('custom_admin_page')
            else:
                return redirect('index')
        else:
            return render(request, 'login/login.html', {'error': 'Nombre de usuario o contraseña incorrectos'})
    return render(request, 'login/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'login/register.html')

def logout_view(request):
    auth_logout(request)
    return redirect('index')

# Vistas de recuperación de contraseña
def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            reset_link = reverse('password_reset_confirm', args=[user.id])
            full_link = request.build_absolute_uri(reset_link)
            send_mail(
                'Restablecer contraseña',
                f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {full_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return render(request, 'password_reset_done.html')
    return render(request, 'password_reset.html')

def password_reset_confirm(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        return redirect('login')
    return render(request, 'password_reset_confirm.html', {'user_id': user_id})
