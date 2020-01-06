from django.shortcuts import render, redirect
from django.contrib import messages
from frontend.models import LoanDetail,Customer,LoanApplication
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from . models import LoanMaster, EMI, Payments
from django.http import JsonResponse
from django.db.models import Max
import math
# Create your views here.

def error(request):
    return render(request, 'frontend/404.html')

def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        password = request.POST['password']

        user = auth.authenticate(username=uname, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')    

    else:        
        return render(request, 'frontend/login.html')

def register(request):
    if request.method == 'POST':
        flname = request.POST['fname'].split()
        fn = flname[0]
        if len(flname) > 1:
            ln = flname[1]
        else:
            ln = ''    
        uname = request.POST['uname']
        email = request.POST['email']
        pwd = request.POST['password']
        
        if User.objects.filter(username=uname).exists():
            messages.info(request, "Username Exists")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"Email Exists")
            return redirect('register')
        else:
            user = User.objects.create_user(first_name=fn,last_name=ln, email=email, username=uname, password=pwd)            
            user.save()
            return redirect('login')

    else:        
        return render(request, 'frontend/register.html')    

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/user/login')
def dashboard(request):
    return render(request, 'dashboard/index.html')

@login_required(login_url='login')
def loan_form(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'frontend/404.html')
    else:
        if request.method == 'POST':
            id = request.POST['id']
            name = request.POST['name']
            age = request.POST['age']
            email = request.POST['email']
            phone = request.POST['phone']
            type_of_loan = request.POST['type_of_loan']
            loan_amt = request.POST['loan_amt']
            income = request.POST['income']
            address = request.POST['address']

            la = LoanApplication.objects.create(loan_amount=loan_amt, cust_name=name, income=income, age=age, address=address, phone=phone, email=email, loan_type_id=type_of_loan, user_id=id, status='pending')
            la.save()
            messages.success(request, "Application Submitted Successfully!")
            return redirect('loan_form')
        
        else:    
            type_loan = LoanDetail.objects.all()
            return render(request, 'dashboard/loan_form.html',{'type_loan':type_loan})
        

@login_required(login_url='login')
def loan_applications(request,view):
    if request.user.is_superuser or request.user.is_staff:
        if view == 'pending':
            apps = LoanApplication.objects.filter(status='pending')
        elif view == 'all':
            apps = LoanApplication.objects.all()
        else:
            apps = LoanApplication.objects.get(app_id=view)
            return render(request,'dashboard/loan_app_actions.html',{'view':view, 'app':apps})    

        return render(request,'dashboard/loan_applications.html',{'applications':apps, 'view':view.upper()})
    else:
        if request.user.is_superuser and request.user.is_staff:
            return render(request, 'frontend/404.html')
        else:
            apps = LoanApplication.objects.filter(user_id=request.user)
            return render(request,'dashboard/loan_applications.html',{'apps':apps})


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        if request.user.is_superuser or request.user.is_staff:
            flname = request.POST['name'].split()
            fn = flname[0]
            if len(flname) > 1:
                ln = flname[1]
            else:
                ln = '' 

            user = User.objects.get(id=request.user.id)
            user.first_name = fn
            user.last_name = ln
            user.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('profile')
        else:
            pan_no = request.POST['pan_no']
            phone = request.POST['phone']
            address = request.POST['address']

            customer, created = Customer.objects.update_or_create(
                user_id=request.user.id,
                defaults={"phone": phone, "pan_no": pan_no, "address": address}
            )
            messages.success(request, "Profile Updated Successfully")
            return redirect('profile')
        
    else:    
        user = User.objects.get(id=request.user.id)
        try:
            customer = Customer.objects.get(user_id=request.user)
        except:
            customer = None            

        return render(request, 'dashboard/profile.html', {"profile":customer, "admin": user})

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        password = request.POST['new_pwd']

        user = User.objects.get(id=request.user.id)
        user.set_password(password)
        user.save()
        messages.success(request, "Password Changed Successfully! Login with new password..")
        return redirect('login')
    else:
        return render(request, 'dashboard/profile.html')

@login_required(login_url='login')        
def admin_approve_loan(request, app_id):
    if request.method == 'POST':
        if request.POST['submit'] == 'approve':
            name = request.POST['name']
            phone = request.POST['phone']
            loan_type = request.POST['type_of_loan']
            emi_tenure = float(request.POST['emi_tenure']) / 12
            loan_amt = round(float(request.POST['loan_amt']),2)
            address = request.POST['address']
            rateobj = LoanDetail.objects.get(id=loan_type)
            rate = rateobj.rate
            app_id = request.POST['app_id']
            user_id = request.POST['user_id']

            mloan, created = LoanMaster.objects.update_or_create(
                app_id = app_id,
                defaults={"loan_tenure":emi_tenure*12, "loan_amount":loan_amt, "interest_rate": rate, "phone": phone, "address":address, "app_id":app_id, "loan_type_id":loan_type, "cust_name":name, "user_id":user_id}
            )
            p = float(loan_amt)
            r = rate / (12 * 100)
            t = emi_tenure * 12
            power = pow(1 + r, t)
            emi = round((p * r * power ) / (power - 1),2)
            interest_amount = round(emi * (emi_tenure * 12),2)

            emiobj = EMI.objects.update_or_create(
                loan_id = mloan.loan_id,
                defaults={"total_amount":loan_amt, "interest_amount":interest_amount,"emi_amount":emi}
            )

            status_app = LoanApplication.objects.filter(app_id=app_id).update(status='approved')

            messages.success(request, "Application Updated Successfully")
            return redirect('admin_loan_details', view='all')
        else:
            submit = request.POST['submit']
            app_id = request.POST['app_id']
            if submit == 'cancel':
                status_app = LoanApplication.objects.filter(app_id=app_id).update(status='cancelled')
                messages.info(request, "Application Cancelled!")
                return redirect('admin_loan_applications', view=app_id)
            else:
                delobj = LoanMaster.objects.filter(app_id=app_id).delete()
                messages.info(request, "One Record Deleted!")
                return redirect('admin_loan_details', view='all')
    else:
        return redirect('error')

@login_required(login_url='login')        
def loan_detail(request, view):
    if request.user.is_superuser or request.user.is_staff:
        if view == 'my':
            mloan = LoanMaster.objects.filter(user_id=request.user)
        elif view == 'all':
            mloan = LoanMaster.objects.all()
        else:
            mloan = LoanMaster.objects.get(loan_id=view)
            emi = EMI.objects.get(loan_id=view)
            return render(request,'dashboard/loan_detail_actions.html',{'mloan':mloan, 'emi':emi})

        return render(request,'dashboard/loan_detail.html',{'mloan':mloan})      
    else:
        mloan = LoanMaster.objects.filter(user_id=request.user)
        return render(request,'dashboard/loan_detail.html',{'mloan':mloan})

@login_required(login_url='login')
def user_account(request,view):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            if request.POST['submit'] == 'create':
                is_staff = request.POST.get('is_staff', '') == 'on'
                is_superuser = request.POST.get('is_superuser','') == 'on'
                fname = request.POST['fname']
                lname = request.POST['lname']
                uname = request.POST['uname']
                email = request.POST['email']
                pwd = request.POST['pwd']
                if User.objects.filter(username=uname).exists():
                    messages.info(request, 'Username Exists!!')
                    return redirect('user_account', view='add')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Exists!!')
                    return redirect('user_account', view='add')
                else:
                    user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email, password=pwd, is_staff=is_staff, is_superuser=is_superuser)    
                    user.save()
                    return redirect('user_account', view='all')

            elif request.POST['submit'] == 'update':
                is_staff = request.POST.get('is_staff','') == 'on'
                is_superuser = request.POST.get('is_superuser','') == 'on'
                fname = request.POST['fname']
                lname = request.POST['lname']
                uname = request.POST['uname']
                email = request.POST['email']

                user = User.objects.get(id=view)    
                user.first_name = fname
                user.last_name = lname
                user.uname = uname
                user.email = email
                user.is_staff = is_staff
                user.is_superuser = is_superuser
                user.save()
                messages.success(request, 'Updated Successfully..')
                return redirect('user_account', view=view)
        else:
            if view == 'all':
                if request.user.is_superuser:
                    users = User.objects.all()
                else:
                    users = User.objects.filter(is_superuser=False, is_staff=False) 

            elif view == 'add':
                users = None

            else:
                users = User.objects.get(id=view)
                
            return render(request, 'dashboard/admin_acc.html', {'view':view.capitalize(),'users':users})
    else:
        return redirect('error')
@login_required(login_url='login')
def make_payment(request):
    if request.method == "POST":
        loan_id = request.POST['loan_id']
        cust_id = request.POST['cust_id']
        emi_amount = request.POST['emi_amount']
        no_of_payment = request.POST['no_of_payment']
        if no_of_payment == 'done':
            messages.info(request, 'All EMIs have been paid.')
            return redirect('make_payment')
        else:    
            payobj = Payments.objects.create(no_of_payments= no_of_payment, emi_amount= emi_amount, cust_id=cust_id, loan_id=loan_id)
            messages.success(request, "Payment Successful")
            return redirect('make_payment')
    else:
        userLoan = LoanMaster.objects.filter(user_id=request.user)
        return render(request, 'dashboard/make_pay.html',{'loans':userLoan})

def showPayAmt(request):
    loan_id = request.GET.get('loan_id','')
    emiobj = EMI.objects.get(loan_id=loan_id)
    payobj = Payments.objects.filter(loan_id=loan_id).aggregate(Max('no_of_payments'))
    loanobj = LoanMaster.objects.get(loan_id=loan_id)
    if payobj['no_of_payments__max'] == None:
        no_payment = 1
    else:
        if payobj['no_of_payments__max'] >= loanobj.loan_tenure:
            no_payment = 'done'            
        else:
            no_payment = payobj['no_of_payments__max'] + 1 
    data = {
        "emi": emiobj.emi_amount,
        "no_pay": no_payment,
        "cust_id": loanobj.user_id
    }
    return JsonResponse(data)

def payment_history(request):
    if request.method == "POST":
            loan_id = request.POST['loan_id']
            if request.user.is_superuser or request.user.is_staff:
                payobj = Payments.objects.filter(loan_id=loan_id).order_by('no_of_payments')
                myloans=None
            else:
                myloans = LoanMaster.objects.filter(user_id=request.user)
                payobj = Payments.objects.filter(cust_id=request.user).filter(loan_id=loan_id).order_by('no_of_payments')
        
            if payobj:
                messages.success(request, 'Payments found!!')
            else:
                messages.info(request, 'Payments Not found!!')
    else:
        payobj=None
        myloans = LoanMaster.objects.filter(user_id=request.user)
    return render(request, 'dashboard/pay_history.html', {'payments':payobj, 'myloans':myloans})