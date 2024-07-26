from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem
from django.http import HttpResponse
from django.views.generic import View
from .models import Payment
from .forms import PaymentForm
from django.conf import settings
import stripe


def menu_detail(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)
    context = {
        'menu_item': menu_item
    }
    return render(request, 'menu_detail.html', context)


def menu_list(request):
    menu_items = MenuItem.objects.all()
    context = {
        'menu_items': menu_items
    }
    return render(request, 'menu.html', context)


def add_to_cart(request, menu_item_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        cart = request.session.get('cart', {})

        # Debug: Cart verilerini kontrol et
        print(f"Current cart (before): {cart}, Type: {type(cart)}")

        if isinstance(cart, dict):  # cart'ın sözlük olduğundan emin olun
            if str(menu_item_id) in cart:
                cart[str(menu_item_id)] += 1
            else:
                cart[str(menu_item_id)] = 1

            request.session['cart'] = cart
        else:
            # Eğer cart bir sözlük değilse, bunu düzeltin
            request.session['cart'] = {str(menu_item_id): 1}

        # Debug: Güncellenmiş cart'ı kontrol et
        print(f"Updated cart: {request.session['cart']}")

        return redirect('cart')
    return HttpResponse("Invalid request", status=400)

def remove_from_cart(request, menu_item_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        if str(menu_item_id) in cart:
            if cart[str(menu_item_id)] > 1:
                cart[str(menu_item_id)] -= 1
            else:
                del cart[str(menu_item_id)]

        request.session['cart'] = cart
        return redirect('cart')
    return HttpResponse("Invalid request")


def cart(request):
    cart = request.session.get('cart', {})
    
    # Debug: Cart verilerini kontrol et
    print(f"Cart from session: {cart}, Type: {type(cart)}")

    if not isinstance(cart, dict):
        # Eğer cart bir sözlük değilse, bunu düzeltin
        cart = {}
    
    menu_items = MenuItem.objects.filter(id__in=cart.keys())
    cart_items = []
    
    for menu_item in menu_items:
        quantity = cart.get(str(menu_item.id), 0)  # Varsayılan değeri 0 olarak ayarladık
        cart_items.append({
            'menu_item': menu_item,
            'quantity': quantity
        })
    
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)





stripe.api_key = settings.STRIPE_SECRET_KEY



class PaymentView(View):
    def get(self, request, *args, **kwargs):
        form = PaymentForm()
        return render(request, 'payment.html', {'form': form, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})

    def post(self, request, *args, **kwargs):
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                token = form.cleaned_data.get('stripeToken')
                amount = form.cleaned_data.get('amount')

                charge = stripe.Charge.create(
                    amount=int(amount * 100),  # Amount in cents
                    currency='usd',
                    source=token,
                    description='Example charge',
                )

                # Save payment to database
                payment = Payment.objects.create(
                    stripe_charge_id=charge['id'],
                    amount=amount
                )

                return redirect('payment_success')
            except stripe.error.CardError as e:
                return redirect('payment_error')

        return render(request, 'payment.html', {'form': form, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})