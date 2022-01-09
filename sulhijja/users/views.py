from django.db import reset_queries
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from .models import Datadiri
from .forms import UserForms, DatadiriForms


# Create your views here.

def is_operator(user):
    if user.groups.filter(name='Operator').exists():
        return True
    else:
        return False

@login_required
@user_passes_test(is_operator)
def users(request):
    template_name = "back/tabel_user.html"
    list_user = User.objects.all()
    context = {
        'title' :'tabel users',
        'list_user':list_user

    }
    return render(request, template_name,context)

@login_required
@user_passes_test(is_operator)
def user_detil(request, id):
    template_name = "back/user_detil.html"
    try:
        user_info = User.objects.get(id=id)
        datadri = Datadiri.objects.get(user=user_info)
    except:
        return redirect(users)
    context = {
        'title' :'user detail',
        'user_info' : user_info,
        'datadiri' : datadri,
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator)
def user_edit(request, id):
    template_name = "back/user_edit.html"
    try:
        user_info = User.objects.get(id=id)
        datadri = Datadiri.objects.get(user=user_info)
    except:
        return redirect(users)

    if request.method == "POST":
        forms_user = UserForms(request.POST, instance=user_info)
        forms_datadiri = DatadiriForms(request.POST, instance=datadri)
        if forms_user.is_valid() and forms_datadiri.is_valid():
            activ = forms_user.save(commit=False)
            activ.is_active = True
            activ.save()
            forms_datadiri.save()
            return redirect(users)
    else:
        forms_user = UserForms(instance=user_info)
        forms_datadiri = DatadiriForms(instance=datadri)
    context = {
        'title' :'user edit',
        'user_info' : user_info,
        'datadiri' : datadri,
        'forms_user' : forms_user,
        'forms_datadiri' : forms_datadiri,
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator)
def user_delete(request, id):
    try:
        User.objects.get(id=id).delete()
    except:
        pass
    return redirect(users)


