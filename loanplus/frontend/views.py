from django.shortcuts import render,redirect
from django.contrib import messages
from .models import LoanDetail,Customer,LoanApplication
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'frontend/index.html')

def about(request):
    return render(request, 'frontend/about.html',{"page":"About"})

def services(request):
    loans = LoanDetail.objects.all()
    return render(request, 'frontend/services.html',{"page":"Services","loans":loans})

def emi_calculator(request):
    loans = LoanDetail.objects.all()
    return render(request, 'frontend/calculator.html', {"page":"EMI Calculator","loans":loans})

