from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Login Views 
class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        authenticate_user = authenticate(request, username=username, password=password)
        
        if authenticate_user is None:
            messages.error(request, "Invalid Credentials")
            return render(request, "auth/login.html")

        login(request, authenticate_user)
        return redirect('dashboard')
# End of Login Views
    
    
# Register Views 
class RegisterView(View):
    def get(self, request):
        return render(request, "auth/register.html")
    
    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if password != confirm_password:
            messages.error(request, "Password doesn't match")
            return render(request, "auth/register.html")  

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "auth/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "auth/register.html")

        User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        messages.success(request, "Successfuly Register continue to Login.")
        return redirect("login")
# End of Register Views