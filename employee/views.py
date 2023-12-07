from django.shortcuts import get_object_or_404, redirect, render
from manager.models import *
from django.contrib.auth import authenticate, login, logout,password_validation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def login_with_otp_employee(request):
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
            return redirect('index')
        return render(request, 'employee/otp_verification.html')

    return render(request, 'employee/login_with_otp.html')

# views.py
def verify_otp_employee(request):
    if request.method == 'POST':
        user_id = request.session.get('otp_user_id')
        user = User.objects.get(id=user_id)
        entered_otp = request.POST.get('otp')

        if str(request.session.get('otp')) == entered_otp:
            # OTP is valid, log in the user
            login(request, user)
            if hasattr(user, 'employee') and user.employee:
                messages.success(request, f'Welcome {user.employee.name}!')
            else:
                messages.error(request, f'sorry {user}!! You are not a registered employee')
                logout(request)
            return redirect('index')  # Replace 'success_page' with your actual success page
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('index')  # Replace 'success_page' with your actual success page


    return redirect('login_with_otp_employee')  # Redirect to the OTP entry page



# Create your views here.
@login_required(login_url='loginpage')
def index(request):

    myconstants =Myconstants.objects.get(id=1)
    employee = Employee.objects.filter(in_service=True).order_by('-points')
    allnotification = Notifications.objects.all().order_by('-date')

    context = {
        'employees':employee,
        'myconstants':myconstants,
        'notifications':allnotification

    }
    user = request.user
    if user.employee.in_service == False:
        logout(request)
        messages.error(request, f'sorry {user}!! You are out of service')
        return redirect('index')
    return render(request, 'employee/index.html',context)


def logout_view(request):
    logout(request)
    return redirect('index')  

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'employee') and user.employee:
                messages.success(request, f'Welcome {user.employee.name}!')
            else:
                messages.error(request, f'sorry {user}!! You are not a registered employee')
                logout(request)
            return redirect('index')  # Redirect to the home page after successful login

        else:
            messages.error(request, "Wrong password or username.")
            return redirect('loginpage')  # Redirect to the login page with an error message
    else:
        messages.error(request, "Wrong password or username.")
        return redirect('loginpage') 
        
def loginpage(request):
    return render(request,'employee/login.html')     

@login_required(login_url='loginpage')
def addcart(request,client_id):
    addnumber = get_object_or_404(Clientnumber, id=client_id)
    user = request.user

    if not user.is_authenticated:
        return redirect('index')
    employee = user.employee
    addnumber.taken_by = employee
    addnumber.status='hold'
    addnumber.save()
    messages.success(request, f'{addnumber.number} is added to your cart!')

    return redirect('cart')

@login_required(login_url='loginpage')
def cart(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('index')
    
    mycart = Clientnumber.objects.filter(taken_by=user.employee,remove=False,interested=False)
    numbers = Clientnumber.objects.filter(taken_by=None,remove=False,interested=False)
    context = {
        'numbers': numbers,
        'mycart': mycart
    }
    return render(request, 'employee/cart.html', context)


monthlyLimit= Myconstants.objects.get(id=1).monthlyLimit
weeklyLimit= Myconstants.objects.get(id=1).weeklyLimit

def update_status(request):
    employee = request.user.employee
    
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        status = request.POST.get('status')
        client = Clientnumber.objects.get(id=client_id)
        client.status = status
        client.save()

        if client.status == 'no_response':
            client.taken_by = None
            client.save()
        elif client.status == 'not_interested':
            client.remove = True
            client.save()
        elif client.status == 'interested':
            client.interested = True
            workreport = Workreport.objects.create(
                clientnumber = client,
                date = timezone.now()
            )

            if employee.monthlyDone < monthlyLimit:
                employee.monthlyDone += 1
                employee.monthlyPending -= 1
                messages.success(request, f'Congratulation {employee.name},10 points rewarded.')
            else:
                employee.extraWork =+ 1
                employee.addpoints(5)
                messages.success(request, f'Congratulation {employee.name},15 points rewarded for your special work.')

            employee.weeklyPending -= 1
            employee.weeklyDone += 1
            employee.totalWork += 1
            employee.addpoints(10)
            employee.save()


            client.save()        

        return redirect('cart')
    

@login_required(login_url='loginpage')
def profile(request):
    user = request.user
    employee = user.employee
    achievements = Workreport.objects.filter(clientnumber__taken_by=employee,clientnumber__remove=False,clientnumber__interested=True)

    context = {
        'employee':employee,
        'achievements':achievements
    }
    return render(request, 'employee/profile.html',context)    



def sendmessage(request):
    user = request.user
    
    if request.method == 'POST':
        sender_message= request.POST.get('message')
        employeemessage = Employeemessage.objects.create(
            employeemessage = sender_message,
            sender=user.employee
        )
        employeemessage.save()
        messages.success(request, 'Message sended.')
    else:
        messages.error(request, 'Message failed.')
    return redirect('profile')


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

        return render(request, 'employee/dailyreport.html', context)
    


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

        return render(request, 'employee/weeklyreport.html', context)


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

        return render(request, 'employee/monthlyreport.html', context)
