from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session["username"] = username

            # login(request, user)
            return redirect('otp')
        else:
            error_message = 'Invalid username or password'
    return render(request, "login.html", {'error_message': error_message})

def otp_view(request):
    error_message = None
    return render(request, "otp.html", {})

@login_required
def main_view(request):
    return render(request, "main.html", {})

def logout_view(request):
    logout(request)
    return redirect('login')