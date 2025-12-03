from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CreateUserForm
from django.contrib import messages
from userprofile.models import UserProfile
# from django.contrib.auth.decorators import login_required

# def main(request):
#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect("dashboard")
#     else:
#         form = AuthenticationForm()
#     return render(request, "main.html" , {"form" : form })

def loginpage(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard_view")
    else:
        form = AuthenticationForm()

    if request.user.is_authenticated:
        return redirect('dashboard_view')
    return render(request, "loginpage.html" , {"form" : form })

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            user = request.user
            # date = request.POST.get('Date_of_birth')
            # UserProfile.objects.create(user_id=user, Birth_date=date)
            user = form.cleaned_data.get('username')
            messages.success(request, " Account was created for " + user)
        
            return redirect("dashboard_view")

        else:
            print(form.errors)
            return redirect("register")
        
    if request.user.is_authenticated:
        return redirect('dashboard_view')
    
    context = {"form" : form }
    return render(request, "register.html" , context)



def logout_view(request):
     if request.method == "POST":
          logout(request)
          return redirect("loginpage")

def about(request):
    return render(request, "about.html")