from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from target.models import categories_table, main_category
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
main_category_list = ['Transportation',
                      'Car',
                      'Entertainment',
                      'Food',
                      'Home',
                      'Utilities',
                      'Gifts and Donations',
                      'Shopping',
                      'Miscellanous',
                      'Loans',
                      'income',
                      'transfer',
                      'credit card payment',
                      'cashback',
                      'unassigned'
                    ]

category_list = ['housing', 
                 'utilities', 
                 'car payment', 
                 'gas', 
                 'groceries',
                  'proparty tax',
                  'home insurance',
                  'car insurance',
                   'internet',
                   'mobile bills',
                    'car wash',
                    'subscription',
                    'food delivery',
                    'entertainment',
                    'home improvement',
                    'gifts',
                    'donations',
                    'Egypt Expenses',
                    'personal care',
                    'transportation',
                    'miscellaneous',
                    'car maintenance',
                    'home maintenance',
                    'pet care',
                    'loans',
                    'health',
                    'clothes',
                    'sport',
                    'credit card payment',
                    'refund or cashback',
                    'transfer',
                    'unassigned',
                    'income']

basic_main_category ={
                'housing':'Home', 
                 'utilities' : 'Utilities', 
                 'car payment':'Car', 
                 'gas':'Car', 
                 'groceries':'Food',
                  'proparty tax':'Home',
                  'home insurance':'Home',
                  'car insurance':'Car',
                   'internet':'Utilities',
                   'mobile bills':'Utilities',
                    'car wash':'Car',
                    'subscription':'Entertainment',
                    'food delivery':'Food',
                    'entertainment':'Entertainment',
                    'home improvement':'Home',
                    'gifts':'Gifts and Donations',
                    'donations':'Gifts and Donations',
                    'Egypt Expenses':'Entertainment',
                    'personal care':'Shopping',
                    'transportation':'Transportation',
                    'miscellaneous':'Miscellanous',
                    'car maintenance':'Car',
                    'home maintenance':'Home',
                    'pet care':'Shopping',
                    'loans':'Loans',
                    'health':'Shopping',
                    'clothes':'Shopping',
                    'sport':'Entertainment',
                    'credit card payment':'credit card payment',
                    'refund or cashback':'cashback',
                    'transfer':'transfer',
                    'unassigned':'Miscellanous',
                    'income':'income'
}

def loginpage(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard_view")
        else:
            return redirect("/?failed=1")
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
            UserProfile.objects.create(user_id=user)
            family_id=None
            
            for category in main_category_list:
                main_category.objects.create(user_id=user,category_name=category,family_id=family_id)
    
            for category in category_list:
                main_category_name = main_category.objects.get(user_id=user,category_name=basic_main_category[category])
                categories_table.objects.create(user_id=user,categories_name=category,family_id=family_id,main_category_id=main_category_name)
            user = form.cleaned_data.get('username')

            messages.success(request, " Account was created for " + user)
        
            return redirect("dashboard_view")

        else:
            return redirect("/register/?failed=1")
        
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
def terms(request):
    return render(request, "terms.html")
def contact(request):
    return render(request, "contact.html")
def privacy(request):
    return render(request, "privacy.html")