from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/login')
def home(request):
    return render(request, 'home.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login.home')
        else:
            print('Wrong Credential!')
    return  render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('login.login')