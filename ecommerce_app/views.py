from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, CartItem
from .forms import ProductForm, SearchForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Product List & Search
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.all()

# Product Detail
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

# Add to Cart
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.stock < 1:
        messages.warning(request, "Out of Stock!")
        return redirect('product-detail', pk=pk)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "Item added to cart!")
    return redirect('product-detail', pk=pk)

# Remove from Cart
@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('cart')

# Cart View
@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

# Checkout
@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    for item in items:
        product = item.product
        product.stock -= item.quantity
        product.save()
    items.delete()
    messages.success(request, "Checkout successful!")
    return redirect('product-list')

# Signup
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('product-list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
