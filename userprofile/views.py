from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .models import UserProfile

material_status_list = ['Single', 'Married']
gender_list = ['Male', 'Female']

countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo (Congo-Brazzaville)",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czech Republic",
    "Democratic Republic of the Congo",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Korea",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Korea",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States of America",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe"
]




@login_required(login_url="/users/loginpage/")
def profile_view(request):
    user = request.user
    userprofile = UserProfile.objects.get(user_id = user)
    context ={
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "Job_title": userprofile.Job_Title,
        "material_status": userprofile.Marital_Status,
        "DateofBirth": userprofile.Birth_date,
        "Gender": userprofile.Gender,
        "Phone_number": userprofile.Phone_number,
        "Address": userprofile.Address,
        "Country": userprofile.Country,
        "Region": userprofile.Region,
        "ZIP_Code": userprofile.ZIP_Code,
        "material_status_list":material_status_list,
        "gender_list":gender_list
        
    }
    return render(request,'userprofile/profile.html',context)

@login_required(login_url="/users/loginpage/")
def user_update(request):
    
    if request.method =='PUT':
        user = request.user
        username = user.username
        data = json.loads(request.body)
        first_name_data = data.get('first_name_data')
        last_name_data = data.get('last_name_data')
        Birth_date = data.get('BD')
        Marital_Status = data.get('MS')
        gender = data.get('GENDER')
        job_title = data.get('JT')
        phone_number = data.get('PN')
        address = data.get('AD')
        country = data.get('country')
        Region = data.get('Region')
        email = data.get('email')
        zip_code = data.get('ZPC')
        change_password = data.get('change_password')
        confirm_change_password = data.get('confirm_change_password')
        
        
        if first_name_data:
            update_value = User.objects.get(username=username)
            update_value.first_name = first_name_data
            update_value.save()

        if last_name_data:
            update_value = User.objects.get(username=username)
            update_value.last_name = last_name_data
            update_value.save()
            print(last_name_data)

        if email:
            update_value = User.objects.get(username=username)
            update_value.email = email
            update_value.save()

        if change_password and confirm_change_password:
            if change_password == confirm_change_password:
                update_value = User.objects.get(username=username)
                update_value.set_password("change_password")
                update_value.save()

        if Birth_date:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.Birth_date = Birth_date
            update_value.save()

        if Marital_Status:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.Marital_Status = Marital_Status
            update_value.save()
        
        if gender:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.Gender = gender
            update_value.save()
        
        if job_title:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.Job_Title = job_title
            update_value.save()
             
        if phone_number:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.Phone_number = phone_number
            update_value.save()
        
        if address:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.Address = address
            update_value.save()
        
        if country:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.Country = country
            update_value.save()
        
        if Region:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.Region = Region
            update_value.save()
        
        if zip_code:
            update_value = UserProfile.objects.get(user_id=user)
            update_value.ZIP_Code = zip_code
            update_value.save()
        
        return JsonResponse({'status': 'updated'})
    return JsonResponse({'error': 'Invalid method'}, status=405)
    