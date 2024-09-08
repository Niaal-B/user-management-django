from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.
@never_cache
@login_required(login_url='login')
def Homepage(request):
    uname=request.user.email
    return render(request,'home.html',{
        "check":uname
    })
    


@never_cache
def Signupage(request):
    if request.user.is_authenticated:
        return redirect(Homepage)
    if request.method== 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            return render(request,'signup.html',{
                'error':"Password are Not same"
            })
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            
            my_user.save()

            return redirect('login')
    return render(request,'signup.html')



@never_cache
def Loginpage(request):
    if request.user.is_authenticated:
        return redirect(Homepage)
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{
                'error':"Invalid Username Or Password"
            })

    return render(request,'login.html')

@never_cache
@login_required(login_url='signup')
def Logout(request):
    logout(request)
    print("user is logout")
    return redirect('login')