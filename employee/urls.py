# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_view, name='login'),
    path('logoutemployee', logout_view, name='logoutemployee'),
    path('login_with_otp_employee/', login_with_otp_employee, name='login_with_otp_employee'),
    path('verify_otp_employee/', verify_otp_employee, name='verify_otp_employee'),
    path('loginpage/', loginpage, name='loginpage'),
    path('addcart/<int:client_id>', addcart, name='addcart'),
    path('cart/', cart, name='cart'),
    path('update_status/', update_status, name='update_status'),
    path('profile/', profile, name='profile'),
    path('reportpageemployee/<int:employee_id>/<str:reporttype>', reportpage, name='reportpageemployee'),
    path('sendmessage/', sendmessage, name='sendmessage'),
    path('', index, name='index'),
]
