from django.urls import path
from django.urls.conf import include, re_path
from django.conf import settings  
from django.conf.urls.static import static  
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
path("", views.index, name="index"),
path("home/", views.home, name="home"),
path("forecasting/", views.forecasting_view, name="forecasting"),
path("membershipapplication/", views.membershipapplication_view, name="membershipapplication"),
path("cancelmembershipapplication/", views.cancelapplication_view, name="cancelmembershipapplication"),
path("threedaysremaining/", views.threedaysremaining_view, name="threedaysremaining"),
path("renewactivemembership/", views.renewactivemembership_view, name="renewactivemembership"),
path("renewexpiredmembership/", views.renewexpiredmembership_view, name="renewexpiredmembership"),
path("activemembership/", views.activemembership_view, name="activemembership"),
path("expiredmembership/", views.expiredmembership_view, name="expiredmembership"),
path("success/", views.success_view, name="success"),
path("allsendemail/", views.all_send_email, name="allsendemail"),
path("cancelmonthly/<int:id>", views.cancel_monthly, name="cancelmonthly"),
path("cancelannual/<int:id>", views.cancel_annual, name="cancelannual"),
path("cancelcustom/<int:id>", views.cancel_custom, name="cancelcustom"),
path("monthlydelete/<int:id>", views.monthly_delete, name="monthlydelete"),
path("annualdelete/<int:id>", views.annual_delete, name="annualdelete"),
path("customdelete/<int:id>", views.custom_delete, name="customdelete"),
path("monthlyaccept/<int:id>", views.monthly_accept, name="monthlyaccept"),
path("annualaccept/<int:id>", views.annual_accept, name="annualaccept"),
path("customaccept/<int:id>", views.custom_accept, name="customaccept"),
path("cancelmonthlyview/<int:id>", views.cancelmonthly_view, name="cancelmonthlyview"),
path("cancelannualview/<int:id>", views.cancelannual_view, name="cancelannualview"),
path("cancelcustomview/<int:id>", views.cancelcustom_view, name="cancelcustomview"),
path("monthlysendemail/<int:id>", views.monthly_send_email, name="monthlysendemail"),
path("annualsendemail/<int:id>", views.annual_send_email, name="annualsendemail"),
path("customsendemail/<int:id>", views.custom_send_email, name="customsendemail"),
path("rmonthlymembership/<int:id>", views.renew_monthly, name="rmonthlymembership"),
path("rmonthlyaccept/<int:id>", views.renewmonthly_accept, name="rmonthlyaccept"),
path("rmonthlydelete/<int:id>", views.renewmonthly_delete, name="rmonthlydelete"),
path("rmonthlyview/<int:id>", views.renewmonthly_view, name="rmonthlyview"),
path("rmonthlyexpired/<int:id>", views.renew_monthlyexpired, name="rmonthlyexpired"),
path("rmonthlyexpiredaccept/<int:id>", views.renewmonthlyexpired_accept, name="rmonthlyexpiredaccept"),
path("rmonthlyexpireddelete/<int:id>", views.renewmonthlyexpired_delete, name="rmonthlyexpireddelete"),
path("rmonthlyexpiredview/<int:id>", views.renewmonthlyexpired_view, name="rmonthlyexpiredview"),
path("rannualmembership/<int:id>", views.renew_annual, name="rannualmembership"),
path("rannualaccept/<int:id>", views.renewannual_accept, name="rannualaccept"),
path("rannualdelete/<int:id>", views.renewannual_delete, name="rannualdelete"),
path("rannualview/<int:id>", views.renewannual_view, name="rannualview"),
path("rannualexpired/<int:id>", views.renew_annualexpired, name="rannualexpired"),
path("rannualexpiredaccept/<int:id>", views.renewannualexpired_accept, name="rannualexpiredaccept"),
path("rannualexpireddelete/<int:id>", views.renewannualexpired_delete, name="rannualexpireddelete"),
path("rannualexpiredview/<int:id>", views.renewannualexpired_view, name="rannualexpiredview"),
path("rcustommembership/<int:id>", views.renew_custom, name="rcustommembership"),
path("rcustomaccept/<int:id>", views.renewcustom_accept, name="rcustomaccept"),
path("rcustomdelete/<int:id>", views.renewcustom_delete, name="rcustomdelete"),
path("rcustomview/<int:id>", views.renewcustom_view, name="rcustomview"),
path("rcustomexpired/<int:id>", views.renew_customexpired, name="rcustomexpired"),
path("rcustomexpiredaccept/<int:id>", views.renewcustomexpired_accept, name="rcustomexpiredaccept"),
path("rcustomexpireddelete/<int:id>", views.renewcustomexpired_delete, name="rcustomexpireddelete"),
path("rcustomexpiredview/<int:id>", views.renewcustomexpired_view, name="rcustomexpiredview"),
path("monthlymembershippdf/", views.monthlymembership_pdf, name="monthlymembershippdf"),
path("annualmembershippdf/", views.annualmembership_pdf, name="annualmembershippdf"),
path("custommembershippdf/", views.custommembership_pdf, name="custommembershippdf"),
path("adminpage/", views.admin_view, name="adminpage"),
path("adminsearch/", views.admin_search, name="adminsearch"),
path("usersedit/<int:id>", views.users_edit, name="usersedit"),
path("usersdelete/<int:id>", views.users_delete, name="usersdelete"),
path("monthlymembershipview/<int:id>", views.monthlymembership_view, name="monthlymembershipview"),
path("annualmembershipview/<int:id>", views.annualmembership_view, name="annualmembershipview"),
path("custommembershipview/<int:id>", views.custommembership_view, name="custommembershipview"),
path("monthlymembershipaccept/<int:id>", views.monthlymembership_accept, name="monthlymembershipaccept"),
path("annualmembershipaccept/<int:id>", views.annualmembership_accept, name="annualmembershipaccept"),
path("custommembershipaccept/<int:id>", views.custommembership_accept, name="custommembershipaccept"),
path("monthlymembershipdelete/<int:id>", views.monthlymembership_delete, name="monthlymembershipdelete"),
path("annualmembershipdelete/<int:id>", views.annualmembership_delete, name="annualmembershipdelete"),
path("custommembershipdelete/<int:id>", views.custommembership_delete, name="custommembershipdelete"),
path("membership/", views.membership_view, name="membership"),
path("membershipsearch/", views.membership_search, name="membershipsearch"),
path("monthlyform/", views.monthly_form, name="monthlyform"),
path("annualform/", views.annual_form, name="annualform"),
path("customform/", views.custom_form, name="customform"),
path("signup/", views.signup_view, name="signup"),
path("signin/", views.signin_view, name="signin"),
path("signout/", views.signout_view, name="signout"),

# MEAL
path("mealplanform/", views.mealplan_form, name="mealplanform"),
path('generate_pdf', views.generate_pdf, name='generate_pdf'),
# path("mealplan/", views.mealplan_view, name="mealplan"),

# PASSWORD RESET URL
path("reset_password/", 
     auth_views.PasswordResetView.as_view(template_name="membership/password_reset.html"), 
     name="reset_password"),
path("reset_password_sent/",
     auth_views.PasswordResetDoneView.as_view(template_name="membership/password_reset_sent.html"),
     name="password_reset_done"),
path("reset/<uidb64>/<token>",
     auth_views.PasswordResetConfirmView.as_view(template_name="membership/password_reset_form.html"),
     name="password_reset_confirm"),
path("reset_password_complete/",
     auth_views.PasswordResetCompleteView.as_view(template_name="membership/password_reset_done.html"),
     name="password_reset_complete"),

]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  