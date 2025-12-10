from django.urls import path
from . import views

urlpatterns = [
    path('',views.trans_add,name="trans_page"),
    path('view/',views.trans_view,name="trans_view"),
    path('all/',views.trans_all,name="trans_all"),
    path('account_get/',views.Account_get,name="trans_account"),
    path('io_get/',views.IO_get,name="trans_io"),
    path('refresh_categorization/',views.refresh_categorization,name="refresh_categorization"),
    path('file_mapping/',views.file_mapping,name="file_mapping"),

    path('descriptionupdate/',views.description_update,name="description_update"),
    path('date_update/',views.date_update,name="date_update"),
    path('amount_update/',views.amount_update,name="amount_update"),
    path('category_update/',views.category_update,name="category_update"),
    path('IO_update/',views.IO_update,name="IO_update"),
    path('account_update/',views.account_update,name="account_update"),
    path('delete/',views.transaction_delete,name="transaction_delete"),

    path('keyword/',views.keyword_insert,name="keyword"),
    path('keyword/all',views.keyword_all,name="keyword_all"),
    path('keyword/delete',views.keyword_delete,name="keyword_delete"),
    # path('keyword/add',views.keyword_add,name="keyword_add"),
    path('keyword/update',views.keyword_update,name="keyword_update"),
    path('keyword/category',views.keyword_category_get,name="keyword_category"),
    path('keyword/categoryupdate',views.keyword_category_update,name="keyword_category_update"),

]
