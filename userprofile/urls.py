from django.urls import path
from . import views


urlpatterns = [

    path('',views.profile_view, name="profile_view"),
    path('user_update/',views.user_update, name="user_update"),

]