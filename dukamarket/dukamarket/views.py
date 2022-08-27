


from unicodedata import category
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from app.models import Slider, Banner_area, Main_Category, Product, Category, Sub_Category




def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = Banner_area.objects.all().order_by('-id')[0:3]


    main_category = Main_Category.objects.all()
    product = Product.objects.all().filter(section__name="Top Deals Of The Day")


    context = {
        'sliders':sliders,
        'banners':banners, 
        'main_category':main_category,
        'product':product,

    }

    return render(request, 'Main/home.html', context)


# Product detail
def PRODUCT_DETAILS(request, slug):
    product = Product.objects.all().filter(slug=slug)
    if product.exists():
        product = Product.objects.all().get(slug=slug)
    else:
        return redirect('404')

    context = {
        'product':product,

    }
    return render(request, 'product/product_detail.html', context)

# ERRORS PAGE 404
def Error404(request):
    return render(request, 'errors/404.html')


# MY ACCOUNT page
def MY_ACCOUNT(request):
    return render(request, 'account/my-account.html')

# Register page
def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


# user existe
        if User.objects.all().filter(username = username).exists():
            messages.error(request, 'username is already exists')
            return redirect('login')

        if User.objects.all().filter(email = email).exists():
            messages.error(request, 'email is already exists')
            return redirect('login')


        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')


# LOGIN PAGE
def LOGIN(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email and Password are invalid !')
            return redirect('login')
    

# MY profil page
@login_required(login_url='/accounts/login/')
def PROFILE(request):
    return render(request, 'profile/profile.html')


# MY profil update page
@login_required(login_url='/accounts/login/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id


        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email


        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile Are Successfully Updated !')
        return redirect('profile')



# About page
def ABOUT(request):
    return render(request, 'Main/about.html')




#  Contact Page
def CONTACT(request):
    return render(request, 'Main/contact.html')




# product page
def PRODUCT(request):
    product = Product.objects.all()
    category = Category.objects.all()
  

    context = {

        'product':product,
        'category':category,
        #'filter_price':filter_price,
        #'color':color,
        #'size':size,
        #'brand':brand
    }

    return render(request, 'product/product.html', context)




#  Product Page
def PRODUCT(request):
    category = Category.objects.all()
    product = Product.objects.all()

    context = {
        'category':category,
        'product':product,
    }
    return render(request, 'product/product.html', context)


# Filter page
def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')


    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()


    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})