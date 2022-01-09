import contextlib
from typing import ContextManager
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.models import User
from rest_framework import response

from .models import Artikel,Kategori
from .forms import ArtikelForms

from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ArtikelSerializer

# Create your views here.

@login_required
def dashboard(request):
    if request.user.groups.filter(name='Operator').exists():
        request.session['is_operator'] = 'operator'

    template_name = "back/dashboard.html"
    context = {
        'title':'dashboard',
    }
    return render(request, template_name,context)

@login_required
def artikel(request):
    template_name = "back/tabel_artikel.html"
    artikel = Artikel.objects.filter(nama = request.user)
    #for a in artikel:
        #print(a.nama,'-',a.judul,'-',a.kategory)
    context = {
        'title':'tabel artikel',
        'artikel':artikel,
    }
    return render(request, template_name,context)

@login_required
def tambah_artikel(request):
    template_name = "back/tambah_artikel.html"
    kategory = Kategori.objects.all()

    if request.method == "POST":
        forms_artikel = ArtikelForms(request.POST, request.FILES)
        if forms_artikel.is_valid():
            art = forms_artikel.save(commit=False)            
            art.nama = request.user
            art.save()
            return redirect(artikel)

    else:
        forms_artikel = ArtikelForms()        
    context = {
        'title':'tambah artikel',
        'kategory': kategory,
        'forms_artikel':forms_artikel,
    }
    return render(request, template_name,context)

@login_required
def lihat_artikel(request, id):
    template_name = "back/lihat_artikel.html"
    artikel = Artikel.objects.get(id=id)   
    context = {
        'title':'lihat artikel',
        'artikel': artikel,

    }
    return render(request, template_name,context)

@login_required
def edit_artikel(request, id):
    template_name = "back/tambah_artikel.html"
    a = Artikel.objects.get(id=id)
    if request.method == "POST":
        forms_artikel = ArtikelForms(request.POST, request.FILES, instance=a)
        if forms_artikel.is_valid():
            art = forms_artikel.save(commit=False)            
            art.nama = request.user
            art.save()
            return redirect(artikel)
    else:
        forms_artikel = ArtikelForms(instance=a)

    context = {
        'title':'Edit artikel',
        'artikel': a,
        'forms_artikel':forms_artikel

    }
    return render(request, template_name,context)

@login_required
def delete_artikel(request, id):
    Artikel.objects.get(id=id).delete()
    return redirect(artikel)

@api_view(['GET'])
def artikel_list(request, x_api_key):
    try:
        key = request.user.api.api_key
    except:
        content = {
            'status' : False,
            'message' : 'anda belum login'
        }
        return Response(content)
    if key != x_api_key:
        content ={
            'status' : False,
            'message' : 'x api key tidak sama'
        }
        return Response(content)
    list = Artikel.objects.all()
    jumlah_artikel = list.count()
    serializer = ArtikelSerializer(list, many=True)
    content = {
        'status' : True,
        'jumlah' : jumlah_artikel,
        'rows' : serializer.data
    }
    return Response(content)

@api_view(['POST',])
def artikel_post(request, x_api_key):
    try:
        key = request.user.api.api_key
    except:
        content = {
            'status' : False,
            'message' : 'anda belum login'
        }
        return Response(content)
    if key != x_api_key:
        content ={
            'status' : False,
            'message' : 'x api key tidak sama'
        }
        return Response(content)
    if request.method == 'POST':
        serializer = ArtikelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'berhasil membuat data'
            }
            return Response(content)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {
            'status' : status.HTTP_405_METHOD_NOT_ALLOWED,
            'message' : 'method tidak ditemukan'
        }
        return Response(content)

@api_view(['GET','PUT','DELETE'])
def artikel_detail(request, pk, x_api_key):
    try:
        key = request.user.api.api_key
    except:
        content = {
            'status' : False,
            'message' : 'anda belum login'
        }
        return Response(content)
    if key != x_api_key:
        content ={
            'status' : False,
            'message' : 'x api key tidak sama'
        }
        return Response(content)
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        artikel = Artikel.objects.get(pk=pk)
    except Artikel.DoesNotExist:
        content = {
            'status' : status.HTTP_404_NOT_FOUND,
            'message' : 'artikel tidak ada'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtikelSerializer(artikel)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArtikelSerializer(artikel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'status' : status.HTTP_202_ACCEPTED,
                'message' : 'berhasil update',
                'rows' : serializer.data
            }
            return Response(content, status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        artikel.delete()
        content = {
            'status' : status.HTTP_204_NO_CONTENT,
            'message' : 'berhasil didelete'
        }
        return Response(content, status.HTTP_204_NO_CONTENT)
