from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def singup(request):
    if request.method=='POST':
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.get(username=request.POST['username'])
                error = 'User Name Has Alredy Taken'
                context ={
                    'error':error,
                }
                return render(request,'singup.html',context)
            except:

                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            error = 'Password Not Match'
            context ={
                    'error':error,
                }
            return render(request,'singup.html',context)

        
    else:


        return render(request,'singup.html')
def login(request):
    if request.method=='POST':
        user = auth.authenticate(request,username=request.POST['username'],password=request.POST['password'])

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            error = 'Pls Log In Your Correct informations'
            context ={
                    'error':error,
                }
            return render(request,'login.html',context)

    else:
        return render(request,'login.html')
def logout(request):
    if request.method =='POST':
        auth.logout(request)
        return redirect('home')
    return render(request,'logout.html')