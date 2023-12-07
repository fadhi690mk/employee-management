from django.contrib import admin
from . models import *


class EmployeeAdmin(admin.ModelAdmin):
    list_display=['name','in_service']
    list_editable =['in_service']
admin.site.register(Employee,EmployeeAdmin)


class NotificationsAdmin(admin.ModelAdmin):
    list_display=['notifications','date','auto_delete']
    list_editable =['auto_delete']
admin.site.register(Notifications,NotificationsAdmin)

class MyconstantsAdmin(admin.ModelAdmin):
    list_display=['weeklyLimit','monthlyLimit']
admin.site.register(Myconstants,MyconstantsAdmin)

class ClientnumberAdmin(admin.ModelAdmin):
    list_display=['taken_by','number','name','status']
admin.site.register(Clientnumber,ClientnumberAdmin)

class EmployeemessageAdmin(admin.ModelAdmin):
    list_display=['employeemessage']
    
admin.site.register(Employeemessage,EmployeemessageAdmin)

class WorkreportAdmin(admin.ModelAdmin):
    list_display=['clientnumber','date']
    list_editable =['date']
    
admin.site.register(Workreport,WorkreportAdmin)
