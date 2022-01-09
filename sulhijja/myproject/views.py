from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from blog.models import Artikel, Kategori
from django.contrib.auth import authenticate, get_user
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.db import transaction
from django.contrib.auth.hashers import make_password

from blog.models import Artikel
from users.models import Datadiri



def home(request):
    template_name = 'front/index.html'
    artikel = Artikel.objects.all()
    kategori = Kategori.objects.all()
    context = {
        'title':'Halaman awal',
        'artikel':artikel,
        'kategori':kategori,
    }
    return render(request, template_name, context)

def artikel_filter(request, nama):
    template_name = 'front/index.html'
    kategori = Kategori.objects.all()
    artikel = Artikel.objects.filter(kategory__nama=nama)
    context = {
        'title':'Halaman awal',
        'artikel':artikel,
        'kategori':kategori,
    }
    return render(request, template_name, context)

def detail_artikel(request, id):
    template_name = 'front/detail_artikel.html'
    artikel  = Artikel.objects.get(id=id)
    context = {
        'title':'detail',
        'artikel':artikel,
    }    
    return render(request, template_name, context)


def about(request):
    template_name = 'front/about.html'
    context = {
        'title':'about me',
        'welcome': 'ini page about',
    }
    return render(request, template_name, context)

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    template_name = 'account/login.html'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #data ada
            print('username benar')
            auth_login(request, user)
            return redirect('home')
        else:
            #data tidak ada
            print('username salah')

    context = {
        'title':'from login',
    }
    return render(request, template_name, context)

def logout_view(request):
    logout(request)
    return redirect('home')

def registrasi(request):
    template_name = "account/register.html"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        telp = request.POST.get('telp')
        try:
            with transaction.atomic():
                User.objects.create(
                    username = username,
                    password = make_password(password),
                    first_name = nama_depan,
                    last_name = nama_belakang,
                    email = email            
                )
                get_user = User.objects.get(username = username)
                Datadiri.objects.create(
                    user = get_user,
                    alamat = alamat,
                    telp = telp,
                )
            return redirect(login)
        except:pass

    context = {
        'title':'form registrasi'
    }
    return render(request, template_name, context)

