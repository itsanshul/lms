from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pan_no = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
  

class LoanDetail(models.Model):
    id = models.AutoField(primary_key=True)
    type_of_loan = models.CharField(max_length=50)
    duration = models.CharField(max_length=10)
    rate = models.FloatField()

class LoanApplication(models.Model):
    app_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.ForeignKey(LoanDetail, on_delete=models.CASCADE)
    loan_amount = models.FloatField()
    cust_name = models.CharField(max_length=50)
    income = models.FloatField()
    age = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)