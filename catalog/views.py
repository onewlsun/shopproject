from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Category, Product
from django.db.models import Q 
from decimal import Decimal, InvalidOperation

def home(request):
    categories = Category.objects.all()
    return render(request, "catalog/home.html", {"categories": categories})

def category_list(request):
    categories = Category.objects.all()
    return render(request, "catalog/category_list.html", {"categories": categories})

def product_list(request, slug):
    catalog_obj = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(category=catalog_obj, is_active=True).order_by("name")
    qs = qs.select_related("category").prefetch_related("images") 
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    # фильтр цены
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    try:
        if min_price:
            qs = qs.filter(price__gte=Decimal(min_price))
        if max_price:
            qs = qs.filter(price__lte=Decimal(max_price))
    except (InvalidOperation, ValueError):
        pass

    # фильтр наличия
    if request.GET.get("in_stock") == "1":
        qs = qs.filter(stock__gt=0)

    # сортировка
    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "new":
        qs = qs.order_by("-id")
    else:
        qs = qs.order_by("name")


    paginator = Paginator(qs, 8)
    page_obj = paginator.get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)
    qs_params = params.urlencode()

    return render(request, "catalog/product_list.html", {
        "category": catalog_obj,
        "page_obj": page_obj,
        "qs_params": qs_params,
    })


# Корзина
def get_cart(request):
    return request.session.get("cart", {})

def save_cart(request, cart):
    request.session["cart"] = cart
    request.session.modified = True

def add_to_cart(request, product_id):
    from .models import Product
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    product_id = str(product_id)
    quantity = cart.get(product_id, 0)
    if quantity < product.stock:
        cart[product_id] = quantity + 1
    save_cart(request, cart)
    return redirect("catalog:cart_view")

def cart_view(request):
    cart = get_cart(request)
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_sum = 0
    total_quantity = 0
    for product in products:
        quantity = cart[str(product.id)]
        item_total = product.price * quantity
        total_sum += item_total
        total_quantity += quantity
        cart_items.append({"product": product, "quantity": quantity, "total": item_total})
    context = {
        "cart_items": cart_items,
        "total_sum": total_sum,
        "total_quantity": total_quantity,
        "positions": len(cart_items),
    }
    return render(request, "catalog/cart.html", context)



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)
    return render(request, "catalog/product_detail.html", {
        "product": product,
        "products": products
    })


def increase_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    product_id = str(product_id)
    if cart.get(product_id, 0) < product.stock:
        cart[product_id] = cart.get(product_id, 0) + 1
    save_cart(request, cart)
    return redirect("catalog:cart_view")

def decrease_quantity(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            cart.pop(product_id)
    save_cart(request, cart)
    return redirect("catalog:cart_view")

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        cart.pop(product_id)
    save_cart(request, cart)
    return redirect("catalog:cart_view")

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу логи
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from orders.models import Order

@login_required
def profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
    return render(request, "catalog/profile.html")

def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})