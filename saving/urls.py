from django.urls import path
from . import views


urlpatterns = [
    path('',views.saving_monthly_target, name="saving_monthly_target"),
    path('saving_target_get',views.saving_target_get, name="saving_target_get"),
    path('freq_get',views.freq_get, name="freq_get"),
    path('saving_target_update',views.saving_target_update, name="saving_target_update"),
    path('date_update',views.date_update, name="date_update"),
    path('delete_saving',views.delete_saving, name="delete_saving"),
    path('freq_update',views.freq_update, name="freq_update"),
    
    path('income',views.income_view, name="income_view"),
    path('income/income_get',views.income_get, name="income_get"),
    path('income/income_freq_get',views.income_freq_get, name="income_freq_get"),
    path('income/delete_income',views.delete_income, name="delete_income"),
    path('income/income_update',views.income_update, name="income_update"),
    path('income/income_date_update',views.income_date_update, name="income_date_update"),
    path('income/income_freq_update',views.income_freq_update, name="income_freq_update"),
    
    path('goal',views.goal_view, name="goal_view"),
    path('goal/goal_get',views.goal_get, name="goal_get"),
    path('goal/delete_goal',views.goal_delete, name="goal_delete"),
    path('goal/goal_name_update',views.goal_name_update, name="goal_name_update"),
    path('goal/goal_target_update',views.goal_target_update, name="goal_target_update"),
    path('goal/goal_due_date_update',views.goal_due_date_update, name="goal_due_date_update"),
    path('goal/goal_account_update',views.goal_account_update, name="goal_account_update"),
    path('goal/get_accounts',views.get_accounts, name="get_accounts"),



]
