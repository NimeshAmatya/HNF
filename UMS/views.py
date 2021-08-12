from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth


# Create your views here.

def home(request):
    
    return render(request, 'ums/home.html')

#REGISTER
def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if first_name == '' or last_name == '' or username == '' or email == '' or password == '' or confirm_password == '':
            messages.info(request,'Fill up the empty fields!!!')
            return redirect('UMS:register')
            

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Taken!!')
                return redirect('UMS:register')
                
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Taken!!')
                return redirect('UMS:register')

            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                messages.info(request, 'User Created')
                return redirect('UMS:login')

        else:
            messages.info(request, 'Password did not match!!')
            return redirect('UMS:register')

        return redirect('/')

    return render(request,'ums/register.html')

#LOGIN
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')

        else: 
            messages.info(request,'Invalid Credentials!!')
            return redirect('UMS:login')

    else:
        return render(request,'ums/login.html')

#LOGOUT
def logout(request):
    auth.logout(request)
    return redirect('UMS:home')




    