from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect, HttpResponse
from accounts.models import Profile, Cart, CartItems
from products.models import Product, SizeVariant


# Create your views here.
def login_page(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)
        
        if not user_obj.exists():
            messages.warning(request, "This email is not registered")
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your Account is not verified")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request,user_obj)
            return redirect('/')
        
        messages.warning(request, "Incorrect password")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/login.html')

def register_page(request):
    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)
        if user_obj.exists():
            messages.warning(request, "Email is already taken.")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.info(request, "An Email is sent on your mail.")
        return HttpResponseRedirect(request.path_info)


    return render(request, 'accounts/register.html')


def activate_email(request,email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    

def add_to_cart(request, uid):
    variant = request.GET.get('variant')
        
    product = Product.objects.get(uid = uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user = user, is_paid =False) 

    cart_items = CartItems.objects.create(cart = cart, product = product, )
    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_items.size_variant = size_variant
        cart_items.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def cart(request):
    cart = Cart.objects.filter(is_paid=False, user=request.user).first()
    cart_items = cart.cart_items.all() if cart else []
    return render(request, 'accounts/cart.html', {'cart': cart, 'cart_items': cart_items})

# def cart(request):
#     context  = {'cart': Cart.objects.filter(is_paid = False, user = request.user)}
#     return render(request,'accounts/cart.html', context)

