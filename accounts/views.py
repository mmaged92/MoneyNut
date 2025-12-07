from django.shortcuts import render, redirect
from .models import Accounts, Bank
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import datetime, timedelta
from trans.models import trans
from django.db.models import Q, Sum
from family.models import familyMemebers

# Create your views here.

accounts = ['Chequing', 'Saving', 'Credit', 'line of credit', 'cash']

banks_in_canada = [
    "Royal Bank of Canada (RBC)",
    "Toronto-Dominion Bank (TD)",
    "Bank of Nova Scotia (Scotiabank)",
    "Bank of Montreal (BMO)",
    "Canadian Imperial Bank of Commerce (CIBC)",
    "National Bank of Canada",
    "Laurentian Bank of Canada",
    "HSBC Bank Canada (now part of RBC, 2024)",
    "Canadian Western Bank",
    "EQ Bank",
    "Tangerine Bank",
    "Simplii Financial",
    "Desjardins Group",
    "ATB Financial",
    "Manulife Bank of Canada",
    "PC Financial",
    "Wealth One Bank of Canada",
    "First Nations Bank of Canada",
    "Home Trust Company",
    "Bridgewater Bank",
    "Cash"
]



        

@login_required(login_url="/users/loginpage/")
def add_account(request):
    if request.user.is_authenticated:
            user = request.user
    
    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = None

    
    for bank in banks_in_canada:
        if not Bank.objects.filter(user_id = user, Bank=bank).exists():
            Bank.objects.create(user_id = user, Bank=bank,family_id=family_id)
            
    if request.method == "POST":
        account_type = request.POST.get('account_type')
        Bank_name = request.POST.get('Bank_name')
        account_name = request.POST.get('account_name')
        if not account_type or not Bank_name or not account_name:
            return redirect('add_account') 
        
        Bank_id = Bank.objects.get(Bank=Bank_name)
        if account_type == 'Saving' or account_type == 'Chequing':
            account_number = request.POST.get('account_number')
            Starting_balance = request.POST.get('account_balance')
            Starting_balance_date = request.POST.get('account_balance_date')
            if not account_number or not Starting_balance or not Starting_balance_date:
                if not account_number:
                    account_number = ""
                if not Starting_balance:
                    Starting_balance = 0
                if not Starting_balance_date:
                    Starting_balance_date = datetime.today()
            
            Accounts.objects.create(user_id=user,Bank=Bank_id,account_type=account_type,account_name=account_name,account_number=account_number,Starting_balance=Starting_balance, Starting_balance_date=Starting_balance_date,family_id=family_id)
            return redirect('add_account')        
        
        if  account_type == 'cash':
            Starting_balance = request.POST.get('account_balance')
            Starting_balance_date = request.POST.get('account_balance_date')      
            if not Starting_balance or not Starting_balance_date:
                if not Starting_balance:
                    Starting_balance = 0
                if not Starting_balance_date:
                    Starting_balance_date = datetime.today() 
            account_number = ""
            Accounts.objects.create(user_id=user,Bank=Bank_id,account_type=account_type,account_name=account_name, Starting_balance=Starting_balance, Starting_balance_date=Starting_balance_date,family_id=family_id)
            return redirect('add_account')        
             
        if  account_type == 'Credit' or account_type == 'line of credit':    
            account_number = request.POST.get('account_number')
            if not account_number:
                account_number = None
            Starting_balance = 0
            Starting_balance_date = None
            Accounts.objects.create(user_id=user,Bank=Bank_id,account_type=account_type,account_name=account_name,account_number=account_number,Starting_balance=Starting_balance,family_id=family_id)
            return redirect('add_account')             
        
        
    update_account_balance(user)

    Banks = Bank.objects.filter(user_id=user)
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
        
    
    return render(request, 'account/account.html',{'Banks':Banks, 'accounts':accounts,'isfamily':isfamily})


@login_required(login_url="/users/loginpage/")
def add_bank(request):
    user = request.user
    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = ""
    if request.method == "POST":
        Bank_new = request.POST.get('Bank_new')
        if not Bank_new:
            return redirect("add_bank")
        if not Bank.objects.filter(user_id = user, Bank=Bank_new):
            Bank.objects.create(user_id = user, Bank=Bank_new,family_id=family_id)
            return redirect('add_bank')  
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
        
    return render(request, 'account/banks.html',{"isfamily":isfamily})


@login_required(login_url="/users/loginpage/")
def get_banks(request):
    user = request.user
    Banks = Bank.objects.filter(user_id=user)
    bank_list = []
    for bank in Banks:
        bank_list.append({'Bank': bank.Bank, 'Bank_id':bank.id})
    return JsonResponse(bank_list, safe=False)

@login_required(login_url="/users/loginpage/")
def update_banks(request):
    user = request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        Bank_id = data.get('Bank_id')
        print(newvalue)
        print(Bank_id)
        update = Bank.objects.get(user_id=user,id=Bank_id)
        update.Bank = newvalue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newvalue})
    return JsonResponse({"error":"invalid method"})

@login_required(login_url="/users/loginpage/")
def delete_banks(request):
    user = request.user
    if request.method == 'DELETE':
        data = json.loads(request.body)
        Bank_id = data.get('BanK_id')
        print(Bank_id)
        try:
            update = Bank.objects.get(user_id=user,id=Bank_id)
            update.delete()
        except:
            for id in Bank_id:
                update = Bank.objects.get(user_id=user,id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)   

@login_required(login_url="/users/loginpage/")
def get_accounts(request):
    user = request.user
    accounts = Accounts.objects.filter(user_id=user)
    accounts_list = []
    for account in accounts:
        accounts_list.append({'Bank':account.Bank.Bank ,'account_type':account.account_type,'account_name':account.account_name,
                              'account_number':account.account_number,'Starting_balance':account.Starting_balance ,'account_balance':account.Balance, 
                              'account_balance_start_date':account.Starting_balance_date,'account_id':account.id})
    return JsonResponse(accounts_list, safe=False)

@login_required(login_url="/users/loginpage/")

def bank_get(request):
    user = request.user
    Banks = Bank.objects.filter(user_id=user)
    bank_list = []
    for bank in Banks:
        bank_list.append(bank.Bank)
    return JsonResponse(bank_list, safe=False)

@login_required(login_url="/users/loginpage/")
def accounttype_get(request):
    return JsonResponse(accounts, safe=False)

@login_required(login_url="/users/loginpage/")
def accountname_update(request):
    user = request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        update = Accounts.objects.get(user_id=user,id=account_id)
        update.account_name = newvalue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newvalue})
    return JsonResponse({"error":"invalid method"})

@login_required(login_url="/users/loginpage/")
def accounttype_update(request):
    user = request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        update = Accounts.objects.get(user_id=user,id=account_id)
        update.account_type = newvalue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newvalue})
    return JsonResponse({"error":"invalid method"})

@login_required(login_url="/users/loginpage/")
def accountnumber_update(request):
    user = request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        update = Accounts.objects.get(user_id=user,id=account_id)
        update.account_number = newvalue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newvalue})
    return JsonResponse({"error":"invalid method"})

@login_required(login_url="/users/loginpage/")
def accountbalancestart_update(request):
    user = request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        update = Accounts.objects.get(user_id=user,id=account_id)
        update.Starting_balance = newvalue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newvalue})
    return JsonResponse({"error":"invalid method"})

@login_required(login_url="/users/loginpage/")
def accountbalance_update(request):
    user = request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        update = Accounts.objects.get(user_id=user,id=account_id)
        update.Balance = newvalue
        update.save()
        return JsonResponse({'status': 'updated','newValue':newvalue})
    return JsonResponse({"error":"invalid method"})

@login_required(login_url="/users/loginpage/")
def account_date_update(request):
    user = request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        # newvalue = datetime.strptime(newvalue, "%Y-%m-%dT%H:%M:%S.%fZ")
        # new_date = newvalue.strftime("%Y-%m-%d")
        # print(new_date)
        print(account_id)
        if newvalue == "" or newvalue == None:
            newvalue = None
        update = Accounts.objects.get(user_id=user,id=account_id)
        update.Starting_balance_date = newvalue
        update.save()
        print(update.Starting_balance_date)
        return JsonResponse({'status': 'updated','newValue':newvalue})
    return JsonResponse({"error":"invalid method"})

@login_required(login_url="/users/loginpage/")
def bank_update(request):
    user = request.user
    if request.method == 'PUT':
        data = json.loads(request.body)
        newvalue = data.get('newValue')
        account_id = data.get('account_id')
        print(newvalue)
        print(account_id)
        bankNew = Bank.objects.get(user_id=user,Bank=newvalue)
        update = Accounts.objects.get(user_id=user,id=account_id)
        update.Bank = bankNew
        update.save()
        return JsonResponse({'status': 'updated','newValue':newvalue})
    return JsonResponse({"error":"invalid method"})

@login_required(login_url="/users/loginpage/")
def delete_accounts(request):
    user = request.user
    if request.method == 'DELETE':
        data = json.loads(request.body)
        target_id = data.get('account_id')
        try:
            update = Accounts.objects.get(user_id=user,id=target_id)
            update.delete()
        except:
            for id in target_id:
                update = Accounts.objects.get(id=id)
                update.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)   

def update_account_balance(user):
    try: 
        accounts = Accounts.objects.filter(user_id=user, account_type__in = ['Chequing','Saving'])
    except Exception:
            return

    account_balance = 0
    total_account_balance = 0
    for account in accounts: 
        try: 
            date = datetime(account.Starting_balance_date.year,account.Starting_balance_date.month,account.Starting_balance_date.day)
        except Exception:
            return
            
        date_end= date.today()
        account_balance = account.Starting_balance
        while(date <= date_end):   
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
                
            account_balance = account_balance + income + transfer_in - transfer_out - expense           
            date = date +timedelta(days=1)  
        account.Balance = round(account_balance,2)
        total_account_balance += account_balance
        account.save()
    
    return total_account_balance
         