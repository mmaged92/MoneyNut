from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from trans.models import trans
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
import json
from .models import SavingTarget, SavingGoal, expectedIncome
from accounts.models import Accounts
from family.models import familyMemebers
month_dict = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

years_list = list(range(2025, 2055))

distribution = ['-- Select frequency --','annually','monthly','semi-monthly' ,'bi-weekly']

##################################################Saving###################################################################

def saving_target_insert(user,freq, saving_amount, start_date, date_end):
    date = start_date
    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = None
    if freq == "monthly":
        print(freq)
        while(date<=date_end):
            year = date.year
            month = date.month
            month = month_dict[month]
            
            if not SavingTarget.objects.filter(user_id=user,frequency= freq, month=month,year=year,Saving_target=saving_amount,date=date).exists():
                SavingTarget.objects.create(user_id=user,frequency= freq, month=month,year=year,Saving_target=saving_amount,date=date,family_id=family_id)
            date = date + relativedelta(months=1)

    elif freq == "annually":
        while(date<=date_end):
            year = date.year
            month = None                
            if not SavingTarget.objects.filter(user_id=user,frequency= freq, month=month,year=year,Saving_target=saving_amount,date=date).exists():
                SavingTarget.objects.create(user_id=user,frequency= freq, month=month,year=year,Saving_target=saving_amount,date=date,family_id=family_id)
                                            
            date = date + relativedelta(years=1)

    
    elif freq == "bi-weekly":
        print(freq)
        while(date<date_end):
            year = date.year
            month = date.month
            month = month_dict[month]
            if not SavingTarget.objects.filter(user_id=user,frequency= freq, month=month,year=year,Saving_target=saving_amount,date=date).exists():
                SavingTarget.objects.create(user_id=user,frequency= freq, month=month,year=year,Saving_target=saving_amount,date=date,family_id=family_id)
            date = date + timedelta(days=14)
    elif freq == "semi-monthly":
        print(freq)
        while(date<date_end):
            year = date.year
            month = date.month
            month = month_dict[month]
            if not SavingTarget.objects.filter(user_id=user,frequency= freq, month=month,year=year,Saving_target=saving_amount,date=date).exists():
                SavingTarget.objects.create(user_id=user,frequency= freq, month=month,year=year,Saving_target=saving_amount,date=date,family_id=family_id)
            if date.day == 15:
                date = date + relativedelta(months=1)
                date = date.replace(day=1) - timedelta(days=1)
            else:
                date = date + timedelta(days=15)
    else:
        return redirect("saving_monthly_target")
    
    saving_target = SavingTarget.objects.filter(user_id=user)
    return saving_target






@login_required(login_url="/users/loginpage/")
def saving_monthly_target(request):
    if request.method == "POST":
        freq = request.POST.get('frequency')       
        saving_amount = request.POST.get('amount')
        start_date = request.POST.get('date_start')
        date_end = request.POST.get('date_end')

        if not freq or freq == '--Select frequency--' or not saving_amount or not start_date or not date_end:
            return redirect("saving_monthly_target")
        
        date_format = "%Y-%m-%d"
        date_string= start_date
        start_date = datetime.strptime(date_string, date_format)
        
        date_format = "%Y-%m-%d"
        date_string= date_end
        date_end = datetime.strptime(date_string, date_format)       
        
        saving_target_insert(request.user,freq, saving_amount, start_date, date_end)
        
        
    if familyMemebers.objects.filter(user_id=request.user).exists():
        isfamily = True
    else:
        isfamily = False
        
    
    
    
    return render(request, 'saving/saving_monthly_target.html',{'frequency':distribution,"isfamily":isfamily})

@login_required(login_url="/users/loginpage/")
def saving_target_get(request):
    user= request.user
    
    saving_targets = SavingTarget.objects.filter(user_id=user)
    target_list = []
    
    for target in saving_targets:
          
        target_list.append({'year': target.year, 'month':target.month ,'Saving_target':target.Saving_target, 
                            'frequency':target.frequency, 'saving_target_id':target.id,
                        'date':target.date})            
    return JsonResponse(target_list, safe=False)



@login_required(login_url="/users/loginpage/")
def freq_get(request):
    return JsonResponse(distribution, safe=False)

@login_required(login_url="/users/loginpage/")
def delete_saving(request):
    user= request.user
    if request.method == 'DELETE':
        data = json.loads(request.body)
        saving_target_id = data.get('target_id')
        print(saving_target_id)
        try:
            update = SavingTarget.objects.get(user_id=user,id=saving_target_id)
            update.delete()
        except:
            for id in saving_target_id:
                update = SavingTarget.objects.get(user_id=user,id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)



@login_required(login_url="/users/loginpage/")
def saving_target_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        saving_target_id = data.get('saving_target_id')
        print(newValue)
        update = SavingTarget.objects.get(user_id=user,id=saving_target_id)
        print(update)
        update.Saving_target = newValue
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
        saving_target_id = data.get('saving_target_id')
        update = SavingTarget.objects.get(user_id=user,id=saving_target_id)
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
        saving_target_id = data.get('saving_target_id')
        year = data.get('year')

        if newValue == 'annually':
            update = SavingTarget.objects.get(user_id=user,id=saving_target_id)
            update.frequency = 'annually'
            update.save()
        elif newValue == 'monthly':
            update = SavingTarget.objects.get(user_id=user,id=saving_target_id)
            update.frequency = 'monthly'
            update.save()
        else:
            update = SavingTarget.objects.get(user_id=user,id=saving_target_id)
            update.frequency = 'bi-weekly'
            update.save()           
        return JsonResponse({'status':'updated','newValue':newValue})
    return JsonResponse({'error':'Invalid method'}, status = 405)
##################################################Income###################################################################
def income_insert(user,freq, amount, start_date, date_end):
    date = start_date

    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = None
    if freq == "monthly":
        print(freq)
        while(date<=date_end):
            year = date.year
            month = date.month
            month = month_dict[month]
            if not expectedIncome.objects.filter(user_id=user,frequency= freq, month=month,year=year,Expected_income=amount,date=date).exists():
                expectedIncome.objects.create(user_id=user,frequency= freq, month=month,year=year,Expected_income=amount,date=date,family_id=family_id)
            date = date + relativedelta(months=1)

        return redirect("income_view")
    elif freq == "annually":
        while(date<=date_end):
            year = date.year
            month = None
            if not expectedIncome.objects.filter(user_id=user,frequency= freq, month=month,year=year,Expected_income=amount,date=date).exists():
                expectedIncome.objects.create(user_id=user,frequency= freq, month=month,year=year,Expected_income=amount,date=date,family_id=family_id)
                                            
            date = date + relativedelta(years=1)
        return redirect("income_view")
    elif freq == "bi-weekly":
        print(freq)
        while(date<date_end):
            year = date.year
            month = date.month
            month = month_dict[month]
            if not expectedIncome.objects.filter(user_id=user,frequency= freq, month=month,year=year,Expected_income=amount,date=date).exists():
                expectedIncome.objects.create(user_id=user,frequency= freq, month=month,year=year,Expected_income=amount,date=date,family_id=family_id)
            date = date + timedelta(days=14)

        return redirect("income_view")
    elif freq == "semi-monthly":
        print(freq)
        while(date<date_end):
            year = date.year
            month = date.month
            month = month_dict[month]
            if not expectedIncome.objects.filter(user_id=user,frequency= freq, month=month,year=year,Expected_income=amount,date=date).exists():
                expectedIncome.objects.create(user_id=user,frequency= freq, month=month,year=year,Expected_income=amount,date=date,family_id=family_id)
            if date.day == 15:
                date = date + relativedelta(months=1)
                date = date.replace(day=1) - timedelta(days=1)
            else:
                date = date + timedelta(days=15)

    else:
        return redirect("income_view")
    






@login_required(login_url="/users/loginpage/")
def income_view(request):
    if request.method == "POST":
        freq = request.POST.get('frequency')

        saving_amount = request.POST.get('amount')

        start_date = request.POST.get('date_start')

        date_end = request.POST.get('date_end')
        
        if not freq or not saving_amount or not start_date or not date_end:
            return redirect("income_view")
        

        date_format = "%Y-%m-%d"
        date_string= date_end
        date_end = datetime.strptime(date_string, date_format)
        date_end=date_end.replace(day=1)
        
        date_string= start_date
        start_date = datetime.strptime(date_string, date_format)
        start_date=start_date.replace(day=15)
        
        income_insert(request.user,freq, saving_amount, start_date, date_end)
        return redirect("income_view")
        
    if familyMemebers.objects.filter(user_id=request.user).exists():
        isfamily = True
    else:
        isfamily = False
    return render(request, 'saving/income.html',{'frequency':distribution,"isfamily":isfamily})

@login_required(login_url="/users/loginpage/")
def income_get(request):
    user= request.user
    Incomes = expectedIncome.objects.filter(user_id=user)
    income_list = []
    
    for income in Incomes:
          
        income_list.append({'year': income.year, 'month':income.month ,'income':income.Expected_income, 
                            'frequency':income.frequency, 'income_id':income.id
                        , 'date':income.date})            
    return JsonResponse(income_list, safe=False)




@login_required(login_url="/users/loginpage/")
def income_freq_get(request):
    return JsonResponse(distribution, safe=False)

@login_required(login_url="/users/loginpage/")
def delete_income(request):
    user= request.user
    if request.method == 'DELETE':
        data = json.loads(request.body)
        income_id = data.get('income_id')
        try:
            update = expectedIncome.objects.get(user_id=user,id=income_id)
            update.delete()
        except:
            for id in income_id:
                update = expectedIncome.objects.get(user_id=user,id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)



@login_required(login_url="/users/loginpage/")
def income_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        income_id = data.get('income_id')
        print(newValue)
        update = expectedIncome.objects.get(user_id=user,id=income_id)
        print(update)
        update.Expected_income = newValue
        update.save()
        return JsonResponse({'status':'updated','newValue':newValue})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def income_date_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        date= datetime.strptime(newValue, "%Y-%m-%d")
        year = date.year
        month= date.month
        income_id = data.get('income_id')
        update = expectedIncome.objects.get(user_id=user,id=income_id)
        update.date = newValue
        update.year = year
        update.month = month
        update.save()
        return JsonResponse({'status':'updated','newValue':newValue})
    return JsonResponse({'error':'Invalid method'}, status = 405)

@login_required(login_url="/users/loginpage/")
def income_freq_update(request):
    user= request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newValue = data.get('newValue')
        income_id = data.get('income_id')
        year = data.get('year')

        if newValue == 'annually':
            update = expectedIncome.objects.get(user_id=user,id=income_id)
            update.frequency = 'annually'
            update.save()
        elif newValue == 'monthly':
            update = expectedIncome.objects.get(user_id=user,id=income_id)
            update.frequency = 'monthly'
            update.save()
        elif newValue == 'bi-weekly':
            update = expectedIncome.objects.get(user_id=user,id=income_id)
            update.frequency = 'bi-weekly'
            update.save()           
        else:
            update = expectedIncome.objects.get(user_id=user,id=income_id)
            update.frequency = 'semi-monthly'
            update.save()           
        return JsonResponse({'status':'updated','newValue':newValue})
    return JsonResponse({'error':'Invalid method'}, status = 405)

#######################################Goal############################################

def setSavingGoal(user, goal_name, goal_amount,account_name, due_date,create_date):
    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = None
    if not SavingGoal.objects.filter(user_id=user, Goal_name=goal_name, Goal=goal_amount, due_date=due_date,create_date=create_date,Account=account_name):
        SavingGoal.objects.create(user_id=user, Goal_name=goal_name, Goal=goal_amount, due_date=due_date,create_date=create_date,Account=account_name,family_id=family_id)
        return redirect("goal_view")
    return redirect("goal_view")

def goal_table_get(user):
    goal_list = []
    goals = SavingGoal.objects.filter(user_id=user)
    for goal in goals:
        goal_list.append({"goal_id":goal.id, "Due_date":goal.due_date, "Goal_target":goal.Goal
                          ,"Goal_name": goal.Goal_name, "Goal_created_on":goal.create_date, "Account":goal.Account.account_name})
    return goal_list

@login_required(login_url="/users/loginpage/")
def goal_view(request):
    user = request.user
    if request.method == 'POST':
        goal_name = request.POST.get('goal_name')
        goal_amount = request.POST.get('goal_amount')
        due_date = request.POST.get('due_date')
        account_name = request.POST.get('account_name')
        if not goal_name or not goal_amount or not due_date:
            return redirect("goal_view")
        
        
        account = Accounts.objects.get(user_id=user,account_name=account_name)
        setSavingGoal(user, goal_name, goal_amount,account, due_date,datetime.today())
        return redirect("goal_view")
    
    account_list = Accounts.objects.filter(user_id=user)
    
    if familyMemebers.objects.filter(user_id=request.user).exists():
        isfamily = True
    else:
        isfamily = False
    
    
    context ={
        "accounts":account_list,
        "isfamily":isfamily
    }
    return render(request, 'saving/saving_goal.html',context)


@login_required(login_url="/users/loginpage/")
def goal_get(request):
    return JsonResponse(goal_table_get(request.user), safe=False)
    
@login_required(login_url="/users/loginpage/")
def goal_delete(request):
    if request.method == 'DELETE':
        user= request.user
        data = json.loads(request.body)
        goal_id = data.get('goal_id')
        try:
            update = SavingGoal.objects.get(user_id=user,id=goal_id)
            update.delete()
        except:
            for id in goal_id:
                update = SavingGoal.objects.get(user_id=user,id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)      

@login_required(login_url="/users/loginpage/")
def goal_name_update(request):
    if request.method == "PUT":
        user= request.user
        data = json.loads(request.body)
        goal_id = data.get('goal_id')
        newValue = data.get('newValue')
        
        update = SavingGoal.objects.get(user_id=user, id = goal_id)
        update.Goal_name = newValue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)      
        
@login_required(login_url="/users/loginpage/")
def get_accounts(request):   
    user=request.user
    accounts = Accounts.objects.filter(user_id=user)
    account_list = []
    for account in accounts:
        account_list.append(account.account_name)

    return JsonResponse(account_list, safe=False)
    
    
@login_required(login_url="/users/loginpage/")
def goal_target_update(request):
    if request.method == "PUT":
        user= request.user
        data = json.loads(request.body)
        goal_id = data.get('goal_id')
        newValue = data.get('newValue')
        
        update = SavingGoal.objects.get(user_id=user, id = goal_id)
        update.Goal = newValue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)    

@login_required(login_url="/users/loginpage/")
def goal_account_update(request):
    if request.method == "PUT":
        user= request.user
        data = json.loads(request.body)
        goal_id = data.get('goal_id')
        newValue = data.get('newValue')
        
        new_account_id = Accounts.objects.get(user_id=user,account_name=newValue)
        update = SavingGoal.objects.get(user_id=user, id = goal_id)
        update.Account = new_account_id
        update.save()
        return JsonResponse({'status': 'updated','newValue':newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)    
    
@login_required(login_url="/users/loginpage/")
def goal_due_date_update(request):
    if request.method == "PUT":
        user= request.user
        data = json.loads(request.body)
        goal_id = data.get('goal_id')
        newValue = data.get('newValue')
        
        update = SavingGoal.objects.get(user_id=user, id = goal_id)
        update.due_date = newValue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newValue})
    return JsonResponse({'error': 'Invalid method'}, status=405)    

