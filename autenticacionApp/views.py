from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "home.html")
@login_required
def priv(request):
    return render(request, "priv.html")

def registro(request):
    if request.method =='GET':
        return render(request,"registro.html",{
            "form":UserCreationForm
        })
    else:
        req=request.POST
        if req['password1']==req['password2']:
            try:
                user = User.objects.create_user(
                    username=req['username'], password=req['password1']
                )
                user.save()
                login(request, user)
                return redirect('/home/')
            except  IntegrityError as ie:
                return render(request,"registro.html",{
                    "form":UserCreationForm,
                    "msg":"Usuario existente"
                })
            except Exception as e:
                return render(request,"registro.html",{
                    "form":UserCreationForm,
                    "msg":f"Error {e}"
                })
        else:
            return render(request,"registro.html",{
                "form":UserCreationForm,
                "msg":"favor de verificar la contraseña"
                })
    
def cerrarsesion(request):
    logout(request)
    return redirect('/')

def iniciarSesion(request):
    if request.method=="GET":
        return render(request,"login.html",{
            "form":AuthenticationForm
        })
    else:
        try:
            user=authenticate(request,
                            username=request.POST['username'],password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('/home/')
            else:
                return render(request,"login.html",{
                "form":AuthenticationForm,
                "msg":"Usuario o contraseña incorrectos"
            })
        except Exception as e:
            return render(request,"login.html",{
            "form":AuthenticationForm,
            "msg":f"Error {e}"
        })