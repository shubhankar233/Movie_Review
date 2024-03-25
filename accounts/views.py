# from django.shortcuts import render, redirect
# from .forms import*
# from django.contrib.auth import authenticate, login, logout

# # Create your views here.
# # registeration

# def register(request):
#     if request.method == "POST":
#         form = ResgistrationForm(request.POST or None)
#         if form.is_valid():
#             user = form.save()

#             raw_password = form.cleaned_data('password1')

#             user = authenticate(username=user.username, password=raw_password)

#             login(request,user)
#             return redirect("main:home")
#     else:
#         form = RegistrationForm()
#     return redirect(request, "accounts/register.html", {"forms": form})

from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")

     #if not logged in   
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()

                raw_password = form.cleaned_data.get('password1')  # Use square brackets for accessing cleaned_data

                user = authenticate(username=user.username, password=raw_password)

                login(request, user)
                return redirect("main:home")
        else:
            form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})  # Use render to render the template


#login
def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            print(username, password)
            #check creditianls
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("main:home")
                else:
                    return render(request, 'accounts/login.html',{"error":"Your account has been disabled."})
            else:
                return render(request, 'accounts/login.html',{"error":"Invalid Username or Password. Try Again."})
        return render(request, 'accounts/login.html')

# logout user
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        print("Logged out successfully")
        return redirect("accounts:login")
    else:
        return redirect("accounts:login")