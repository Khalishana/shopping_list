from django.shortcuts import render
from django.http import HttpResponseRedirect
from main.forms import ProductForm
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm #buat form pendaftaran
from django.contrib import messages
from django.contrib.auth import authenticate, login  
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required #buat ngeharusin user masuk pake login
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from main.models import Product

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    #products = Product.objects.all() #buat ngambil semua object product yang disimpen di database
    products = Product.objects.filter(user=request.user)

    context = {
        #'name': 'Khalisha Hana',
        'name': request.user.username, #biar nama user sesuai sm nama username
        'class': 'PBP A',
        'products': products,
        'last_login': request.COOKIES['last_login'], #nambahin informasi last login di web
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        #form.save()
        product = form.save(commit=False) #biar ga langsung nyimpen objek ke database
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) #membuat respons direct ke halaman yg ada nama + kelas
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
            #return redirect('main:show_main')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request) #buat ngehapus sesi pengguna yg udh masuk
    response = HttpResponseRedirect(reverse('main:login')) #buat respons balik ke halaman login
    response.delete_cookie('last_login') #cookie last login dihapus pas user logout
    return response
    #return redirect('main:login') #ngarahin ke halaman login

def edit_product(request, id):
    # Get product berdasarkan ID
    product = Product.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    # Get data berdasarkan ID
    product = Product.objects.get(pk = id)
    # Hapus data
    product.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))