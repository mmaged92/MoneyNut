from django.urls import path
from . import views


urlpatterns = [

    path('monthly_view',views.monthly_view, name="monthly_view"),
    path('monthly_view/category_get_view/',views.category_get_view, name="category_get_view"),
    path('monthly_view/monthly_get/',views.monthly_get, name="monthly_get"),
    path('monthly_view/category_spent/',views.category_spent, name="category_spent"),
    path('monthly_view/category_spent_amounts/',views.category_spent_amounts, name="category_spent_amounts"),
    path('monthly_view/category_spent_daily/',views.category_spent_daily, name="category_spent_daily"),
    path('monthly_view/spentvstarget/',views.spentvstarget, name="spentvstarget"),
    path('monthly_view/incomevsspent/',views.incomevsspent, name="incomevsspent"),
    path('monthly_view/savingvstarget/',views.savingvstarget, name="savingvstarget"),
    path('annual_view/annual_target_view',views.annual_target_view, name="annual_target_view"),
    path('annual_view/annual_get_target/',views.annual_get_target, name="annual_get_target"),
    path('annual_view/annual_Expected_income/',views.Expected_income_get, name="Expected_income_get"),
    path('annual_view/annual_Expected_Saving/',views.Expected_Saving_get, name="Expected_Saving_get"),
    path('annual_view/annual_actual_view',views.annual_actual_view, name="annual_actual_view"),
    path('annual_view/annual_get_actual/',views.annual_get_actual, name="annual_get_actual"),
    path('annual_view/annual_spent/',views.annual_spent, name="annual_spent"),
    path('annual_view/annual_target/',views.annual_target, name="annual_target"),
    path('annual_view/annual_income/',views.annual_income, name="annual_income"),
    path('annual_view/annual_saving/',views.annual_saving, name="annual_saving"),
    path('annual_view/annual_saving_target/',views.annual_saving_target, name="annual_saving_target"),
    path('annual_view/balance_track_annual/',views.balance_track_annual, name="balance_track_annual"),
    path('monthly_view/balance_track_monthly/',views.balance_track_monthly, name="balance_track_monthly"),
    path('dashboard/',views.dashboard_view, name="dashboard_view"),
    path('dashboard/total_spent/',views.total_spent, name="total_spent"),
    path('dashboard/current_balance/',views.current_balance, name="current_balance"),
    path('dashboard/fixed_fees_remaining/',views.fixed_fees_remaining, name="fixed_fees_remaining"),
    path('dashboard/this_month_status/',views.this_month_status, name="this_month_status"),
    path('dashboard/spent_trend/',views.this_month_spent_trend, name="this_month_spent_trend"),
    path('dashboard/this_month_spent_percentage/',views.this_month_spent_percentage, name="this_month_spent_percentage"),
    path('dashboard/this_month_trans/',views.this_month_trans, name="this_month_trans"),
    path('dashboard/this_month_spent_sub_categ_percentage_inverse/',views.this_month_spent_percentage_inverse, name="this_month_spent_percentage_inverse"),
    path('dashboard/this_month_spent_sub_categ_percentage/',views.this_month_spent_sub_categ_percentage, name="this_month_spent_sub_categ_percentage"),
    path('saving_goal/',views.Saving_goal, name="Saving_goal"),
    path('saving_goal_progress/',views.saving_goal_progress, name="saving_goal_progress"),
    
    
    
    
]
