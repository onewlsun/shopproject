from django.shortcuts import render
from .models import Order

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/my_orders.html', {'orders': orders})