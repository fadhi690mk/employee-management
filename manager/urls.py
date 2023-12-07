# urls.py

from django.urls import path
from .views import *
urlpatterns = [
    path('', manager_view, name='manager'),
    path('workflow', workflow, name='workflow'),
    path('registration', registration, name='registration'),
    path('register', register, name='register'),
    path('notifications', notifications, name='notifications'),
    path('limits', limits, name='limits'),
    path('quotes', quotes, name='quotes'),
    path('uploadnumber', uploadnumber, name='uploadnumber'),
    path('outdated_notification/<int:notification_id>', outdated_notification, name='outdated_notification'),
    path('addpoints/<int:employee_id>', addpoints, name='addpoints'),
    path('employeeprofile/<int:employee_id>', employeeprofile, name='employeeprofile'),
    path('employee_update/<int:employee_id>', employee_update, name='employee_update'),
    path('outofservice/<int:employee_id>', outofservice, name='outofservice'),
    path('login_with_otp/', login_with_otp, name='login_with_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('logout/', logout_view, name='logout'),
    path('inbox_message/', inbox_message, name='inbox_message'),
    path('delete_inbox/<int:msg_id>', delete_inbox, name='delete_inbox'),
    path('reportpage/<int:employee_id>/<str:reporttype>', reportpage, name='reportpage'),
]
