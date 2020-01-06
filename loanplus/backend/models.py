from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class LoanMaster(models.Model):
    loan_id = models.AutoField(primary_key=True)
    app = models.ForeignKey("frontend.LoanApplication" ,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cust_name = models.CharField(max_length=50)
    loan_type = models.ForeignKey("frontend.LoanDetail", on_delete=models.CASCADE)
    loan_tenure = models.IntegerField()
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    issue_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=10)
    address = models.TextField()

class EMI(models.Model):
    c_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(LoanMaster,on_delete=models.CASCADE)
    total_amount = models.FloatField()
    interest_amount = models.FloatField()
    emi_amount = models.FloatField()

class Payments(models.Model):
    payment_no = models.AutoField(primary_key=True)
    cust = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(LoanMaster, on_delete=models.CASCADE)
    no_of_payments = models.IntegerField()
    pay_date = models.DateTimeField(auto_now_add=True)
    emi_amount = models.FloatField()