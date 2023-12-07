from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



from django.contrib.admin.views.decorators import staff_member_required


# views.py
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random

def generate_otp():
    return random.randint(100000, 999999)

def send_otp_email(user, otp):
    subject = 'Your OTP for Login'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

def login_with_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            
            # Generate OTP
            otp = generate_otp()

            # Store OTP in session or database (for validation)
            request.session['otp'] = otp
            request.session['otp_user_id'] = user.id

            # Send OTP to the user via email
            send_otp_email(user, otp)
        except:
            messages.error(request, "Invalid user.")
            return redirect('manager')
        return render(request, 'elements/otp_verification.html')

    return render(request, 'elements/login_with_otp.html')

# views.py
def verify_otp(request):
    if request.method == 'POST':
        user_id = request.session.get('otp_user_id')
        user = User.objects.get(id=user_id)
        entered_otp = request.POST.get('otp')

        if str(request.session.get('otp')) == entered_otp:
            # OTP is valid, log in the user
            login(request, user)
            messages.success(request, "Invalid OTP. Please try again.")

            return redirect('manager')  # Replace 'success_page' with your actual success page
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('manager')  # Replace 'success_page' with your actual success page


    return redirect('login_with_otp')  # Redirect to the OTP entry page



@staff_member_required(login_url='login_with_otp')
def manager_view(request):
    myconstants =Myconstants.objects.get(id=1)
    employee = Employee.objects.filter(in_service=True).order_by('points')
    context = {
        'employees':employee,
        'myconstants':myconstants
    }
    return render(request, 'manager/manager.html',context)

@staff_member_required(login_url='login_with_otp')
def workflow(request):
    employee = Employee.objects.filter(in_service=True)
    context = {
        'employees':employee
    }
    return render(request, 'manager/workflow.html',context)

@staff_member_required(login_url='login_with_otp')
def registration(request):
    return render(request, 'manager/registration.html')


@staff_member_required(login_url='login_with_otp')
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        if password == cpassword:
            try:
                user = User.objects.create_user(username=email, email=email, password=password)
                
                # Get additional employee data
                name = request.POST.get('name')
                cphone = request.POST.get('phone')
                work_mail = request.POST.get('workMail')
                cwork_phone = request.POST.get('workPhone')
                phone = cphone.strip().replace(" ", "")
                if not phone.startswith('+91'):    
                    phone = '+91' + phone
                work_phone = cwork_phone.strip().replace(" ", "")
                if not work_phone.startswith('+91'):    
                    work_phone = '+91' + work_phone    
                
                employee = Employee.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    work_mail=work_mail,
                    work_phone=work_phone
                )

                # Check if 'profilePhoto' exists in request.FILES
                if 'profilePhoto' in request.FILES:
                    profile_photo = request.FILES['profilePhoto']
                    employee.profile_photo = profile_photo
                    employee.save()

                messages.success(request, 'Employee registered successfully!')
            except IntegrityError:
                # Handle IntegrityError (UNIQUE constraint violation)
                messages.error(request, 'User mail already exists.')
            return redirect('registration')


        else:
            messages.error(request, 'Passwords do not match.')
    else:
        messages.error(request, 'Employee registration failed.')

    return redirect('registration')

@staff_member_required(login_url='login_with_otp')
def employee_update(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    if request.method == 'POST':
        # Update user email
        employee.user.email = request.POST.get('email')
        # Update other employee details
        employee.name = request.POST.get('name')
        employee.phone = request.POST.get('phone')
        employee.work_mail = request.POST.get('work_mail')
        employee.work_phone = request.POST.get('work_phone')

        # Check if 'profilePhoto' exists in request.FILES
        if 'profilePhoto' in request.FILES:
            profile_photo = request.FILES['profilePhoto']
            employee.profile_photo = profile_photo

        # Save the changes
        employee.user.save()
        employee.save()

        messages.success(request, 'Employee information updated successfully!')
        return redirect('workflow')  # Redirect to the employee list page

    context = {'employee': employee}
    return render(request, 'manager/employee_update.html', context)


@staff_member_required(login_url='login_with_otp')
def addpoints(request,employee_id):
    if request.method == 'POST':
        addnewpoints = int(request.POST.get('addpoints'))
        employee = Employee.objects.get(id=employee_id)
        employee.addpoints(addnewpoints)
        employee.save()
        messages.success(request, f'{addnewpoints} points add to {employee.name}')
    else:
        messages.error(request, 'Points not added.')
    return redirect('workflow')

def logout_view(request):
    logout(request)
    return redirect('manager')  

@staff_member_required(login_url='login_with_otp')
def outofservice(request,employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.in_service = False
    employee.save()
    messages.success(request, f'{employee.name} is now out of service')
    return redirect('workflow')
    
@staff_member_required(login_url='login_with_otp')
def notifications(request):
    if request.method == 'POST':
        notifications_text = request.POST.get('notifications')
        auto_delete_option = request.POST.get('auto_delete')

        # Create a new notification instance
        new_notification = Notifications(
            notifications=notifications_text,
            auto_delete=auto_delete_option
        )
        new_notification.save()

        messages.success(request, 'Notification created successfully!')
        return redirect('notifications')  # Replace 'notification_list' with your actual URL for listing notifications
    allnotification = Notifications.objects.all().order_by('-date')
    context={
        'notifications':allnotification
    }
    return render(request, 'manager/notifications.html',context)   

@staff_member_required(login_url='login_with_otp')
def inbox_message(request):
    inboxes = Employeemessage.objects.filter(deleted=False).order_by('-date')
    context={
        'inboxes':inboxes
    }
    return render(request, 'manager/messages.html',context)    

@staff_member_required(login_url='login_with_otp')
def outdated_notification(request,notification_id):
    notifications = Notifications.objects.get(id=notification_id)
    notifications.auto_delete = 'out_dated'
    notifications.save()
    return redirect('notifications')

@staff_member_required(login_url='login_with_otp')
def delete_inbox(request,msg_id):
    inbox = Employeemessage.objects.get(id=msg_id)
    inbox.deleted = True
    inbox.save()
    return redirect('inbox_message')

@staff_member_required(login_url='login_with_otp')
def limits(request):
    myconstants, created = Myconstants.objects.get_or_create(id=1)
    if request.method == 'POST':
        weeklyLimit = request.POST.get('weeklyLimit')
        MonthlyLimit = request.POST.get('MonthlyLimit')

        myconstants.weeklyLimit = weeklyLimit
        myconstants.monthlyLimit = MonthlyLimit
        myconstants.save()
    context={
        'myconstants':myconstants
    }
    return render(request, 'manager/limits.html',context) 

@staff_member_required(login_url='login_with_otp')
def quotes(request):
    myconstants, created = Myconstants.objects.get_or_create(id=1)
    if request.method == 'POST':
        quotes = request.POST.get('quotes')

        myconstants.quotes=quotes
        myconstants.save()

    return redirect('manager')  


@staff_member_required(login_url='login_with_otp')
def uploadnumber(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        raw_number = request.POST.get('number')
        place = request.POST.get('place')

        # Clean up the number: add +91 if not present and remove spaces
        cleaned_number = raw_number.strip().replace(" ", "")
        if not cleaned_number.startswith('+91'):
            cleaned_number = '+91' + cleaned_number

        try:
            # Attempt to create a new client number instance
            client_number = Clientnumber(
                name=name,
                place=place,
                number=cleaned_number,
            )
            client_number.save()
        except IntegrityError:
            # Handle IntegrityError (UNIQUE constraint violation)
            client = Clientnumber.objects.get(number=cleaned_number)
            if not client.taken_by == None:
                messages.error(request, f'{client.number} of {client.name} is previously taken by {client.taken_by} & status is {client.status}')
            else:
                messages.error(request, f'{client.number} of {client.name} is already exist')

        return redirect('uploadnumber')

    numbers = Clientnumber.objects.filter(remove=False,interested=False)
    context = {
        'numbers': numbers
    }
    return render(request, 'manager/numbers.html', context)



def employeeprofile(request,employee_id):
    employee = Employee.objects.get(id=employee_id)
    achievements = Workreport.objects.filter(clientnumber__taken_by=employee,clientnumber__remove=False,clientnumber__interested=True)

    context = {
        'employee':employee,
        'achievements':achievements
    }
    return render(request, 'manager/profile.html',context)    

def reportpage(request,employee_id, reporttype):
    employees = Employee.objects.filter(in_service=True).order_by('name')
    reports=None
    title='General'
    if employee_id==0:
        reports = Workreport.objects.all()
    else:
        employee = Employee.objects.get(id=employee_id)
        reports = Workreport.objects.filter(clientnumber__taken_by=employee)
        title=employee.user.username

    if reporttype == 'daily':

        # Group reports by day
        grouped_reports = {}
        for report in reports:
            date_key = report.date.date()  # Extract the date without time
            if date_key not in grouped_reports:
                grouped_reports[date_key] = []
            grouped_reports[date_key].append(report)

        # Create a list of reports grouped by date
        reports_by_date = list(grouped_reports.items())
        reports_by_date.reverse()
        # Paginate by date
        paginator = Paginator(reports_by_date, 1)  # 1 date per page
        page = request.GET.get('page')

        try:
            reports_page = paginator.page(page)
        except PageNotAnInteger:
            reports_page = paginator.page(1)
        except EmptyPage:
            reports_page = paginator.page(paginator.num_pages)

        context = {
            'reports_page': reports_page,
            'employees':employees,
            'title':title,
            'employee_id':employee_id
        }

        return render(request, 'manager/dailyreport.html', context)
    


    if reporttype == 'weekly':
        # Group reports by year and week
        grouped_reports = {}
        for report in reports:
            year_week = (report.date.year, report.date.isocalendar()[1])  # (year, ISO week number)
            if year_week not in grouped_reports:
                grouped_reports[year_week] = []
            grouped_reports[year_week].append(report)

        # Convert the dictionary to a list of dictionaries
        reports_by_week = [{'year': year, 'week_number': week_number, 'reports': reports}
                        for (year, week_number), reports in grouped_reports.items()]

        # Paginate the grouped reports
        paginator = Paginator(reports_by_week, 1)  # 1 week per page
        page = request.GET.get('page')

        try:
            reports_page = paginator.page(page)
        except PageNotAnInteger:
            reports_page = paginator.page(1)
        except EmptyPage:
            reports_page = paginator.page(paginator.num_pages)

        context = {
            'reports_page': reports_page,
            'employees':employees,
            'title':title,
            'employee_id':employee_id
        }

        return render(request, 'manager/weeklyreport.html', context)


    if reporttype == 'monthly':
        # Group reports by year and month
        grouped_reports = {}
        for report in reports:
            year_month = report.date.strftime('%Y-%m')
            if year_month not in grouped_reports:
                grouped_reports[year_month] = []
            grouped_reports[year_month].append(report)

        # Convert the dictionary to a list of dictionaries
        reports_by_month = [{'year_month': year_month, 'reports': reports}
                            for year_month, reports in grouped_reports.items()]

        # Paginate the grouped reports
        paginator = Paginator(reports_by_month, 1)  # 1 month per page
        page = request.GET.get('page')

        try:
            reports_page = paginator.page(page)
        except PageNotAnInteger:
            reports_page = paginator.page(1)
        except EmptyPage:
            reports_page = paginator.page(paginator.num_pages)

        context = {
            'reports_page': reports_page,
            'employees':employees,
            'title':title,
            'employee_id':employee_id
        }

        return render(request, 'manager/monthlyreport.html', context)
