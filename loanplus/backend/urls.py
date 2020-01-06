from django.urls import path, re_path
from . import views

urlpatterns = [
    path("error-page", views.error, name="error"),
    path("user/login", views.login, name="login"),
    path("user/register", views.register, name="register"),
    path("user/logout", views.logout, name="logout"),
    path("user/dashboard",views.dashboard, name="dashboard"),
    path("user/dashboard/apply-now",views.loan_form, name="loan_form"),
    path("user/dashboard/view-loan-applications/<view>",views.loan_applications, name="loan_applications"),
    path('user/dashboard/loan-detail/<view>', views.loan_detail, name="loan_details"),
    path('user/dashboard/profile', views.profile, name='profile'),
    path('user/dashboard/change-password', views.change_password, name='change_password'),
    path('admin/dashboard/loan-application/<view>', views.loan_applications, name="admin_loan_applications"),
    path('admin/dashboard/approve-loan/<app_id>', views.admin_approve_loan, name="admin_approve_loan"),
    path('admin/dashboard/loan-details/<view>', views.loan_detail, name="admin_loan_details"),
    path('admin/dashboard/accounts/user/<view>', views.user_account, name="user_account"),
    path('user/dashoard/make-payment', views.make_payment, name="make_payment"),
    path('user/dashoard/payment-history', views.payment_history, name="payment_history"),
    path('showPayAmt', views.showPayAmt, name="showPayAmt"),
]
