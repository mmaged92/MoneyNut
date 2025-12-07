from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from .models import categories_table, budget_target, main_category
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from family.models import familyMemebers

month_dict = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

fees_type = ["YES" , "NO"]

years_list = list(range(2025, 2055))

distribution = ['annually','monthly', 'bi-weekly']
main_category_list = ['Transportation',
                      'Car',
                      'Entertainment',
                      'Food',
                      'Home',
                      'Utilities',
                      'Grifts and Donations',
                      'Shopping',
                      'Miscellanous'
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

# # file_path_years = 'C:/Users/mahmo/OneDrive/Desktop/Budget/years.csv'
# file_path_months = 'C:/Users/mahmo/OneDrive/Desktop/Budget/months.csv'
# # with open(file_path_years, newline='', encoding='utf-8-sig') as csvfile:
# #     reader = csv.DictReader(csvfile)
# #     for row in reader:
# #         years.objects.create(years=row['year'])

# with open(file_path_months, newline='', encoding='utf-8-sig') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         year =  years.objects.get(id=row['year_id'])
#         months.objects.create(month=row['month'], year_id=year)
# ms= years.objects.all()


# yd = months.objects.select_related("year_id")
# for m in months.objects.all():
#      print(m.month, m.year_id.years)

@login_required(login_url="/users/loginpage/")
def category_add(request):
    user= request.user
    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = None
    for category in category_list:
        if not categories_table.objects.filter(user_id=user, categories_name=category).exists():
            categories_table.objects.create(user_id=user,categories_name=category,family_id=family_id)
            
    for category in main_category_list:
        if not main_category.objects.filter(user_id=user, category_name=category).exists():
            main_category.objects.create(user_id=user,category_name=category,family_id=family_id)

    if request.method == "POST":
        categories_new = request.POST.get('category')
        fixed_fees = request.POST.get('fixed_fees')
        main_category_input = request.POST.get('main_category')
        main_category_name = main_category.objects.get(user_id=user,category_name=main_category_input)
        
        if fixed_fees == "on":
            fixed_fees = True
        else:
            fixed_fees = False
        
        if categories_new: 
            if not categories_table.objects.filter(user_id=user, categories_name__iexact=categories_new, main_category_id__iexact=categories_new).exists():
                categories_table.objects.create(user_id=user,categories_name=categories_new,Fixed_fees=fixed_fees,main_category_id=categories_new,family_id=family_id)
        
            return redirect("category_add")
    main_categories =  main_category.objects.filter(user_id=user)
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','unassigned','transfer','income'])
    
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
    
    
    return render(request, 'target/category_edit.html', {"categories":categories, "main_categories":main_categories,"isfamily":isfamily})

@login_required(login_url="/users/loginpage/")
def category_get(request):
    user= request.user
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','unassigned','transfer','income'])
    category_list = []

    for category in categories:
        try:
            main_category_name = category.main_category_id.category_name
        except Exception:
            main_category_name ="--Select main Category--"
        category_list.append({"Category":category.categories_name, "fixed_fees": category.Fixed_fees,"main_category":main_category_name ,"category_id":category.id})
    return JsonResponse(category_list, safe=False)

@login_required(login_url="/users/loginpage/")
def category_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('new_value')
        category_id = data.get('category_id')
        update = categories_table.objects.get(user_id=user,id=category_id)
        if not categories_table.objects.filter(user_id=user,categories_name__iexact=newValue).exists():
            update.categories_name = newValue
            update.save()
        return JsonResponse({'status': 'updated', 'newValue': newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)


@login_required(login_url="/users/loginpage/")
def fixed_fees_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('new_value')
        print(newValue)
        
        category_id = data.get('category_id')
        update = categories_table.objects.get(user_id=user,id=category_id)
        if not categories_table.objects.filter(user_id=user,categories_name__iexact=newValue).exists():
            update.Fixed_fees = newValue
            update.save()
        return JsonResponse({'status': 'updated', 'newValue': newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)    

@login_required(login_url="/users/loginpage/")
def category_delete(request):
    user= request.user
    if request.method == 'DELETE':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        try:
            update = categories_table.objects.get(user_id=user,id=category_id)
            update.delete()
        except:
            for id in category_id:
                update = categories_table.objects.get(user_id=user,id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def target_insert(request):
    user= request.user
    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = ""
    if request.method == "POST":
        freq = request.POST.get('frequency')

        category = request.POST.get('categories')

            

        amount = request.POST.get('amount')
        if not amount:
            return 
        
        
        date = request.POST.get('date')



        date_end = request.POST.get('date_end')
        
        if not date_end or not date or not amount or not category or not freq:
            return redirect("target_insert")  


        date_format = "%Y-%m-%d"
        date_string= date
        date = datetime.strptime(date_string, date_format)
            
        date_format = "%Y-%m-%d"
        date_string= date_end
        date_end = datetime.strptime(date_string, date_format)
            
            

        category = categories_table.objects.get(user_id=user,categories_name=category)     
        if freq == "monthly":
            print(freq)
            while(date<=date_end):
                year = date.year
                month=date.month
                month = month_dict[month]
                if not budget_target.objects.filter(user_id=user,frequency= freq, month=month,year=year,category_id=category,target=amount,date=date).exists():
                    budget_target.objects.create(user_id=user,frequency= freq, month=month,year=year,category_id=category,target=amount,date=date,family_id=family_id)
                date = date + relativedelta(months=1)

            return redirect("target_insert")    
        
        elif freq == "annually":
            while(date<=date_end):
                year = date.year
                month = None                
                if not budget_target.objects.filter(user_id=user,frequency= freq, month=month,year=year,category_id=category,target=amount,date=date).exists():
                    budget_target.objects.create(user_id=user,frequency= freq, month=month,year=year,category_id=category,target=amount,date=date,family_id=family_id)
                                            
                date = date + relativedelta(years=1)
            return redirect("target_insert")  
        elif freq == "bi-weekly":
            print(freq)
            while(date<date_end):
                year = date.year
                month=date.month
                month = month_dict[month]
                if not budget_target.objects.filter(user_id=user,frequency= freq, month=month,year=year,category_id=category,target=amount,date=date).exists():
                    budget_target.objects.create(user_id=user,frequency= freq, month=month,year=year,category_id=category,target=amount,date=date,family_id=family_id)
                date = date + timedelta(days=14)
            return redirect("target_insert")  
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','unassigned','transfer','income'])

    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
    
    
    
    return render(request, 'target/targetset.html',{"categories":categories, "years" : years_list,"isfamily":isfamily})

@login_required(login_url="/users/loginpage/")
def target_delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        target_id = data.get('target_id')
        print(target_id)
        try:
            update = budget_target.objects.get(id=target_id)
            update.delete()
        except:
            for id in target_id:
                update = budget_target.objects.get(id=id)
                update.delete()
        return redirect('target_insert')
    return JsonResponse({'error': 'Invalid method'}, status=405)   

@login_required(login_url="/users/loginpage/")
def target_get(request):
    user= request.user
    targets = budget_target.objects.filter(user_id=user)
    target_list = []
    
    for target in targets:
        target_list.append({'year': target.year, 'month':target.month, 'category':target.category_id.categories_name
                        ,'target':target.target, 'frequency':target.frequency, 'target_id':target.id
                        , 'date':target.date})            
    return JsonResponse(target_list, safe=False)



@login_required(login_url="/users/loginpage/")
def category_update_target(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        target_id = data.get('target_id')
        newcategory = categories_table.objects.get(user_id=user,categories_name = newValue)
        update = budget_target.objects.get(user_id=user,id=target_id)
        update.category_id = newcategory
        update.save()
        return JsonResponse({'status': 'modified','newValue':newValue})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def target_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        target_id = data.get('target_id')
        update = budget_target.objects.get(user_id=user,id=target_id)
        update.target = newValue
        update.save()
        return JsonResponse({'status':'updated','newValue':newValue})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def date_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        date= datetime.strptime(newValue, "%Y-%m-%d")
        year = date.year
        month= date.month
        month = month_dict[month]        
        target_id = data.get('target_id')
        update = budget_target.objects.get(user_id=user,id=target_id)
        update.date = newValue
        update.year = year
        update.month = month
        update.save()
        
        return JsonResponse({'status':'updated','newValue':newValue})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def freq_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        target_id = data.get('target_id')

        if newValue == 'annually':
            update = budget_target.objects.get(user_id=user,id=target_id)
            update.frequency = 'annually'
            update.save()
        else:
            update = budget_target.objects.get(user_id=user,id=target_id)
            update.frequency = 'monthly'
            update.save()
        return JsonResponse({'status':'updated','newValue':newValue})
    return JsonResponse({'error':'Invalid method'}, status = 405)


@login_required(login_url="/users/loginpage/")
def freqget(request):
    return JsonResponse(distribution, safe=False)

@login_required(login_url="/users/loginpage/")
def category_main_category_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('new_value')
        category_id = data.get('category_id')
        update = categories_table.objects.get(user_id=user,id=category_id)
        main_category_new = main_category.objects.get(user_id=user,category_name=newValue)
        update.main_category_id = main_category_new
        update.save()
        return JsonResponse({'status': 'updated', 'newValue': newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def main_category_add(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newCategory = data.get('newCategory')
        print(data)
        if not main_category.objects.filter(user_id=user,category_name__iexact=newCategory).exists():
            main_category.objects.create(user_id=user,category_name=newCategory)
            return redirect('category_add')
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def main_category_get(request):
    user= request.user
    categories = main_category.objects.filter(user_id=user)
    category_list = []
    for category in categories:
        category_list.append({"Category":category.category_name, "category_id":category.id})
    return JsonResponse(category_list, safe=False)

@login_required(login_url="/users/loginpage/")
def main_category_get_list(request):
    user= request.user
    categories = main_category.objects.filter(user_id=user)
    category_list = []
    for category in categories:
        category_list.append(category.category_name)
    return JsonResponse(category_list, safe=False)

@login_required(login_url="/users/loginpage/")
def main_category_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('new_value')
        category_id = data.get('category_id')
        update = main_category.objects.get(user_id=user,id=category_id)
        if not main_category.objects.filter(user_id=user,category_name__iexact=newValue).exists():
            update.category_name = newValue
            update.save()
        return JsonResponse({'status': 'updated', 'newValue': newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def main_category_delete(request):
    user= request.user
    if request.method == 'DELETE':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        try:
            update = main_category.objects.get(user_id=user,id=category_id)
            update.delete()
        except:
            for id in category_id:
                update = main_category.objects.get(user_id=user,id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)



