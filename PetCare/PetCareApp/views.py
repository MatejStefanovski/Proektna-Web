from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product, CartItem, Veterinarian
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from decimal import Decimal


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def home(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'products': products})

def veterinari(request):
    veterinarians = Veterinarian.objects.all().order_by('-created_at')
    return render(request, 'veterinari.html', {'veterinarians': veterinarians})

def oprema(request):
    products = Product.objects.filter(label='oprema').order_by('-created_at')
    return render(request, 'oprema.html', {'products': products})

def hotel(request):
    return render(request, 'hotel.html')

def igracki(request):
    products = Product.objects.filter(label='igracki').order_by('-created_at')
    return render(request, 'igracki.html', {'products': products})

def milenicinja(request):
    products = Product.objects.filter(label='milenicinja').order_by('-created_at')
    return render(request, 'milenicinja.html', {'products': products})

def hrana(request):
    products = Product.objects.filter(label='hrana').order_by('-created_at')
    return render(request, 'hrana.html', {'products': products})

def nega(request):
    products = Product.objects.filter(label='nega').order_by('-created_at')
    return render(request, 'nega.html', {'products': products})

def dresiranje(request):
    return render(request, 'dresiranje.html')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.subtotal for item in cart_items)
    total_with_shipping = total + Decimal('5.00')

    if not cart_items:
        messages.warning(request, 'Вашата кошничка е празна.')
        return redirect('cart')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'total_with_shipping': total_with_shipping
    })

@login_required
@require_POST
def process_checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, 'Вашата кошничка е празна.')
        return redirect('cart')

    required_fields = ['firstName', 'lastName', 'email', 'address', 'cardNumber', 'expiryDate', 'cvv', 'cardName']
    for field in required_fields:
        if not request.POST.get(field):
            messages.error(request, f'Полето {field} е задолжително.')
            return redirect('checkout')

    card_number = request.POST.get('cardNumber', '').replace(' ', '')
    cvv = request.POST.get('cvv', '')

    if len(card_number) < 13 or len(card_number) > 19:
        messages.error(request, 'Внесете валиден број на картичка.')
        return redirect('checkout')

    if len(cvv) < 3 or len(cvv) > 4:
        messages.error(request, 'Внесете валиден CVV.')
        return redirect('checkout')

    cart_items.delete()

    messages.success(request, 'Вашата нарачка е успешно процесирана!')

    return render(request, 'thank_you.html')

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('home')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = reverse('home')
    return redirect(next_url)

@login_required
@require_POST
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')

@login_required
@require_POST
def remove_all_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')
