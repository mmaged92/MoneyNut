from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from trans.models import trans
from target.models import budget_target, categories_table, main_category
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
import json
from saving.models import SavingTarget
from accounts.models import Accounts
from accounts.views import update_account_balance
from saving.models import SavingGoal, expectedIncome
from family.models import familyMemebers

year_list = list(range(2023,2055))

month_list =['January', 'February', 'March','April','May','June','July','August','September','October','November','December']
month_dict = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}
month_dict_add = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
    7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
}
year = date.today().year
month_no = date.today().month
month = month_dict[month_no]
# date_start = datetime(year,month_no,1)
# date_end = date_start + relativedelta(months=1) 
category_view ='Overall'

Goal_id = ""


def getMonthlyView(user):
    monthly_view=[]   
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    d_s = datetime(year,month_no,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)

    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    
    days_month = d_e - timedelta(days=1)
    days_month = days_month.day
    for category in categories:
        
        category_spent_total = category_spent_sum(user,category,d_s,d_e)
            
        category_target_total = category_target_sum(user,category,d_s,d_e)
        if category.categories_name == 'unassigned':
            Remianing = 0
        else:
            Remianing = category_target_total - category_spent_total
        
        status = budget_status(user,category,d_s,d_e, days_month)
        if category_spent_total == 0 and category_target_total == 0:
            continue
        monthly_view.append({'category': category.categories_name,'Total_spent': category_spent_total , "Total_Target": category_target_total, "Remianing": round(Remianing,2), "Status": status})

    Total_month_spent = category_spent_sum(user,None,d_s,d_e)
    
    Total_month_target = category_target_sum(user,None,d_s,d_e)
    
    month_status = budget_status(user,None,d_s,d_e, days_month)
    

    Total_ramaining = Total_month_target-Total_month_spent
    
    monthly_view.append({'category': "Monthly Total",'Total_spent': Total_month_spent , "Total_Target": Total_month_target, "Remianing": round(Total_ramaining,2), "Status": month_status})
    return monthly_view

def category_spent_sum(user,category,d_s,d_e):
    if category == None:
        category = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', date__range=(d_s, d_e),category_id__in=category)))['total']    
    else:
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', category_id=category, date__range=(d_s, d_e))))['total']    
    
    if category_spent_total == None:
        category_spent_total = 0
    else:
        category_spent_total = round(category_spent_total,2)
    
    return round(category_spent_total,2)

def category_main_spent_sum(user,category,d_s,d_e):
    if category == None:
        category = main_category.objects.filter(user_id=user).exclude(category_name=['income','transfer','credit card payment','cashback'])
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', date__range=(d_s, d_e),main_category_id__in=category)))['total']    
    else:
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', main_category_id=category, date__range=(d_s, d_e))))['total']    
    if category_spent_total == None:
        category_spent_total = 0
    else:
        category_spent_total = round(category_spent_total,2)
    
    return round(category_spent_total,2)

def spent_day_sum(user,date):
    # if category == 'Overall':
    category = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', date=date, category_id__in=category)))['total'] or 0
    # else:
    #     category = categories_table.objects.get(user_id=user,categories_name=category)
    #     category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense', category_id=category, date=date)))['total']    
    # if category_spent_total == None:
    #      category_spent_total = 0
    # else:
    #     category_spent_total = round(category_spent_total,2)
    
    return round(category_spent_total,2)    

def category_target_sum(user,category,d_s,d_e):
    category_target_total = 0
    if category == None:
        category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,date__range=(d_s,d_e))))['total']
    else:    
        category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, category_id=category,date__range=(d_s,d_e))))['total']
        
    if category_target_total == None:
        category_target_total = 0
         
    return round(category_target_total,2)


def budget_status(user,category,d_s,d_e, days_month):
    if category == None:
        category = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
        spent_total =  category_spent_sum(user,None,d_s,d_e)
        target_total =  category_target_sum(user,None,d_s,d_e)
        category = ""
        if spent_total == None:
            spent_total = 0
        if target_total == None:
            target_total = 0
            
        target_No_FF_total =  budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,category_id__Fixed_fees=False,date__range=(d_s,d_e))))['total'] or 0
        spent_FF_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user,category_id__Fixed_fees=False, IO='expense', date__range=(d_s, d_e))))['total'] or 0

        if datetime.today() <= d_e:
            days = datetime.today().day 
        else:
            days = d_e.day
        
        if spent_total > target_total:
            status = 'Over Budget'
        elif spent_total == target_total:
            status = 'On Budget' 
        elif spent_total < target_total:
            status = 'Under Budget' 
            if ((spent_FF_total/int(days))  > (target_No_FF_total/days_month) ) and days != d_e.day :
                status = 'Over Spending'

    else:
        spent_total =  category_spent_sum(user,category,d_s,d_e)
        target_total = category_target_sum(user,category,d_s,d_e)
        category= category.categories_name
        if spent_total == None:
            spent_total = 0
        if target_total == None:
            target_total = 0

        target_No_FF_total =  budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,category_id__Fixed_fees=False,date__range=(d_s,d_e))))['total'] or 0
        spent_FF_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user,category_id__Fixed_fees=False, IO='expense', date__range=(d_s, d_e))))['total'] or 0

        if datetime.today() <= d_e:
            days = datetime.today().day 
        else:
            days = d_e.day
        
        if spent_total > target_total:
            status = 'Over Budget'
        elif spent_total == target_total:
            status = 'On Budget' 
        elif spent_total < target_total:
            status = 'Under Budget' 
            if ((spent_total/int(days))  > (target_total/days_month) ) and days != d_e.day :
                status = 'Over Spending'


    return status

def category_spent_pichart(user):
    category_spent=[]   
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    d_s = datetime(year,month_no,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    
    categories = main_category.objects.filter(user_id=user).exclude(category_name=['income','transfer','credit card payment','cashback'])
    Total_month_spent = category_main_spent_sum(user,None,d_s,d_e)
    
    if Total_month_spent == 0:
        return category_spent.append({'y': 100, 'name': "categories_name"})
    
    for category in categories:   
        category_month_spent_total = round(category_main_spent_sum(user,category,d_s,d_e)*100/Total_month_spent,2)
        category_spent.append({'y': category_month_spent_total, 'name': category.category_name})
    return category_spent

def category_pent_bar(user):
    category_spent=[]   
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    d_s = datetime(year,month_no,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    categories = main_category.objects.filter(user_id=user).exclude(category_name=['income','transfer','credit card payment','cashback'])
    Total_month_spent = category_main_spent_sum(user,None,d_s,d_e)
    
    if Total_month_spent == 0:
        return category_spent.append({'label': "categories_name",'y': 100 })
    for category in categories:   
        category_month_spent_total = round(category_main_spent_sum(user,category,d_s,d_e),2)
        category_spent.append({'label': category.category_name,'y': category_month_spent_total })
    return category_spent 
    
def category_spent_bar_daily(user):
    category_spent=[]   
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    d_s = datetime(year,month_no,1)
    date = d_s
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)

    while(date < d_e):    
        Total_daily_spent = round(spent_day_sum(user,date),2)
        datedisplay = date.strftime("%b/%d")
        category_spent.append({'y': Total_daily_spent, 'label': datedisplay})
        date = date + timedelta(days=1)

    return category_spent     


def income_calc(user,d_s,d_e):
    income = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='income' ,date__range=(d_s, d_e))))['total'] or 0
    transfer_in = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='transfer-in' ,date__range=(d_s, d_e))))['total'] or 0
    transfer_out = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='transfer-out' ,date__range=(d_s, d_e))))['total'] or 0
    income = income + transfer_in - transfer_out
    return income

def target_saving_calc(user,d_s,d_e):
    return SavingTarget.objects.aggregate(total=Sum('Saving_target',filter=Q(user_id=user, date__range=(d_s, d_e))))['total']

def spentVstargetCalc(user):
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    d_s = datetime(year,month_no,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    target = category_target_sum(user,None,d_s,d_e)
    actual_spent = category_spent_sum(user,None,d_s,d_e)
    
    return [{"y": target, "label":"Target"} , {"y": actual_spent, "label":"Actual Spent" }]


def incomeVsspentCalc(user):
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    d_s = datetime(year,month_no,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    income = income_calc(user,d_s,d_e)
    actual_spent = category_spent_sum(user,None,d_s,d_e)
    return [{"y": income, "label":"Income"} , {"y": actual_spent, "label":"Actual Spent" }]


def savingVstargetCalc(user):
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    d_s = datetime(year,month_no,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    income = income_calc(user,d_s,d_e)
    actual_spent = category_spent_sum(user,None,d_s,d_e)
    actual_saving = income - actual_spent
    if actual_saving <0:
        actual_saving = 0
    target_saving = target_saving_calc(user,d_s,d_e)
    return [{"y": target_saving, "label":"Target"} , {"y": actual_saving, "label":"Actual Saving" }]

def get_target_calc(user):
    
    target_list = []

    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])        
    
    for category in categories:
        category_dict = {"category": category.categories_name}
        
        for month_no in range(1,13):
            month = month_dict[month_no]
            month_title = month_dict_add[month_no]        
            try:
                target = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,category_id = category.id, year=year , month = month)))['total'] or 0
            except Exception:
                target = 0
            if target == 0:
                continue
            category_dict[month_title] = target
        
        try:
            Category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,category_id = category.id, year=year)))['total'] or 0
            
        except Exception:
            Category_target_total = 0
        if Category_target_total == 0:
            continue 
        category_dict['Total_Target'] = round(Category_target_total,2)
        target_list.append(category_dict)   
    
    
    
    category_dict = {"category": "Total"}    
    for month_no in range(1,13):
        month = month_dict[month_no]
        month_title = month_dict_add[month_no]
        try:
            target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, month=month, year=year)))['total'] or 0
        except Exception:
            target_total = 0
        category_dict[month_title] = target_total
        
        
    try:
        target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, year=year)))['total'] or 0
            
    except Exception:
        target_total = 0
    category_dict['Total_Target'] = target_total
    target_list.append(category_dict)  
    
    
    return target_list

def get_actual_calc(user):
    
    actual_list = []

    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])        
    
    for category in categories:
        category_dict = {"category": category.categories_name}
        
        for month_no in range(1,13):
            d_s = datetime(year, month_no, 1)
            d_e = d_s + relativedelta(months=1) - timedelta(days=1)
            month_title = month_dict_add[month_no]        

            actual_total_month = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense',category_id=category ,date__range=(d_s, d_e))))['total'] or 0

            category_dict[month_title] = round(actual_total_month,2)
            
        d_s = datetime(year, 1, 1)
        d_e = datetime(year, 12, 1)

        Category_actual_annual_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, IO='expense',category_id=category ,date__range=(d_s, d_e))))['total'] or 0
         
        
        
        try:
            Category_target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user,category_id = category.id, date__range=(d_s, d_e))))['total'] or 0
            
        except Exception:
            Category_target_total = 0
            
        if Category_actual_annual_total ==0 and Category_target_total ==0:
            continue
            
        category_dict['Total_Actual'] = round(Category_actual_annual_total,2)
        category_dict['Total_Target'] = round(Category_target_total,2)
        
        if "unassigned" == category.categories_name :
            Status = "-"
        elif Category_target_total > Category_actual_annual_total:
            Status = "Under Budget"
        elif Category_target_total < Category_actual_annual_total:
            Status = "Over Budget"
        else:
            Status = "On Budget"
            
        category_dict['Status'] =  Status
          
        actual_list.append(category_dict)   
    
    
    
    category_dict = {"category": "Total"}    
    for month_no in range(1,13):
        d_s = datetime(year, month_no, 1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1)
        month_title = month_dict_add[month_no]
        actual_month_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user,IO='expense', date__range=(d_s, d_e))
                                                                & ~Q(category_id__categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])))['total'] or 0
        category_dict[month_title] = round(actual_month_total,2)
        
        
    d_s = datetime(year, 1, 1)
    d_e = datetime(year, 12, 1)       
    actual_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user,IO='expense', date__range=(d_s, d_e))
                                                      & ~Q(category_id__categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])))['total'] or 0    
    category_dict['Total_Actual'] = round(actual_total,2)
    
    try:
        target_total = budget_target.objects.aggregate(total=Sum('target', filter=Q(user_id=user, year=year)))['total'] or 0
            
    except Exception:
        target_total = 0
    category_dict['Total_Target'] = target_total
    

    if target_total > actual_total:
        Status = "Under Budget"
    elif target_total < actual_total:
        Status = "Over Budget"
    else:
        Status = "On Budget"
            
    category_dict['Status'] =  Status   
    
    actual_list.append(category_dict)  
    
    return actual_list

def annual_spentCalc(user):
    actual_list = []
    for month_no in range(1,13):
        d_s = datetime(year,month_no,1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1)
        month_title = month_dict_add[month_no]
        actual_spent = category_spent_sum(user,None,d_s,d_e)
        actual_list.append({"label": month_title, "y":actual_spent})
    return actual_list


def annual_targetCalc(user):
    target_list = []
    for month_no in range(1,13):
        month = month_dict[month_no]
        month_title = month_dict_add[month_no]
        d_s = datetime(year,month_no,1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1)
        target = category_target_sum(user,None,d_s,d_e)
        target_list.append({"label": month_title, "y":target})
    return target_list  

def annual_incomeCalc(user):
    income_list = []
    for month_no in range(1,13):
        d_s = datetime(year,month_no,1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1)
        month_title = month_dict_add[month_no]
        income = income_calc(user,d_s,d_e)
        income_list.append({"label":month_title, "y": income} )
    return income_list

def annual_saving_targetCalc(user):
    saving_target_list = []
    for month_no in range(1,13):
        d_s = datetime(year,month_no,1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1)
        month_title = month_dict_add[month_no]
        target_saving = target_saving_calc(user,d_s,d_e)
        saving_target_list.append({"label":month_title, "y": target_saving} )       
    return saving_target_list

def annual_savingCalc(user):
    saving_list = []
    for month_no in range(1,13):
        d_s = datetime(year,month_no,1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1)
        month_title = month_dict_add[month_no]
        income = income_calc(user,d_s,d_e) or 0
        actual_spent = category_spent_sum(user,None,d_s,d_e) or 0 
        actual_saving = income - actual_spent
        if actual_saving <0:
            actual_saving = 0
        saving_list.append({"label": month_title, "y": actual_saving} )    
    return saving_list

def monthly_balance_tracker(user):
    print(year)
    accounts = Accounts.objects.filter(user_id=user, account_type__in = ['Chequing','Saving'])
    accounts_balance = 0
    account__balance_list = []
    for month_no in range(1,13):
        d_s = datetime(year,month_no,1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1)
        month_title = month_dict_add[month_no]
        for account in accounts:
            
            income = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, Accounts_id =account, IO ='income',
                                                                              date__range=(d_s, d_e))))['total'] or 0
            transfer_in = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, Accounts_id =account,
                                                                                   IO='transfer-in', 
                                                                                   date__range=(d_s, d_e))))['total'] or 0
            transfer_out = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, Accounts_id =account,
                                                                                    IO='transfer-out',
                                                                                    date__range=(d_s, d_e))))['total'] or 0
        
            expense = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, Accounts_id =account,
                                                                               IO='expense', 
                                                                               date__range=(d_s, d_e))))['total'] or 0    
            
            
            accounts_balance = accounts_balance + income + transfer_in - transfer_out - expense
            
            
            if d_s.month == account.Starting_balance_date.month :
                accounts_balance = accounts_balance + account.Starting_balance
            
            
        print(month_title, accounts_balance)  
        account__balance_list.append({month_title: round(accounts_balance,2)} )
    # print(account__balance_list[0])
        
    return account__balance_list



def annual_balance_trackCalc(user):
    account__balance_list = []
    balances = monthly_balance_tracker(user)
    month_no = 1
    for month_no in range(1,13):
        month_title = month_dict_add[month_no]
        accounts_balance = balances[month_no-1][month_title]
        
        # print("current", month_no, month_title, accounts_balance)  
        if month_no == 1:
            previous_balance = accounts_balance
        else:
            month_no_prev = month_no -1
            month_title_prev = month_dict_add[month_no_prev]
            previous_balance = balances[month_no_prev-1][month_title_prev]
            # print("previous", month_no_prev, month_title_prev, previous_balance)   
         
        
        
        Variance = accounts_balance - previous_balance
        print(month_title,Variance,accounts_balance,previous_balance)  

        account__balance_list.append({"label": month_title, "y": round(Variance,2)} )    
    account__balance_list.append({"label": "Net Balance", "isCumulativeSum": True} ) 
     
    return account__balance_list

def monthly_balance_trackCalc(user):
    
    accounts = Accounts.objects.filter(user_id=user, account_type__in = ['Chequing','Saving'])
    monthly_accounts_balance = 0
    monthly_account__balance_list = []
    month_no = next(int(n) for n, m in month_dict.items() if m == month)
    d_s = datetime(year,month_no,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    month_title = month_dict_add[month_no]
    date = d_s
    monthly_accounts_balance = monthly_balance_tracker(user)[month_no-2][month_dict_add[month_no-1]]
    print(monthly_balance_tracker(user)[month_no-2])
    print(monthly_accounts_balance)
    while(date <= d_e):
        for account in accounts:  
           
            income = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, Accounts_id =account, IO ='income',
                                                                              date=date)))['total'] or 0
            transfer_in = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, Accounts_id =account,
                                                                                   IO='transfer-in', 
                                                                                   date=date)))['total'] or 0
            transfer_out = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, Accounts_id =account,
                                                                                    IO='transfer-out',
                                                                                    date=date)))['total'] or 0
        
            expense = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, Accounts_id =account,
                                                                               IO='expense', 
                                                                               date=date)))['total'] or 0
                
            monthly_accounts_balance = monthly_accounts_balance + income + transfer_in - transfer_out - expense
            if date.month == account.Starting_balance_date.month and date.day == account.Starting_balance_date.day:
                monthly_accounts_balance = monthly_accounts_balance + account.Starting_balance
        
        datedisplay = date.strftime("%b/%d")
        monthly_account__balance_list.append({"label": datedisplay, "y": round(monthly_accounts_balance,2)})           
        print(monthly_account__balance_list,monthly_account__balance_list )
        date = date +timedelta(days=1)   
         
    return monthly_account__balance_list
def total_spent_calc(user,year,month_no):
    d_s = datetime(year,month_no,1)  
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    expense = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user,
                                                                               IO='expense', 
                                                                             date__range=(d_s,d_e)) & ~Q(category_id__categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])))['total'] or 0
    sympol = "$"  
    return f"{sympol}{expense:,.2f}"

def current_balance_calc_dashboard(user):
    total_accounts_balance = update_account_balance(user)
    sympol = "$"  
    return f"{sympol}{total_accounts_balance:,.2f}"

def fixed_fees_remaining_calc(user,year, month_no):
    d_s = datetime(year,month_no,1)  
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    categories = categories_table.objects.filter(user_id=user, Fixed_fees=True) 
    fixed_fees_remaining = 0
    for category in categories:
        print(category.categories_name)
        category_spent_total = trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user, date__range=(d_s, d_e),category_id=category)))['total'] or 0
        
        if category_spent_total == 0:
            fixed_fees_remaining += budget_target.objects.aggregate(total=Sum('target',filter=Q(user_id=user,category_id=category,date__range=(d_s, d_e))))['total'] or 0 
    
    sympol = "$"  
    return f"{sympol}{fixed_fees_remaining:,.2f}"


def this_month_status_calc(user,year,month_no):
    
    d_s = datetime(year,month_no,1)  
    d_e = d_s +relativedelta(months=1)
    month = month_dict[month_no]
    days_month = d_e - timedelta(days=1)
    days_month = days_month.day
    
    status = budget_status(user,None,d_s,d_e, days_month)
    
    return status

def spent_trend(user,date):
    year = date.year
    month = date.month
    day = date.day
    date_counter = datetime(year,month,1) 
    today = datetime(year,month,day) 
    end_date = date_counter + relativedelta(months=1)-timedelta(days=1)
    spent_list = []
    expense = 0
    while (date_counter <= end_date):
    
        expense += trans.objects.aggregate(total=Sum('amount', filter=Q(user_id=user,
                                                                               IO='expense', 
                                                                               date=date_counter) & ~Q(category_id__categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])))['total'] or 0
        
        if date_counter <= today:
            cummulative_spent = round(expense,2)
        else:
            cummulative_spent = ""
            
        datedisplay = date_counter.strftime("%b/%d")
        spent_list.append({"y":cummulative_spent,"label":datedisplay})
        date_counter = date_counter +timedelta(days=1)
        
    return spent_list



def this_month_spent_percentage_calc(user,date):
    
    category_spent=[]   

    year = date.year
    month = date.month
    d_s = datetime(year,month,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    
    categories = main_category.objects.filter(user_id=user).exclude(category_name=['income','transfer','credit card payment','cashback'])
    Total_month_spent = category_main_spent_sum(user,None,d_s,d_e)
    
    if Total_month_spent == 0:
        return category_spent.append({'y': 100, 'name': "categories_name"})
    
    for category in categories:   
        category_month_spent_total = round(category_main_spent_sum(user,category,d_s,d_e)*100/Total_month_spent,2)
        category_spent.append({'y': category_month_spent_total, 'label': category.category_name})
        
    return category_spent

def this_month_spent_sub_category_calc(user,date):
    
    category_spent=[]   

    year = date.year
    month = date.month
    d_s = datetime(year,month,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income','unassigned'])  
    Total_month_spent = category_spent_sum(user,None,d_s,d_e)
    
    if Total_month_spent == 0:
        return category_spent.append({'y': 100, 'name': "categories_name"})
    
    for category in categories:   
        category_month_spent_total = round(category_spent_sum(user,category,d_s,d_e),2)
        category_month_target_total = round(category_target_sum(user,category,d_s,d_e),2)
        if category_month_spent_total ==0 and category_month_target_total ==0:
            continue
        category_spent.append({'y': category_month_spent_total, 'label': category.categories_name})
        
    return category_spent

def this_month_trans_calc(user,date):
    Trans_list=[]   
    year = date.year
    month = date.month
    d_s = datetime(year,month,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)   
    
    Transactions = trans.objects.filter(user_id=user,date__range=(d_s,d_e))
    for transaction in Transactions:
        print(transaction.date,transaction.description,transaction.amount,transaction.category_id.categories_name,transaction.IO)
        Trans_list.append({"Date":transaction.date,"Description":transaction.description,"Amount":transaction.amount
                            ,"Category":transaction.category_id.categories_name,"In/Out":transaction.IO})   
    return Trans_list

def this_month_target_calc(user,data_input):
    category_target=[]   

    year = data_input.year
    month = data_input.month
    d_s = datetime(year,month,1)
    d_e = d_s + relativedelta(months=1) - timedelta(days=1)
    
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income','refund or cashback','transfer','income','unassigned'])    
    
    for category in categories:   
        category_month_spent_total = round(category_spent_sum(user,category,d_s,d_e),2)
        category_month_target_total = round(category_target_sum(user,category,d_s,d_e),2)
        remaining = category_month_target_total - category_month_spent_total
        if remaining < 0:
            remaining = 0
        if category_month_spent_total ==0 and category_month_target_total ==0:
            continue
        category_target.append({'y': remaining, 'label': category.categories_name})
    return  category_target

# def this_month_spent_sub_category_percentage_inverse_calc(user,date):
#     # spent_categories= this_month_spent_sub_category_percentage_calc(user,date)
#     spent_categories_Target = []
#     spent_categories= this_month_spent_sub_category_percentage_calc(user,date)
#     target = this_month_target_calc(user,date)
#     for spent_category in spent_categories:
#     #     spent_categories_inverse_list.append({"y":100-spent_category['y'],"label":spent_category['label']})
#     return spent_categories_Target

# Create your views here.
@login_required(login_url="/users/loginpage/")
def monthly_view(request):
    user = request.user
    global year
    global month
    global month_no
    year = date.today().year
    month_no = date.today().month
    month = month_dict[month_no]
    if request.method == 'POST':
        year = request.POST.get('year')
        year = int(year)
        month = request.POST.get('month')
        request.session["selected_year"] = year
        request.session["selected_month"] = month
    else:
        year = request.session.get("selected_year", year)
        month = request.session.get("selected_month", month)
    
    # categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    # category_list = ["Overall"]
    # for category in categories:
    #     category_list.append(category.categories_name)
    # selected_category = request.session.get("selected_category", "Overall")
    
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
    
    
    context = {
        'years': year_list,
        'months':month_list,
        "selected_year": year,
        "selected_month": month,
        'Month':month,
        # "categories":category_list,
        # "selected_category":selected_category,
        "isfamily":isfamily
    }  
    
    return render(request, 'expense/monthly.html',  context)


def Expected_income_calc(user):
    Expected_income_list =[]      
    print(year) 
    for month_no in range(1,13):
        d_s = datetime(year,month_no,1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1) 
        month_title = month_dict_add[month_no]
        Expected_income = expectedIncome.objects.aggregate(total=Sum('Expected_income', filter=Q(user_id=user,date__range=(d_s,d_e))))['total'] or 0
        
        Expected_income_list.append({"label": month_title, "y": round(Expected_income,2)} )    
     
    return Expected_income_list
    


def Expected_Saving_calc(user):
    Expected_saving_list =[]   
    for month_no in range(1,13):
        d_s = datetime(year,month_no,1)
        d_e = d_s + relativedelta(months=1) - timedelta(days=1) 
        month_title = month_dict_add[month_no]
        target = category_target_sum(user,None,d_s,d_e)
        Expected_income = expectedIncome.objects.aggregate(total=Sum('Expected_income', filter=Q(user_id=user,date__range=(d_s,d_e))))['total'] or 0
        Expected_saving = Expected_income - target
        if Expected_saving <0:
            Expected_saving = 0
        Expected_saving_list.append({"label": month_title, "y": round(Expected_saving,2)}) 
    return Expected_saving_list




@login_required(login_url="/users/loginpage/")
def monthly_get(request):    
    return JsonResponse(getMonthlyView(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def category_spent(request):    
    return JsonResponse(category_spent_pichart(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def category_spent_amounts(request):    
    return JsonResponse(category_pent_bar(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def category_spent_daily(request):    
    return JsonResponse(category_spent_bar_daily(request.user), safe=False)
      
@login_required(login_url="/users/loginpage/")
def annual_target_view(request):
    user = request.user
    global year

    year = date.today().year
    if request.method == 'POST':
        year = request.POST.get('year')
        year = int(year)
        request.session["selected_year"] = year
    else:
        year = request.session.get("selected_year", year)
    
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    category_list = ["Overall"]
    for category in categories:
        category_list.append(category.categories_name)
    selected_category = request.session.get("selected_category", "Overall")
    
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
    
    context = {
        'years': year_list,
        "selected_year": year,
        "categories":category_list,
        "selected_category":selected_category,
        "isfamily":isfamily
    }  
    return render(request, 'expense/annually_target.html', context)

@login_required(login_url="/users/loginpage/")
def annual_get_target(request):
    return JsonResponse(get_target_calc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def category_get_view(request):
    global category_view
    category_view ='Overall'
    if request.method=="POST":
        data = json.loads(request.body)
        category_view = data.get('category_view')
        request.session["selected_category"] = category_view
        return JsonResponse({'status': 'success'})
    else:
        category_view =  request.session.get("selected_category","Overall")
        return JsonResponse({'selected_category': category_view})

@login_required(login_url="/users/loginpage/")
def spentvstarget(request):
    return JsonResponse(spentVstargetCalc(request.user), safe=False)
    
    
@login_required(login_url="/users/loginpage/")
def incomevsspent(request):
    return JsonResponse(incomeVsspentCalc(request.user), safe=False)
    
    
@login_required(login_url="/users/loginpage/")
def savingvstarget(request):
    return JsonResponse(savingVstargetCalc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def annual_actual_view(request):
    user = request.user
    global year
    year = date.today().year
    if request.method == 'POST':
        year = request.POST.get('year')
        year = int(year)
        request.session["selected_year"] = year
    else:
        year = request.session.get("selected_year", year)
    
    categories = categories_table.objects.filter(user_id=user).exclude(categories_name__in=['credit card payment', 'refund or cashback','transfer','income'])
    category_list = ["Overall"]
    for category in categories:
        category_list.append(category.categories_name)
    selected_category = request.session.get("selected_category", "Overall")
    
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
    
    
    context = {
        'years': year_list,
        "selected_year": year,
        "categories":category_list,
        "selected_category":selected_category,
        "isfamily":isfamily
    }  
    return render(request, 'expense/annually_actual.html', context)

@login_required(login_url="/users/loginpage/")
def annual_get_actual(request):
    return JsonResponse(get_actual_calc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def annual_spent(request):
    return JsonResponse(annual_spentCalc(request.user), safe=False)
    
    
@login_required(login_url="/users/loginpage/")
def annual_target(request):
    return JsonResponse(annual_targetCalc(request.user), safe=False)
    
    
@login_required(login_url="/users/loginpage/")
def annual_income(request):
    return JsonResponse(annual_incomeCalc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def annual_saving_target(request):
    return JsonResponse(annual_saving_targetCalc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def annual_saving(request):
    return JsonResponse(annual_savingCalc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def balance_track_annual(request):
    return JsonResponse(annual_balance_trackCalc(request.user), safe=False)
@login_required(login_url="/users/loginpage/")
def balance_track_monthly(request):
    return JsonResponse(monthly_balance_trackCalc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def dashboard_view(request):
    user=request.user
    month_no = date.today().month
    month= month_dict[month_no]
    user_name = request.user.first_name
    today_date= date.today()
    displayDate = today_date.strftime("%d %b, %Y")
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
    context ={
        "user_name" : user_name,
        "displayDate":displayDate,
        "month":month,
        "isfamily": isfamily
    }
    return render(request,"expense/dashboard.html",context)

@login_required(login_url="/users/loginpage/")
def total_spent(request):
    year = date.today().year
    month_no = date.today().month
    return JsonResponse(total_spent_calc(request.user,year,month_no), safe=False)

@login_required(login_url="/users/loginpage/")
def total_spent(request):
    year = date.today().year
    month_no = date.today().month
    return JsonResponse(total_spent_calc(request.user,year,month_no), safe=False)

@login_required(login_url="/users/loginpage/")
def current_balance(request):
    return JsonResponse(current_balance_calc_dashboard(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def fixed_fees_remaining(request):
    year = date.today().year
    month_no = date.today().month
    return JsonResponse(fixed_fees_remaining_calc(request.user,year,month_no), safe=False)


@login_required(login_url="/users/loginpage/")
def this_month_status(request):
    year = date.today().year
    month_no = date.today().month
    return JsonResponse(this_month_status_calc(request.user,year,month_no), safe=False)

@login_required(login_url="/users/loginpage/")
def this_month_spent_trend(request):
    return JsonResponse(spent_trend(request.user,date.today()), safe=False)

@login_required(login_url="/users/loginpage/")
def this_month_spent_percentage(request):
    return JsonResponse(this_month_spent_percentage_calc(request.user,date.today()), safe=False)


@login_required(login_url="/users/loginpage/")
def this_month_trans(request):
    return JsonResponse(this_month_trans_calc(request.user,date.today()), safe=False)

@login_required(login_url="/users/loginpage/")
def this_month_spent_percentage_inverse(request):
    return JsonResponse(this_month_target_calc(request.user,date.today()), safe=False)

@login_required(login_url="/users/loginpage/")
def this_month_spent_sub_categ_percentage(request):
    return JsonResponse(this_month_spent_sub_category_calc(request.user,date.today()), safe=False)

@login_required(login_url="/users/loginpage/")
def Expected_income_get(request):
    return JsonResponse(Expected_income_calc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def Expected_Saving_get(request):
    return JsonResponse(Expected_Saving_calc(request.user), safe=False)

@login_required(login_url="/users/loginpage/")
def Saving_goal(request):
    user =request.user
    savings = SavingGoal.objects.filter(user_id=user)
    today_date= date.today()
    displayDate = today_date.strftime("%d %b, %Y")
    goal_target = 0
    goal_due_date = ""
    Remaining = 0
    status = ""
    account_current_balance = 0
    goal_name = ""
    
    if request.method == 'POST':
        global Goal_id
        Goal_id = request.POST.get('Saving_goal')
        if not Goal_id:
            return redirect('Saving_goal')
        
        goal = SavingGoal.objects.get(user_id=user,id=Goal_id)
        goal_name = goal.Goal_name
        goal_target = goal.Goal
        goal_due_date = goal.due_date
        goal_created_on = goal.create_date
        account_current_balance = goal.Account.Balance
        Remaining = goal_target - account_current_balance
        
        if Remaining >= goal_target:
            Remaining = 0
        
        status =Target_status(goal_due_date,today_date,goal_created_on,Remaining,goal_target)  
    sympol = "$" 
    
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
    
    
    context={
        "Goal_name": goal_name,
        "savings": savings,
        "today_date":displayDate,
        "target": f"{sympol}{goal_target:,.2f}",
        "current_balance": f"{sympol}{account_current_balance:,.2f}",
        "duedate":goal_due_date,
        "remaining": f"{sympol}{Remaining:,.2f}",
        "status" : status,
        "isfamily":isfamily
    }
    return render(request,"expense/savingGoal_view.html",context)

@login_required(login_url="/users/loginpage/")
def saving_goal_progress(request):
    return JsonResponse(saving_goal_progresscalc(request.user,Goal_id),safe=False)


def saving_goal_progresscalc(user,goal_id):
    if goal_id:
        goal = SavingGoal.objects.get(user_id=user,id=Goal_id)
        goal_target = goal.Goal
        account_current_balance = goal.Account.Balance
        Remaining = goal_target - account_current_balance
        
        account_current_balance_perc = account_current_balance*100/goal_target
        Remaining_perc = Remaining*100/goal_target
    
        return [{'y': account_current_balance_perc, 'label': 'Current balabce'}, {'y': Remaining_perc, 'label': 'Remaining'}]
    return 

    
def Target_status(goal_due_date,today_date,goal_created_on,Remaining,goal_target):
    if Remaining == 0:
        target_status = "Goal Complete"
    else:
        days_to_target = (goal_due_date - goal_created_on).days 
        days_to_ramaining = (goal_due_date - today_date).days
        print(days_to_target,days_to_ramaining)
        if Remaining/days_to_ramaining > goal_target/days_to_target:
            target_status = "Not on Track"
        else:
            target_status = "On Track"
    
    return target_status

@login_required(login_url="/users/loginpage/")
def accounts_view(request):
    return render(request,"expense/account_view.html")
