from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    index, funkopop, contacto, ruleta, contacto_gracias, agregar_al_carrito,
    ver_carrito, actualizar_carrito, eliminar_del_carrito, login_view, logout_view,
    password_reset_view, password_reset_confirm, iniciar_pago, confirmar_pago, resultado_pago,
    custom_admin_page, manage_products, register_view,
    manage_categoria, update_categoria, delete_categoria,
    manage_proveedor, update_proveedor, delete_proveedor
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('funkopop/', funkopop, name='funkopop'),
    path('contacto/', contacto, name='contacto'),
    path('ruleta/', ruleta, name='ruleta'),
    path('contacto_gracias/', contacto_gracias, name='contacto_gracias'),
    path('agregar_al_carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('actualizar_carrito/', actualizar_carrito, name='actualizar_carrito'),
    path('eliminar_del_carrito/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_confirm/<int:user_id>/', password_reset_confirm, name='password_reset_confirm'),
    path('pago/', iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),
    path('resultado_pago/', resultado_pago, name='resultado_pago'),
    path('custom-admin/', custom_admin_page, name='custom_admin_page'),
    path('custom-admin/manage_products/', manage_products, name='manage_products'),
    path('custom-admin/manage_categoria/', manage_categoria, name='manage_categoria'),
    path('custom-admin/update_categoria/<int:pk>/', update_categoria, name='update_categoria'),
    path('custom-admin/delete_categoria/<int:pk>/', delete_categoria, name='delete_categoria'),
    path('custom-admin/manage_proveedor/', manage_proveedor, name='manage_proveedor'),
    path('custom-admin/update_proveedor/<int:pk>/', update_proveedor, name='update_proveedor'),
    path('custom-admin/delete_proveedor/<int:pk>/', delete_proveedor, name='delete_proveedor'),
    path('register/', register_view, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
