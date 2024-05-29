from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Customer,CartItem,PaymentandShipping2,Address
from .forms import RegistrationForm,CheckoutForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

def home(request):

  return render(request,"home.html")
def toys(request):
  productlist=Product.objects.all()
  return render(request,"toys.html",{"productlist":productlist})
def register(request):
    global form
    if request.method == 'POST':
        try:

            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()

                # Create UserProfile associated with the new user
                user_profile=Customer.objects.create(user=user)
                user_profile.save()
                # Additional logic as needed
                return redirect('login')
            else:
                print(form.errors)
        except Exception as e:
            print(f"Exception: {e}")
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            # Handle case where product does not exist
            return redirect('toys')  # Redirect to toys page or handle as appropriate
        
        # Get the current customer
        customer = request.user.customer
        
        # Check if the product is already in the cart
        try:
            cart_item = CartItem.objects.get(customer=customer, product=product)
            # If the product is already in the cart, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            # If the product is not in the cart, create a new cart item
            CartItem.objects.create(customer=customer, product=product)
        
        return redirect('toys')
    else:
        return redirect('home')  # Redirect to home page or handle as appropriate
def cart(request):
    
    cart_items = request.user.customer.cart.all()
    total_cost = sum(cart_item.product.price for cart_item in cart_items)

    return render(request,"cart.html")
def user_profile(request):
    return render(request,"home.html")
@login_required
@transaction.atomic
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            postcode = form.cleaned_data['postcode']
            cardNumber = form.cleaned_data['cardNumber']
            
            # Get the customer's cart items
            cart_items = request.user.customer.cart.all()

            # Check if items are in stock
            for cart_item in cart_items:
                if cart_item.product.stock < cart_item.quantity:
                    messages.error(request, f"Not enough stock for {cart_item.product.name}.")
                    return redirect('cart')  # Redirect to cart if stock is insufficient

            # Calculate total price
            total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
            item_details="" 
            # Create a dictionary for product names and quantities
            for cart_item in cart_items:
                item_details+="Item name:"+cart_item.product.name+"Item Quantity"+str(cart_item.quantity)+"Item price"+str(cart_item.product.price)+"."

            try:
                # Create payment and shipping object
                payment_shipping = PaymentandShipping2.objects.create(
                    customer=request.user.customer,
                    state=state,
                    city=city,
                    street=street,
                    postcode=postcode,
                    cardNumber=cardNumber,
                    total_price=total_price,
                    item_details=item_details  # Store the dictionary here
                )

                # Decrease the product stock
                for cart_item in cart_items:
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()

                # Clear the cart
                cart_items.delete()

                messages.success(request, "Purchase successful. Your order has been placed.")
                return redirect('home')  # Redirect to a success page or home page
            except Exception as e:
                transaction.set_rollback(True)
                messages.error(request, "An error occurred during checkout. Please try again.")
                return redirect('cart')  # Redirect to cart on failure
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})
    

def update_cart(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
            new_quantity = int(request.POST['quantity'])
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                cart_item.delete()  # Remove item if quantity is zero or less
            # Optionally add a success message
        except (CartItem.DoesNotExist, ValueError):
            # Handle case where item is not found or invalid quantity
            pass
    return redirect('cart')  # Redirect back to the cart page after updating
def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
            cart_item.delete()
            # Optionally add a success message
        except CartItem.DoesNotExist:
            # Handle case where item is not found
            pass
    return redirect('cart')  # Redirect back to the cart page after removal
def order_history(request):
    # Retrieve orders for the current user
    orders = PaymentandShipping2.objects.filter(customer__user=request.user)

    return render(request, 'order_history.html', {'orders': orders})