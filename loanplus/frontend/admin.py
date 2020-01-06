from django.contrib import admin
from .models import LoanDetail, Customer

# Register your models here.

admin.site.register([LoanDetail, Customer])