from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import get_user_model


User = get_user_model()

@login_required
def index(request):
    return render(request, 'frontend/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'frontend/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def get_users(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'No tienes permiso para ver esta información'}, status=403)
    
    users = User.objects.all().values('username', 'email', 'is_superuser', 'last_login')
    return JsonResponse(list(users), safe=False)