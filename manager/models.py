from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    work_mail = models.EmailField(blank=True, null=True)
    work_phone = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    in_service = models.BooleanField(default=True)

    weeklyPending = models.IntegerField(default=0)
    weeklyDone = models.IntegerField(default=0)
    monthlyDone = models.IntegerField(default=0)
    monthlyPending = models.IntegerField(default=0)
    extraWork = models.IntegerField(default=0)
    totalWork = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    last_modified = models.DateTimeField(blank=True)

    def __str__(self):
        return f'{self.user.email}'

    @receiver(pre_save, sender='manager.Employee')
    def reset_monthly_counters(sender, instance, **kwargs):
        # Check if it's a new employee or an existing one
        limit = Myconstants.objects.get(id=1)
        if instance.pk is None:
            # New employee, set initial values
            instance.monthlyDone = 0
            instance.monthlyPending = limit.monthlyLimit
            instance.weeklyDone = 0

        else:
            # Existing employee, check if a new month has started
            current_month = timezone.now().month
            if instance.last_modified.month != current_month:
                instance.monthlyDone = 0
                instance.monthlyPending = limit.monthlyLimit
                instance.weeklyDone = 0
                instance.weeklyPending = 0

    @receiver(pre_save, sender='manager.Employee')
    def reset_weekly_counters(sender, instance, **kwargs):
        # Check if it's a new employee or an existing one
        limit = Myconstants.objects.get(id=1)
        if instance.pk is None:
            # New employee, set initial values
            instance.weeklyDone = 0
            instance.weeklyPending = limit.weeklyLimit  # Set to zero initially
        else:
            # Existing employee, check if a new week has started
            current_week = timezone.now().isocalendar()[1]  # ISO week number
            if instance.last_modified.isocalendar()[1] != current_week:
                instance.weeklyDone = 0
                instance.weeklyPending += limit.weeklyLimit           




    def addpoints(self,addpoints):
        self.points += addpoints
        self.save()

    @staticmethod
    def get_default_profile_image_path():
        return 'default/profile.png'
    
    def save(self, *args, **kwargs):
        if not self.profile_photo:
            self.profile_photo.name = self.get_default_profile_image_path()  
        super().save(*args, **kwargs)    

class Notifications(models.Model):
    NOTIFICATION_CHOICES = [
        ('one_day', 'One Day'),
        ('three_days', 'Three Days'),
        ('one_week', 'One Week'),
        ('one_month', 'One Month'),
        ('no_delete', "Don't Delete"),
        ('out_dated', "out_dated"),
    ]

    notifications = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    auto_delete = models.CharField(max_length=20, choices=NOTIFICATION_CHOICES, default='no_delete')

    @property
    def is_outdated(self):
        time_diff = timezone.now() - self.date
        if self.auto_delete == 'one_day' and time_diff.days >= 1:
            return True
        elif self.auto_delete == 'three_days' and time_diff.days >= 3:
            return True
        elif self.auto_delete == 'one_week' and time_diff.days >= 7:
            return True
        elif self.auto_delete == 'one_month' and time_diff.days >= 30:
            return True
        elif self.auto_delete == 'out_dated':
            return True
        else:
            return False
    
    
class Myconstants(models.Model):
    weeklyLimit = models.IntegerField(default=0)
    monthlyLimit = models.IntegerField(default=0)
    quotes = models.TextField(blank=True,null=True)

class Clientnumber(models.Model):
    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('no_response', 'No Response'),
        ('hold', 'Hold'),
        (None, 'Null'),  # For handling the null option
    ]

    name = models.CharField(max_length=150)
    place = models.CharField(max_length=150,blank=True)
    number = models.CharField(max_length=150,unique=True)
    taken_by = models.ForeignKey(Employee,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,blank=True, null=True)
    remove = models.BooleanField(default=False)
    interested = models.BooleanField(default=False)

class Employeemessage(models.Model):
    employeemessage = models.TextField()
    sender = models.ForeignKey(Employee,on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class Workreport(models.Model):
    clientnumber = models.ForeignKey(Clientnumber,on_delete=models.SET_NULL,blank=True,null=True)
    date = models.DateTimeField(blank=True)
