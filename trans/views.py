from django.shortcuts import render, redirect
from .models import trans, categorization,FileMapping
import csv
from django.http import JsonResponse
from target.models import categories_table, main_category
from accounts.models import Bank, Accounts
from datetime import datetime, timedelta
from django.core import serializers
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
import pandas as pd
import io
from datetime import datetime
from family.models import familyMemebers


# file_path = 'C:/Users/mahmo/OneDrive/Desktop/Budget/keyword.csv'
# with open(file_path, newline='', encoding='utf-8-sig' ) as csvfile:
#     reader = csv.DictReader(csvfile) 
#     for row in reader:
#         print(row['keyword'], row['category'])
#         keyword = row['keyword']
#         category_id = categories_table.objects.get(id=row['category'])  
#         categorization.objects.create(user_id=1, keyword=keyword, category_id = category_id)

ios = ['income', 'expense', 'credit card payment', 'refund or cashback', 'transfer-in','transfer-out']
card_types = ['Credit' , 'Debit']
accounts = ['Chequing', ' Saving', 'Credit']

@login_required(login_url="/users/loginpage/")
def trans_add(request):
    user = request.user
    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = None
    
    if request.method == "POST":
        input_type = request.POST.get('input_type')
        if input_type =='file_upload':
            # Date_column_name = request.POST.get("Date_column_name")
            # Description_column_name = request.POST.get("Description_column_name")
            # Amount_column_name = request.POST.get("Amount_column_name")
            # if not Date_column_name:
            #     Date_column_name = "Date"
            # if not Date_column_name:
            #     Description_column_name = "Description"
            # if not Amount_column_name:
            #     Amount_column_name = "Amount"                     
            
            card_type = request.POST.get('card_type')
            account_name = request.POST.get('account_name')
            
            file_path = request.FILES['file_path']
            
            if not file_path or not account_name or not card_type:
                return redirect("trans_page")

            decoded_file = file_path.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file)
            rows = list(reader)

            account_id = Accounts.objects.get(user_id = user, account_name=account_name)
            if FileMapping.objects.filter(account_id=account_id).exists():
                file_mapping = FileMapping.objects.get(account_id=account_id)
                Date_column_name = file_mapping.Date_header_name
                Description_column_name = file_mapping.Description_header_name
                Amount_column_name = file_mapping.Amount_header_name
            else:
                print("file mapping required")
                categories = categories_table.objects.filter(user_id=user)
                account_names = Accounts.objects.filter(user_id=user)
    
                if familyMemebers.objects.filter(user_id=user).exists():
                    isfamily = True
                else:
                    isfamily = False
                context = {
                        'card_types': card_types, 'categories':categories, 'ios':ios, 'account_names':account_names,"isfamily":isfamily,"mapping_required": True
                }
                return render(request, 'trans/trans.html', context)
            
            amount_inversed = False
            
        # file_path = 'C:/Users/mahmo/OneDrive/Desktop/Budget/Scotia_Momentum_VISA_card_4023_092825.csv'
            try:
                # with open(file_path, newline='') as csvfile:
                #     reader = csv.DictReader(csvfile)
                for row in rows:
                    amount  = row[Amount_column_name] if row['Amount'].strip() != '' else 0.0
                    try:
                        amount =float(amount)
                    except Exception:
                        amount = amount.replace("$", "").replace(",", "")
                        amount = float(amount) 
                    if card_type == 'Credit' and amount > 0 and ('thank you' in row[Description_column_name].lower()  or 'payment' in row[Description_column_name].lower()):
                        amount_inversed = True
                        break
                
                      
                for row in rows:

                    # if not trans.objects.filter(user_id=1, description=row['Description'],date=row['Date'],amount=row['Amount']).exists():
                        amount = row[Amount_column_name]
                        try:
                            amount =float(amount)
                        except Exception:
                            amount = amount.replace("$", "").replace(",", "")
                            amount =float(amount)
                        keywords = categorization.objects.filter(user_id=user)
                        matched = False
                        
                        for keyword in keywords:
                            if keyword.keyword.lower() in row[Description_column_name].lower():
                                matched =True
                                break
                        
                        if matched:
                            category = keyword.category_id
                            category_main = keyword.category_id.main_category_id
                        else:
                            category_name = categories_table.objects.get(user_id=user,categories_name='unassigned')
                            category = category_name  
                            category_main = main_category.objects.get(user_id=user,category_name='unassigned')
                            

                        
                        
                        if card_type == 'Credit' and ('thank you' in row[Description_column_name].lower() or 'payment' in row[Description_column_name].lower()):
                            category = 'credit card payment'
                            category_main = 'credit card payment'
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category = categories_table.objects.get(user_id=user,categories_name=category)
                            IO = 'credit card payment'
                        elif card_type == 'Credit' and amount < 0 and amount_inversed == False:
                            category = 'refund or cashback'
                            category_main = 'cashback'
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category = categories_table.objects.get(user_id=user,categories_name=category)
                            IO = 'income'
                        elif card_type == 'Credit' and amount > 0 and amount_inversed == False:
                            IO = 'expense'
                        elif card_type == 'Credit' and amount > 0 and amount_inversed == True:
                            category = 'refund or cashback'
                            category_main = 'cashback'
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category = categories_table.objects.get(user_id=user,categories_name=category)
                            IO = 'income'
                        elif card_type == 'Credit' and amount < 0 and amount_inversed == True:
                            IO = 'expense'
                        elif card_type == 'Debit' and ('visa' in row[Description_column_name].lower() or 'mastercard' in row[Description_column_name].lower() or 'neo' in row[Description_column_name].lower() ):
                            IO = 'expense'
                            category = 'credit card payment'
                            category_main = 'credit card payment'
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category = categories_table.objects.get(user_id=user,categories_name=category)
                        elif card_type == 'Debit' and amount < 0 and 'e-transfer' in row[Description_column_name].lower():
                            IO = 'expense'
                            category = 'unassigned'
                            category_main = main_category.objects.get(user_id=user,category_name='unassigned')
                            category = categories_table.objects.get(user_id=user,categories_name=category) 
                        elif card_type == 'Debit' and amount > 0 and 'e-transfer' in row[Description_column_name].lower():
                            IO = 'income'
                            category = 'income'
                            category_main = 'income'
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category = categories_table.objects.get(user_id=user,categories_name=category) 
                            print(10, category.categories_name)
                        elif card_type == 'Debit' and amount < 0 and 'transfer' in row[Description_column_name].lower() and 'e-transfer' not in row[Description_column_name].lower() :
                            IO = 'transfer-out'
                            category = 'transfer'
                            category_main = 'transfer'
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category = categories_table.objects.get(user_id=user,categories_name=category) 
                            print(11, category.categories_name)
                        elif card_type == 'Debit' and amount > 0 and 'transfer' in row[Description_column_name].lower() and 'e-transfer' not in row[Description_column_name].lower() :
                            IO = 'transfer-in'
                            category = 'transfer'
                            category_main = 'transfer'
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category = categories_table.objects.get(user_id=user,categories_name=category) 
                            print(12, category.categories_name)
                            
                        elif card_type == 'Debit' and amount < 0:
                            IO = 'expense'
                        else:
                            IO = 'income'
                            category = 'income'
                            category_main = 'income'
                            category_main = main_category.objects.get(user_id=user,category_name=category_main)
                            category = categories_table.objects.get(user_id=user,categories_name=category) 
                        
                        try:
                            date = datetime.strptime(row[Date_column_name], "%m/%d/%Y")
                            date = date.strftime("%Y-%m-%d")
                        except ValueError:
                            date = row[Date_column_name]
                        
                        print("Success")
                        if not trans.objects.filter(user_id=user,description=row[Description_column_name],date=date,amount=abs(amount), category_id = category, main_category_id=category_main, IO = IO, Accounts_id= account_id).exists():
                            trans.objects.create(user_id=user,description=row[Description_column_name],date=date,amount=abs(amount), category_id = category,main_category_id=category_main, IO = IO, Accounts_id= account_id, family_id=family_id)
                            print("")
                print("Success")
            except Exception:
                print("failed")
                return redirect("trans_page")
            
            
        if input_type =='single_entry':  
            user = request.user
            description = request.POST.get('description')
            date = request.POST.get('date')
            amount = request.POST.get('amount')
            category = request.POST.get('category')

            account_name = request.POST.get('account_name_se')
            IO = request.POST.get('IO')
            
            if not description or not date or not amount or not category or not account_name or not IO:
                return redirect("trans_page")
            
            account_id = Accounts.objects.get(user_id=user,account_name=account_name)
            
            try:
                category = categories_table.objects.get(user_id=user,categories_name=category)
                category_main = category.main_category_id
            except Exception:
                category_name = categories_table.objects.get(user_id=user,categories_name='unassigned')
                category = category_name
                category_main = main_category.objects.get(user_id=user,category_name='unassigned')
            if familyMemebers.objects.filter(user_id=user).exists():
                family_id = familyMemebers.objects.get(user_id=user)
                family_id = family_id.family_id
            else:
                family_id = None     
            if not trans.objects.filter(user_id=user, description=description,date=date,amount=amount, category_id = category,main_category_id= category_main,IO = IO, Accounts_id=account_id).exists():
                trans.objects.create(user_id=user,description=description,date=date,amount=amount, category_id = category,main_category_id= category_main ,IO = IO, Accounts_id=account_id, family_id=family_id)

            
    categories = categories_table.objects.filter(user_id=user)
    account_names = Accounts.objects.filter(user_id=user)
    
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
       
    context = {
        'card_types': card_types, 'categories':categories, 'ios':ios, 'account_names':account_names,"isfamily":isfamily
    }
    return render(request, 'trans/trans.html', context)

@login_required(login_url="/users/loginpage/")
def trans_edit(request):
    print(request)
    return JsonResponse({}, status=405)

@login_required(login_url="/users/loginpage/")
def trans_all(request):
    user = request.user
    transactions = trans.objects.filter(user_id=user)
    
    transactions_list = []
    for transaction in transactions:
        
        try: 
            main_category = transaction.main_category_id.category_name
        except Exception:
            main_category = "*********"
        
        
        
        if transaction.category_id == None:
            transactions_list.append({'Description': transaction.description, "Date": transaction.date, "Amount":transaction.amount, "IO":transaction.IO
                                  , "Bank":transaction.Accounts_id.account_name,"Category":'***********',"Category_Main":main_category,
                                  "Account Name":transaction.Accounts_id.account_name, "Account Number": transaction.Accounts_id.account_number,"Account Type":transaction.Accounts_id.account_type,
                                  "Bank":transaction.Accounts_id.Bank.Bank,"category_id":"", "transaction_id":transaction.id, "Account_id":transaction.Accounts_id.id})
        else:
            transactions_list.append({'Description': transaction.description, "Date": transaction.date, "Amount":transaction.amount, "IO":transaction.IO
                                  , "Bank":transaction.Accounts_id.account_name,"Category":transaction.category_id.categories_name,"Category_Main":main_category,
                                  "Account Name":transaction.Accounts_id.account_name,"Account Number":transaction.Accounts_id.account_number, "Account Type":transaction.Accounts_id.account_type,
                                  "Bank":transaction.Accounts_id.Bank.Bank,"category_id":transaction.category_id.id, "transaction_id":transaction.id, "Account_id":transaction.Accounts_id.id})
    return JsonResponse(transactions_list, safe=False)

@login_required(login_url="/users/loginpage/")

def trans_view(request):
    user= request.user
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False
    
    
    return render(request, 'trans/view.html',{"isfamily":isfamily})

@login_required(login_url="/users/loginpage/")
def Account_get(request):
    user = request.user
    accounts = Accounts.objects.filter(user_id=user)
    account_list = []
    for account in accounts:
        account_list.append(account.account_name)
    return JsonResponse(account_list, safe=False)


@login_required(login_url="/users/loginpage/")
def IO_get(request):
    return JsonResponse(ios, safe=False)

@login_required(login_url="/users/loginpage/")
def description_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        update_value = trans.objects.get(id=transaction_id)
        update_value.description = new_value
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def date_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        update_value = trans.objects.get(id=transaction_id)
        update_value.date = new_value
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def amount_update(request):
    if request.method =='PUT':
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        update_value = trans.objects.get(id=transaction_id)
        update_value.amount = new_value
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def category_update(request):
    user=request.user
    if request.method =='PUT':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        
        update_value = trans.objects.get(id=transaction_id)
        new_category_id = categories_table.objects.get(user_id=user,categories_name=new_value)
        update_value.category_id = new_category_id
        if new_value == 'income':
            IO = 'income'
            update_value.IO = IO
        if new_value not in ['income', 'transfer']:
            IO = 'expense'
            update_value.IO = IO
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def IO_update(request):
    
    if request.method =='PUT':
        user=request.user
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')
        update_value = trans.objects.get(id=transaction_id)
        update_value.IO = new_value
        if new_value == 'income':
            category = categories_table.objects.get(user_id=user,categories_name="income")
            update_value.category_id = category
        if new_value == 'expense':
            category = categories_table.objects.get(user_id=user,categories_name="unassigned")
            update_value.category_id = category
        update_value.save()

        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def account_update(request):
    if request.method =='PUT':
        user = request.user
        data = json.loads(request.body)
        Account_id = data.get('Account_id')
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')

        update_value = trans.objects.get(id=transaction_id)
        new_account_id = Accounts.objects.get(user_id=user,account_name=new_value)
        update_value.Accounts_id = new_account_id
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def date_update(request):
    if request.method =='PUT':
        user = request.user
        data = json.loads(request.body)
        new_value = data.get('new_value')
        transaction_id = data.get('transaction_id')

        update_value = trans.objects.get(id=transaction_id)
        update_value.date = new_value
        update_value.save()
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def transaction_delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        # print(data)
        transaction_id = data.get('transaction_id')

        try:
            trans_delete = trans.objects.get(id=transaction_id)
            trans_delete.delete()
        except:
            for id in transaction_id:
                trans_delete = trans.objects.get(id=id)
                trans_delete.delete()

        return JsonResponse({'status': 'deleted', 'keyword_id': transaction_id})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def keyword_insert(request):
    user = request.user
    if familyMemebers.objects.filter(user_id=user).exists():
        family_id = familyMemebers.objects.get(user_id=user)
        family_id = family_id.family_id
    else:
        family_id = None   
    if request.method == "POST":
        keyword = request.POST.get('new_keyword')
        category_id = request.POST.get('category_id')
        if not keyword or not category_id:
            return redirect("keyword")
        if keyword and category_id:
            category_id = categories_table.objects.get(id=category_id)
            if not categorization.objects.filter(user_id=user,keyword=keyword, category_id = category_id).exists():    
                categorization.objects.create(user_id=user,keyword=keyword, category_id = category_id,family_id=family_id)
        else:
            print("error") # insert message error


        
    category_list = categories_table.objects.filter(user_id=user)
    if familyMemebers.objects.filter(user_id=user).exists():
        isfamily = True
    else:
        isfamily = False

    return render(request, 'trans/keyword.html', { 'category_list' : category_list,"isfamily":isfamily})

@login_required(login_url="/users/loginpage/")
def keyword_all(request):
    user = request.user
    keywords = categorization.objects.filter(user_id=user)
    keywords_dic =[]
    for keyword in keywords:
        keywords_dic.append({"keyword_id":keyword.id,"keyword":keyword.keyword, "category_id":keyword.category_id.id, "category":keyword.category_id.categories_name})

    return JsonResponse(keywords_dic, safe=False)

@login_required(login_url="/users/loginpage/")
def keyword_delete(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        keyword_id = data.get('keyword_id')
        print(type(keyword_id))
        try:
            category_delete = categorization.objects.get(id=keyword_id)
            category_delete.delete()
        except:
            for id in keyword_id:
                category_delete = categorization.objects.get(id=id)
                category_delete.delete()
        user = request.user
        transactions = trans.objects.filter(user_id=user)
        for transaction in transactions:
            description = transaction.description
            try:
                category_name = categorization.objects.get(user_id=user,keyword__contains=description)
                category = category_name.category_id
                transaction.category_id = category
                transaction.save()
            except Exception:
                category = None   
                transaction.category_id = None
                transaction.save()  
        return JsonResponse({'status': 'deleted', 'keyword_id': keyword_id})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def keyword_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        print(data)
        keyword_id = data.get('keyword_id')
        new_value = data.get('new_value')
        print(keyword_id)
        print(new_value)

        category_update = categorization.objects.get(id=keyword_id)
        category_update.keyword = new_value
        category_update.save()
                
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def keyword_category_get(request):
    user = request.user
    category_list = categories_table.objects.filter(user_id=user)
    category_options = []
    for category in category_list:
        category_options.append(category.categories_name)

    return JsonResponse(category_options, safe=False)

@login_required(login_url="/users/loginpage/")
def keyword_category_update(request):
    user = request.user
    if request.method =='PUT':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        new_value = data.get('new_value')
        keyword_id = data.get('keyword_id')
        category_update = categorization.objects.get(id=keyword_id)
        new_category_id = categories_table.objects.get(user_id=user,categories_name=new_value)
        category_update.category_id = new_category_id
        category_update.save()
                
        return JsonResponse({'status': 'updated', 'new_value': new_value})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def refresh_categorization(request):
    user = request.user
    trans_list = trans.objects.filter(user_id=user)
    if request.method == 'PUT':
        print('refreshed')
        for transaction in trans_list:
            description = transaction.description
            try:
                category_name = categorization.objects.get(user_id=user,keyword__contains=description)
                category = category_name.category_id
                transaction.category_id = category
                transaction.save()
            except Exception:
                pass
        return JsonResponse({'status': 'updated'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@login_required(login_url="/users/loginpage/")
def file_mapping(request):
    if request.method == 'POST':
        print("HERE")
        data = json.loads(request.body)
        Date_column_name = data.get('Date_column_name')
        Description_column_name = data.get('Description_column_name')
        Amount_column_name = data.get('Amount_column_name')
        account_name_mapping_id = data.get('account_name_mapping')
        # print(Date_column_name,Description_column_name,Amount_column_name,account_name_mapping_id)
        if not Date_column_name or not Description_column_name or not Amount_column_name or not account_name_mapping_id:
            return
        account = Accounts.objects.get(id=account_name_mapping_id)
        if not FileMapping.objects.filter(account_id=account).exists():
            FileMapping.objects.create(account_id=account,Date_header_name=Date_column_name,
                                        Amount_header_name=Amount_column_name,
                                        Description_header_name=Description_column_name)
            
        return JsonResponse({'status': 'added'})
    return JsonResponse({'error': 'Invalid method'}, status=405)