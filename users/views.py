from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Validate username - only letters and numbers
        if not username.isalnum():
            messages.error(request, 'Username should contain only letters and numbers!')
            return redirect('register')

        # Validate email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$'
        if not re.match(email_pattern, email):
            messages.error(request, 'Please enter a valid email address!')
            return redirect('register')

        # Validate password length
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters!')
            return redirect('register')

        # Validate password has letter
        if not any(c.isalpha() for c in password1):
            messages.error(request, 'Password must contain at least one letter!')
            return redirect('register')

        # Validate password has number
        if not any(c.isdigit() for c in password1):
            messages.error(request, 'Password must contain at least one number!')
            return redirect('register')

        # Validate password has special character
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        if not any(c in special_chars for c in password1):
            messages.error(request, 'Password must contain at least one special character!')
            return redirect('register')

        # Check passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        # Check username taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('register')

        # Check email taken
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
        user.save()
        messages.success(request, 'Account created! Please login.')
        return redirect('login')

    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please fill in all fields!')
            return render(request, 'users/login.html')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')