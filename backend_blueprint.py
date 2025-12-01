"""
This file is a backend blueprint: it contains all Django code in one place
so you can quickly copy-paste into a real Django project structure:

project_root/
├─ manage.py
├─ requirements.txt
├─ .env
├─ db.sqlite3
├─ ecommerce/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  └─ asgi.py
└─ store/
   ├─ __init__.py
   ├─ models.py
   ├─ views.py
   ├─ urls.py
   ├─ forms.py
   ├─ templates/
   │  ├─ base.html
   │  └─ store/
   │     ├─ home.html
   │     ├─ product_detail.html
   │     ├─ cart.html
   │     ├─ checkout.html
   │     └─ orders.html
   ├─ static/
   │  ├─ css/
   │  │  └─ styles.css
   │  ├─ js/
   │  │  └─ app.js
   │  └─ images/
   ├─ admin.py
   └─ tests.py
"""

# =========================
# requirements.txt
# =========================
REQUIREMENTS_TXT = """
Django==4.2
Pillow==10.0.0
python-dotenv==1.0.1
"""

# =========================
# manage.py
# =========================
MANAGE_PY = r"""#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
"""

# =========================
# ecommerce/__init__.py
# =========================
ECOMMERCE_INIT_PY = """# empty file, required by Python package system
"""

# =========================
# ecommerce/settings.py (minimal)
# =========================
ECOMMERCE_SETTINGS_PY = r"""from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-change-me")

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "product_list"
LOGOUT_REDIRECT_URL = "product_list"
"""

# =========================
# ecommerce/urls.py
# =========================
ECOMMERCE_URLS_PY = r"""from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""

# =========================
# ecommerce/wsgi.py
# =========================
ECOMMERCE_WSGI_PY = r"""import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
application = get_wsgi_application()
"""

# =========================
# ecommerce/asgi.py
# =========================
ECOMMERCE_ASGI_PY = r"""import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
application = get_asgi_application()
"""

# =========================
# store/__init__.py
# =========================
STORE_INIT_PY = """# empty init for store app
"""

# =========================
# store/models.py
# =========================
STORE_MODELS_PY = r"""from django.conf import settings
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} for {self.user}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=80)
    country = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    @property
    def total(self):
        return sum(item.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
"""

# =========================
# store/forms.py
# =========================
STORE_FORMS_PY = r"""from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "email", "address", "city", "country"]
"""

# =========================
# store/urls.py
# =========================
STORE_URLS_PY = r"""from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="orders"),

    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="store/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
"""

# =========================
# store/views.py
# =========================
STORE_VIEWS_PY = r"""from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, RegisterForm
from .models import CartItem, Order, OrderItem, Product


def product_list(request):
    query = request.GET.get("q", "")
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
    context = {"products": products, "query": query}
    return render(request, "store/home.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "store/product_detail.html", {"product": product})


@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "store/cart.html", {"items": items, "total": total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, "Added to cart")
    return redirect("cart")


@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(user=request.user, product=product).delete()
    messages.info(request, "Item removed from cart")
    return redirect("cart")


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    if not items.exists():
        messages.error(request, "Your cart is empty")
        return redirect("cart")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

            items.delete()
            messages.success(request, "Order placed successfully")
            return redirect("orders")
    else:
        form = CheckoutForm()

    total = sum(item.product.price * item.quantity for item in items)
    return render(
        request,
        "store/checkout.html",
        {"form": form, "items": items, "total": total},
    )


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "store/orders.html", {"orders": orders})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can now log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "store/register.html", {"form": form})
"""

# =========================
# store/admin.py
# =========================
STORE_ADMIN_PY = r"""from django.contrib import admin

from .models import CartItem, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "created_at")
    prepopulated_fields = {"slug": ("title",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "email", "created_at")
    inlines = [OrderItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "created_at")
"""

# =========================
# templates/base.html
# =========================
TEMPLATE_BASE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}E-Shop{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
<header>
    <nav>
        <a href="{% url 'product_list' %}">Home</a>
        {% if user.is_authenticated %}
            <a href="{% url 'cart' %}">Cart</a>
            <a href="{% url 'orders' %}">My Orders</a>
            <a href="{% url 'logout' %}">Logout</a>
        {% else %}
            <a href="{% url 'login' %}">Login</a>
            <a href="{% url 'register' %}">Register</a>
        {% endif %}
    </nav>
</header>
<main>
    {% block content %}{% endblock %}
</main>
</body>
</html>
"""

# =========================
# QUICK START (how to use this blueprint)
# =========================
QUICK_START = r"""
python -m venv venv
source venv/bin/activate           # Linux/Mac
# venv\Scripts\activate           # Windows
pip install -r requirements.txt

django-admin startproject ecommerce .
python manage.py startapp store

# Replace generated files with content from this blueprint:
# - manage.py                  -> MANAGE_PY
# - ecommerce/settings.py      -> ECOMMERCE_SETTINGS_PY
# - ecommerce/urls.py          -> ECOMMERCE_URLS_PY
# - ecommerce/wsgi.py          -> ECOMMERCE_WSGI_PY
# - ecommerce/asgi.py          -> ECOMMERCE_ASGI_PY
# - store/models.py            -> STORE_MODELS_PY
# - store/forms.py             -> STORE_FORMS_PY
# - store/urls.py              -> STORE_URLS_PY
# - store/views.py             -> STORE_VIEWS_PY
# - store/admin.py             -> STORE_ADMIN_PY
# - templates/base.html        -> TEMPLATE_BASE_HTML

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
"""