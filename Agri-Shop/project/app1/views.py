from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
import os
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home.html', {"user": None})


def register(request):
    if request.method == 'POST':
        print(request.POST['name'])
        print(request.POST['role'])
        try:
            user = User.objects.get(username=request.POST['username'])
            print(user)
            return render(request, 'signup.html')
        except User.DoesNotExist:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            if request.POST['role'] == 'farmer':
                new = Farmer(user=user, phone=request.POST['phone'], dob='2001-01-12', nationality='blank')
                new.save()
                print("Created new Farmer:", new)

                return render(request, 'signup.html')
            else:
                new = Client(user=user, phone=request.POST['phone'])
                new.save()
                print("Created new Client:", new)
                return render(request, 'signup.html')

            print('Registered Successfully')
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html', {'user': None})


def login(request):
    if request.method == 'POST':
        try:
            # Check User in DB
            uname = request.POST['username']
            pwd = request.POST['password']
            user_authenticate = auth.authenticate(username=uname, password=pwd)
            if user_authenticate is not None:
                user = User.objects.get(username=uname)
                try:
                    data = Client.objects.get(user=user)
                    auth.login(request, user_authenticate)
                    print('Client has been logged')
                    return redirect('dashboard', user="C")

                except:
                    try:
                        data = Farmer.objects.get(user=user)
                        auth.login(request, user_authenticate)
                        print('Farmer has been logged')
                        return redirect('dashboard', user="F")

                    except:
                        print('error')
                        return redirect('/')

            else:
                print('Login Failed')
                return render(request, 'login.html')
        except:
            return render(request, 'login.html', {'user': None})
    return render(request, 'login.html', {'user': None})


# Logout
def logout(request):
    auth.logout(request)
    print('Logout')
    return redirect('/login')


def about(request):
    return render(request, 'about.html', {'user': None})


def products(request, user):
    return render(request, 'products.html', {"user": user})


def orders(request, user):
    orders_data = Order.objects.all()
    return render(request, 'orders.html', {'user': user, 'orders_data': orders_data})


def dashboard(request, user):
    status = False
    if request.user:
        status = request.user
    if user == "AnonymousUser":
        return redirect('home')
    if user == 'F':
        farmer = Farmer.objects.get(user=request.user)
        products = Product.objects.filter(farmer=farmer)
        print(products)
        user_name = request.user
        return render(request, 'dashboard_farmer.html', {'user': user, 'status': status, 'products': products, 'user_name': user_name })
    else:
        products_data = Product.objects.all()
        print(products_data)
        print('the image is:')
        image_paths = []
        image_names = []
        for product in products_data:
            image_paths.append(product.image.path)
            image_names.append(os.path.basename(product.image.path))
            # print(product.image.url)
        print(image_names)
        print('img length')
        print(len(image_names))
        print('prd length')
        print(len(products_data))
        zip_data = zip(products_data, image_names)
        for p, i in zip_data:
            print('p')
            print(p.name)
            print('i')
            print(i)
        return render(request, 'dashboard_client.html',
                      {'user': user, 'status': status, 'products_data': products_data, 'image_names': image_names,
                       'zip_data': zip_data})


# Logout
def logout(request):
    auth.logout(request)
    print('Logout')
    return redirect('/')


@login_required
def create_order(request, user):
    print("create_order Entered")
    print("Before POST")
    print(user)
    if request.method == 'POST':
        print("POST Entered")
        # Get the product and quantity from the form data
        product_id = request.GET.get('product_id')
        quantity = request.POST['quantity']
        payment_type = request.POST['payment_type']

        # Get the product instance from the database
        product = Product.objects.get(id=product_id)

        client = Client.objects.get(user=request.user)

        # Create a new order item and save it to the database
        order = Order.objects.create(client=client, payment_type=payment_type)
        print("Order create 1 completed")
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
        )
        print("OrderItem create 1 completed")

        # Save the order to the database
        order.save()
        print('order saved')
        order_item.save()
        print('orderItem saved')
        print(user)
        # Redirect the user to their cart
        return redirect('dashboard', user=user)
        # return render(request, 'dashboard_client.html', {'user': user})

    # If the request method is not POST, render the create order form
    products_data = Product.objects.all()
    return render(request, 'create_order.html', {'user': user, "products_data": products_data})


##########################################3

def add_product(request, user):
    print("add_product Entered")
    if request.method == 'POST':
        farmer = Farmer.objects.get(user=request.user)
        name = request.POST['name']
        unit_price = request.POST['unit_price']
        quantity_in_stock = request.POST['quantity_in_stock']
        category = request.POST['category']
        description = request.POST['description']
        if 'image' in request.FILES:
            # There is an uploaded file
            print('There is an uploaded file')
        else:
            # No file uploaded
            print('No file uploaded')
        if request.FILES.get('image'):
            print('image request Entered')
            image = request.FILES['image']
        else:
            image = None
        new_product = Product.objects.create(name=name, unit_price=unit_price, quantity_in_stock=quantity_in_stock,
                                             category=category, description=description, farmer=farmer, image=image)
        new_product.save()
        return redirect('dashboard', user=user)

    else:
        return render(request, 'add_product.html', {'user': user})


@login_required
def delete_product(request, product_id):
    farmer = Farmer.objects.get(user=request.user)
    product = Product.objects.get(id=product_id, farmer=farmer)
    # Get the image path for the product and delete the image file
    image_path = product.image.path
    if os.path.exists(image_path):
        os.remove(image_path)
    product.delete()
    return redirect('dashboard', user='F')


@login_required
def edit_product(request, product_id):
    print("edit_product Entered")
    if request.method == 'POST':
        # farmer = Farmer.objects.get(user=request.user)
        update = Product.objects.get(id=product_id)
        update.name = request.POST['name']
        update.unit_price = request.POST['unit_price']
        update.quantity_in_stock = request.POST['quantity_in_stock']
        update.category = request.POST['category']
        update.description = request.POST['description']
        print('before update image')

        if request.FILES.get('image'):
            print('update image Entered')
            # delete the old image
            image_path = update.image.path
            # If a new image file was uploaded, update the image field
            update.image = request.FILES['image']
            if os.path.exists(image_path):
                os.remove(image_path)
        print('save edite')
        update.save()

        return redirect('dashboard', user="F")

    else:
        product = Product.objects.get(id=product_id)
        return render(request, 'edit_product.html', {'user': "F", 'product': product})


@login_required
def cart(request, user):
    print('done')
    client = Client.objects.get(user=request.user)
    orders = Order.objects.filter(client=client)

    return render(request, 'cart.html', {'orders': orders, 'user': user})
