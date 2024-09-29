from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Homepage view, requires login
@never_cache
@login_required(login_url='login')
def Homepage(request):
    return render(request, 'home.html')

# Signup page
@never_cache
def Signupage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        # Validate that all fields are filled
        if not uname or not email or not pass1 or not pass2:
            return render(request, 'signup.html', {
                'error': "All fields are required",
                'username': uname,
                'email': email
            })
        
        # Username validation
        if len(uname) < 6:
            return render(request, 'signup.html', {
                'error': "Username must be at least 6 characters long",
                'username': uname,
                'email': email
            })
        if not uname.isalnum():
            return render(request, 'signup.html', {
                'error': "Username must be alphanumeric",
                'username': uname,
                'email': email
            })

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'signup.html', {
                'error': "Invalid email format",
                'username': uname,
                'email': email
            })
        
        # Password validation
        if len(pass1) < 8:
            return render(request, 'signup.html', {
                'error': "Password must be at least 8 characters long",
                'username': uname,
                'email': email
            })
        if pass1 != pass2:
            return render(request, 'signup.html', {
                'error': "Passwords do not match",
                'username': uname,
                'email': email
            })
        
        if User.objects.filter(username=uname).exists():
            return render(request, 'signup.html', {
                'error': "Username already exists",
                'username': uname,
                'email': email
            })
        
        try:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
        except IntegrityError:
            return render(request, 'signup.html', {
                'error': "Error during user creation",
                'username': uname,
                'email': email
            })
    
    return render(request, 'signup.html')
# Login page
@never_cache
def Loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_panel')
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {'error': "Invalid Username or Password"})
    
    return render(request, 'login.html')

# Logout function
@never_cache
@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')

# Check if user is admin
def is_admin(user):
    return user.is_staff

# Admin panel
@never_cache
@user_passes_test(is_admin)
def admin_panel(request):
    query = request.GET.get('q','')
    if query:
        users = User.objects.filter(username__icontains=query,is_superuser=False)
    else:
        users = User.objects.filter(is_superuser=False)
    no_users_found = not users.exists()
    
    return render(request, 'admin_panel.html', {
        'users': users,
        'query': query,
        'no_users_found': no_users_found
    })


# Admin user creation
@never_cache
@user_passes_test(is_admin)
def create_user(request):
    error=''
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        # Validate that all fields are filled
        if not uname or not email or not pass1 or not pass2:
            error = 'All fields are required'
        
        # Username validation
        elif len(uname) < 6:
            error = "Username must be at least 6 characters long"
        elif not uname.isalnum():
            error = "Username must be alphanumeric"

        
        # Password validation
        elif len(pass1) < 8:
            error = "Password must be at least 8 characters long"
        elif pass1 != pass2:
            error = "Passwords do not match"
        
        elif User.objects.filter(username=uname).exists():
            error = "Username already exists"
        elif User.objects.filter(email=email).exists():
            error = "Email already exists"
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('admin_panel')
        
    return render(request, 'create_user.html', {'e': error})

#edit 
@never_cache
@user_passes_test(is_admin)
def edit_user(request,user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method=='POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return redirect('admin_panel')
    return render(request, 'edit.html', {'user': user})


@never_cache
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_panel')
