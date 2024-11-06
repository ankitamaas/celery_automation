# yourapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('index', index, name='index'),
    path('results/', results, name='results'),
    path('download_csv/', download_csv, name='download_csv'),
     path('signup/', signup, name='signup'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('delete_all/', delete_all, name='delete_all'),  # Add this line
    path('check_and_send_true', check_and_send_true, name="check_and_send_true")
]
