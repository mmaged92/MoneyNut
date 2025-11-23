from django.urls import path
from . import views


urlpatterns = [
    path('',views.family_invite, name="family_invite"),
    path('add_family',views.add_family, name="add_family"),
    path('view_family_members/',views.view_family_members, name="view_family_members"),
    path('get_family_members/',views.get_family_members, name="get_family_members"),
    path('remove_family_member/',views.remove_family_member, name="remove_family_member"),
    
    path('dashboard_family/',views.family_dashboard_view, name="family_dashboard_view"),
    path('dashboard_family/total_spent_family/',views.family_total_spent, name="family_total_spent"),
    path('dashboard_family/current_balance_family/',views.family_current_balance, name="family_current_balance"),
    path('dashboard_family/fixed_fees_remaining_family/',views.family_fixed_fees_remaining, name="family_fixed_fees_remaining"),
    path('dashboard_family/this_month_status_family/',views.family_this_month_status, name="family_this_month_status"),
    path('dashboard_family/spent_trend_family/',views.family_this_month_spent_trend, name="family_this_month_spent_trend"),
    path('dashboard_family/this_month_spent_percentage_family/',views.family_this_month_spent_percentage, name="family_this_month_spent_percentage"),
    path('dashboard_family/this_month_trans_family/',views.family_this_month_trans, name="family_this_month_trans"),
    path('dashboard_family/this_month_spent_sub_categ_percentage_inverse_family/',views.family_this_month_spent_percentage_inverse, name="family_this_month_spent_percentage_inverse"),
    path('dashboard_family/this_month_spent_sub_categ_percentage_family/',views.family_this_month_spent_sub_categ_percentage, name="family_this_month_spent_sub_categ_percentage"),
    
    path('monthly_view/balance_track_monthly/',views.balance_track_monthly, name="balance_track_monthly_family"),
    path('monthly_view',views.monthly_view, name="monthly_view_family"),
    path('monthly_view/category_get_view/',views.category_get_view, name="category_get_view_family"),
    path('monthly_view/monthly_get/',views.monthly_get, name="monthly_get_family"),
    path('monthly_view/category_spent/',views.category_spent, name="category_spent_family"),
    path('monthly_view/category_spent_amounts/',views.category_spent_amounts, name="category_spent_amounts_family"),
    path('monthly_view/category_spent_daily/',views.category_spent_daily, name="category_spent_daily_family"),
    path('monthly_view/spentvstarget/',views.spentvstarget, name="spentvstarget_family"),
    path('monthly_view/incomevsspent/',views.incomevsspent, name="incomevsspent_family"),
    path('monthly_view/savingvstarget/',views.savingvstarget, name="savingvstarget_family"),
    
    path('annual_view/annual_target_view',views.annual_target_view, name="annual_target_view_family"),
    path('annual_view/annual_get_target/',views.annual_get_target, name="annual_get_target_family"),
    path('annual_view/annual_Expected_income/',views.Expected_income_get, name="Expected_income_get_family"),
    path('annual_view/annual_Expected_Saving/',views.Expected_Saving_get, name="Expected_Saving_get_family"),
    path('annual_view/annual_actual_view',views.annual_actual_view, name="annual_actual_view_family"),
    path('annual_view/annual_get_actual/',views.annual_get_actual, name="annual_get_actual_family"),
    path('annual_view/annual_spent/',views.annual_spent, name="annual_spent_family"),
    path('annual_view/annual_target/',views.annual_target, name="annual_target_family"),
    path('annual_view/annual_income/',views.annual_income, name="annual_income_family"),
    path('annual_view/annual_saving/',views.annual_saving, name="annual_saving_family"),
    path('annual_view/annual_saving_target/',views.annual_saving_target, name="annual_saving_target_family"),
    path('annual_view/balance_track_annual/',views.balance_track_annual, name="balance_track_annual_family"),
    path('saving_goal_family/',views.Saving_goal, name="Saving_goal_family"),
    path('saving_goal_progress_family/',views.saving_goal_progress, name="saving_goal_progress_family"),
    path('trans_view_family/',views.trans_view_family, name="trans_view_family"),
    path('trans_get_family/',views.trans_get_family, name="trans_get_family"),
    
    
]