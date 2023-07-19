import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .models import User, Monthly, Annual, Custom
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection
from django.http import JsonResponse

# ID Card Generator
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, '').replace("\\","/")

# ARIMA PREDICTION
import csv
import datetime
import pandas as pd
import numpy as np
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import matplotlib
matplotlib.use('agg')  # Set the backend to 'agg'
import matplotlib.pyplot as plt
import io
import base64

# MEAL PLANNER
import requests
import random
import math
from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.colors import blue

# from django.core.validators import RegexValidator
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from .models import User
# from .forms import UserForm
# from .functions import handle_uploaded_file

# Create your views here.

def index(request):
    return render(request, "membership/index.html", {})

@login_required(login_url='/signin/')
def home(request):
    User = get_user_model()
    users = User.objects.all()
    current_user = request.user

    # Not Verfied User
    nvuser_monthly = Monthly.objects.select_related().filter(
        is_verified=0,
        is_cancel=0,
        email__exact=current_user.email
    )
    nvuser_annual = Annual.objects.select_related().filter(
        is_verified=0,
        is_cancel=0,
        email__exact=current_user.email
    )
    nvuser_custom = Custom.objects.select_related().filter(
        is_verified=0,
        is_cancel=0,
        email__exact=current_user.email
    )

    # Verified User
    user_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    )
    user_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    )
    user_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    )

    # Verified User Length
    lenuser_monthly = len(Monthly.objects.select_related().filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    ))
    lenuser_annual = len(Annual.objects.select_related().filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    ))
    lenuser_custom = len(Custom.objects.select_related().filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    ))

    # Expired Membership
    expireduser_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email,
        renew__exact='',
        )

    rexpireduser_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')

    expireduser_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email,
        renew__exact='',
        )

    rexpireduser_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')

    expireduser_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email,
        renew__exact='',
        )

    rexpireduser_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')

    # Expired Membership Length
    lenexpireduser_monthly = len(Monthly.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email
    ))
    lenexpireduser_annual = len(Annual.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email
    ))
    lenexpireduser_custom = len(Custom.objects.select_related().filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        email__exact=current_user.email
    ))

    # Expired Notification 3 days
    previous = timezone.now() + timedelta(days=3)
    daysexpireduser3_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )
    previous = timezone.now() + timedelta(days=3)
    daysexpireduser3_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )
    previous = timezone.now() + timedelta(days=3)
    daysexpireduser3_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )

    previous = timezone.now() + timedelta(days=3)
    rdaysexpireduser3_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')
    previous = timezone.now() + timedelta(days=3)
    rdaysexpireduser3_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')
    previous = timezone.now() + timedelta(days=3)
    rdaysexpireduser3_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')

    # Expired Notification 2 days
    previous = timezone.now() + timedelta(days=2)
    daysexpireduser2_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )
    previous = timezone.now() + timedelta(days=2)
    daysexpireduser2_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )
    previous = timezone.now() + timedelta(days=2)
    daysexpireduser2_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )

    previous = timezone.now() + timedelta(days=2)
    rdaysexpireduser2_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')
    previous = timezone.now() + timedelta(days=2)
    rdaysexpireduser2_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')
    previous = timezone.now() + timedelta(days=2)
    rdaysexpireduser2_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')
    

    # Expired Notification 1 day
    previous = timezone.now() + timedelta(days=1)
    daysexpireduser1_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )
    previous = timezone.now() + timedelta(days=1)
    daysexpireduser1_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )
    previous = timezone.now() + timedelta(days=1)
    daysexpireduser1_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )

    previous = timezone.now() + timedelta(days=1)
    rdaysexpireduser1_monthly = Monthly.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')
    previous = timezone.now() + timedelta(days=1)
    rdaysexpireduser1_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')
    previous = timezone.now() + timedelta(days=1)
    rdaysexpireduser1_custom = Custom.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')

    # Expired Notification 1 Month = Annual Membership Only
    previous = timezone.now() + timedelta(days=30)
    daysexpireduser30_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )
    previous = timezone.now() + timedelta(days=30)
    rdaysexpireduser30_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')

    # Expired Notification 1 Week = Annual Membership Only
    previous = timezone.now() + timedelta(days=7)
    daysexpireduser7_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__exact='',
    )
    previous = timezone.now() + timedelta(days=70)
    rdaysexpireduser7_annual = Annual.objects.select_related().filter(
        is_verified=1,
        end_date=previous,
        email__exact=current_user.email,
        renew__isnull=False,
    ).exclude(renew__exact='')

    # Cancel Membership
    cancel_monthly = Monthly.objects.select_related().filter(
        is_verified=0,
        is_cancel=1,
        email__exact=current_user.email,
        ss_email__exact='',
        payment__exact='',
        )
    rcancel_monthly = Monthly.objects.select_related().filter(
        is_verified=0,
        is_cancel=1,
        email__exact=current_user.email,
        ss_email__isnull=False,
        payment__isnull=False,
    ).exclude(ss_email__exact='', payment__exact='')

    cancel_annual = Annual.objects.select_related().filter(
        is_verified=0,
        is_cancel=1,
        email__exact=current_user.email,
        ss_email__exact='',
        payment__exact='',
        )
    rcancel_annual = Annual.objects.select_related().filter(
        is_verified=0,
        is_cancel=1,
        email__exact=current_user.email,
        ss_email__isnull=False,
        payment__isnull=False,
    ).exclude(ss_email__exact='', payment__exact='')

    cancel_custom = Custom.objects.select_related().filter(
        is_verified=0,
        is_cancel=1,
        email__exact=current_user.email,
        ss_email__exact='',
        payment__exact='',
        )
    rcancel_custom = Custom.objects.select_related().filter(
        is_verified=0,
        is_cancel=1,
        email__exact=current_user.email,
        ss_email__isnull=False,
        payment__isnull=False,
    ).exclude(ss_email__exact='', payment__exact='')

    monthly = Monthly.objects.all()
    annual = Annual.objects.all()
    

    context = {
        'users': users,
        'monthly': monthly,
        'annual': annual,
        'user_monthly': user_monthly,
        'user_annual': user_annual,
        'user_custom': user_custom,
        'lenuser_monthly': lenuser_monthly,
        'lenuser_annual': lenuser_annual,
        'lenuser_custom': lenuser_custom,
        'nvuser_monthly': nvuser_monthly,
        'nvuser_annual': nvuser_annual,
        'nvuser_custom': nvuser_custom,
        'expireduser_monthly': expireduser_monthly,
        'expireduser_annual': expireduser_annual,
        'expireduser_custom': expireduser_custom,
        'rexpireduser_monthly': rexpireduser_monthly,
        'rexpireduser_annual': rexpireduser_annual,
        'rexpireduser_custom': rexpireduser_custom,
        'lenexpireduser_monthly': lenexpireduser_monthly,
        'lenexpireduser_annual': lenexpireduser_annual,
        'lenexpireduser_custom': lenexpireduser_custom,
        'daysexpireduser3_monthly': daysexpireduser3_monthly,
        'daysexpireduser3_annual': daysexpireduser3_annual,
        'daysexpireduser3_custom': daysexpireduser3_custom,
        'rdaysexpireduser3_monthly': rdaysexpireduser3_monthly,
        'rdaysexpireduser3_annual': rdaysexpireduser3_annual,
        'rdaysexpireduser3_custom': rdaysexpireduser3_custom,
        'daysexpireduser2_monthly': daysexpireduser2_monthly,
        'daysexpireduser2_annual': daysexpireduser2_annual,
        'daysexpireduser2_custom': daysexpireduser2_custom,
        'rdaysexpireduser2_monthly': rdaysexpireduser2_monthly,
        'rdaysexpireduser2_annual': rdaysexpireduser2_annual,
        'rdaysexpireduser2_custom': rdaysexpireduser2_custom,
        'daysexpireduser1_monthly': daysexpireduser1_monthly,
        'daysexpireduser1_annual': daysexpireduser1_annual,
        'daysexpireduser1_custom': daysexpireduser1_custom,
        'rdaysexpireduser1_monthly': rdaysexpireduser1_monthly,
        'rdaysexpireduser1_annual': rdaysexpireduser1_annual,
        'rdaysexpireduser1_custom': rdaysexpireduser1_custom,
        'daysexpireduser30_annual': daysexpireduser30_annual,
        'rdaysexpireduser30_annual': rdaysexpireduser30_annual,
        'daysexpireduser7_annual': daysexpireduser7_annual,
        'rdaysexpireduser7_annual': rdaysexpireduser7_annual,
        'cancel_monthly': cancel_monthly,
        'cancel_annual': cancel_annual,
        'cancel_custom': cancel_custom,
        'rcancel_monthly': rcancel_monthly,
        'rcancel_annual': rcancel_annual,
        'rcancel_custom': rcancel_custom
    }
    return render(request, "membership/home.html", context)

@login_required(login_url='/signin/')
def renew_monthly(request, id):
    # User = get_user_model()
    users = Monthly.objects.get(id=id)
   
    if request.method == "POST":
        users.renew = request.FILES.get('renew')
        users.renew_price = 550
        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/rmonthlymembership.html", context)

@login_required(login_url='/signin/')
def renewmonthly_accept(request, id):
    monthly = Monthly.objects.get(id=id)

    if len(monthly.file) > 0:
        os.remove(monthly.file.path)
    monthly.file = None
    monthly.file = monthly.renew
    monthly.renew = None
    
    monthly.price = None
    monthly.price = monthly.renew_price
    monthly.renew_price = None

    start = monthly.end_date
    end = timedelta(days=30)

    monthly.start_date = start
    monthly.end_date = monthly.start_date + end
    
    monthly.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewmonthly_delete(request, id):
    monthly = Monthly.objects.get(id=id)
    if len(monthly.renew) > 0:
        os.remove(monthly.renew.path)
    monthly.renew = None
    monthly.renew_price = None

    monthly.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewmonthly_view(request, id):
    monthly = Monthly.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'monthly': monthly,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/rmonthlyview.html", context)

@login_required(login_url='/signin/')
def renew_annual(request, id):
    # User = get_user_model()
    users = Annual.objects.get(id=id)
   
    if request.method == "POST":
        users.renew = request.FILES.get('renew')
        users.renew_price = 6000
        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/rannualmembership.html", context)

@login_required(login_url='/signin/')
def renewannual_accept(request, id):
    annual = Annual.objects.get(id=id)

    if len(annual.file) > 0:
        os.remove(annual.file.path)
    annual.file = None
    annual.file = annual.renew
    annual.renew = None

    annual.price = None
    annual.price = annual.renew_price
    annual.renew_price = None

    start = annual.end_date
    end = timedelta(days=366)

    annual.start_date = start
    annual.end_date = annual.start_date + end
    
    annual.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewannual_delete(request, id):
    annual = Annual.objects.get(id=id)
    if len(annual.renew) > 0:
        os.remove(annual.renew.path)
    annual.renew = None
    annual.renew_price = None

    annual.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewannual_view(request, id):
    annual = Annual.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'annual': annual,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/rannualview.html", context)

def renew_custom(request, id):
    # User = get_user_model()
    users = Custom.objects.get(id=id)
    if request.method == "POST":
        users.renew_enddate = request.POST.get('renew_enddate')
        users.renew = request.FILES.get('renew')

        start = datetime.datetime.strptime(str(users.end_date), '%Y-%m-%d').date()
        end = datetime.datetime.strptime(str(users.renew_enddate), '%Y-%m-%d').date()
        days_diff = (start - end).days
        users.renew_price = abs(days_diff * 25)

        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/rcustommembership.html", context)

@login_required(login_url='/signin/')
def renewcustom_accept(request, id):
    custom = Custom.objects.get(id=id)

    if len(custom.file) > 0:
        os.remove(custom.file.path)
    custom.file = None
    custom.file = custom.renew
    custom.renew = None
    
    custom.end_date = None
    custom.end_date = custom.renew_enddate
    custom.renew_enddate = None

    custom.price = None
    custom.price = custom.renew_price
    custom.renew_price = None

    custom.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewcustom_delete(request, id):
    custom = Custom.objects.get(id=id)
    if len(custom.renew) > 0:
        os.remove(custom.renew.path)
    custom.renew = None
    custom.renew_enddate = None
    custom.renew_price = None

    custom.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewcustom_view(request, id):
    custom = Custom.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'custom': custom,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/rcustomview.html", context)

@login_required(login_url='/signin/')
def renew_monthlyexpired(request, id):
    # User = get_user_model()
    users = Monthly.objects.get(id=id)
   
    if request.method == "POST":
        users.renew = request.FILES.get('renew')
        users.renew_price = 550
        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/rmonthlyexpired.html", context)

@login_required(login_url='/signin/')
def renewmonthlyexpired_accept(request, id):
    monthly = Monthly.objects.get(id=id)

    if len(monthly.file) > 0:
        os.remove(monthly.file.path)
    monthly.file = None
    monthly.file = monthly.renew
    monthly.renew = None

    monthly.price = None
    monthly.price = monthly.renew_price
    monthly.renew_price = None

    start = timezone.now()
    end = timedelta(days=30)

    monthly.start_date = start
    monthly.end_date = monthly.start_date + end
    
    monthly.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewmonthlyexpired_delete(request, id):
    monthly = Monthly.objects.get(id=id)
    if len(monthly.renew) > 0:
        os.remove(monthly.renew.path)
    monthly.renew = None
    monthly.renew_price = None

    monthly.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewmonthlyexpired_view(request, id):
    monthly = Monthly.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'monthly': monthly,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/rmonthlyexpiredview.html", context)

@login_required(login_url='/signin/')
def renew_annualexpired(request, id):
    # User = get_user_model()
    users = Annual.objects.get(id=id)
   
    if request.method == "POST":
        users.renew = request.FILES.get('renew')
        users.renew_price = 6000
        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/rannualexpired.html", context)

@login_required(login_url='/signin/')
def renewannualexpired_accept(request, id):
    annual = Annual.objects.get(id=id)

    if len(annual.file) > 0:
        os.remove(annual.file.path)
    annual.file = None
    annual.file = annual.renew
    annual.renew = None

    annual.price = None
    annual.price = annual.renew_price
    annual.renew_price = None

    start = timezone.now()
    end = timedelta(days=366)

    annual.start_date = start
    annual.end_date = annual.start_date + end
    
    annual.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewannualexpired_delete(request, id):
    annual = Annual.objects.get(id=id)
    if len(annual.renew) > 0:
        os.remove(annual.renew.path)
    annual.renew = None
    annual.renew_price = None

    annual.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewannualexpired_view(request, id):
    annual = Annual.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'annual': annual,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/rannualexpiredview.html", context)

@login_required(login_url='/signin/')
def renew_customexpired(request, id):
    # User = get_user_model()
    users = Custom.objects.get(id=id)
   
    if request.method == "POST":
        users.renew_startdate = request.POST.get('renew_startdate')
        users.renew_enddate = request.POST.get('renew_enddate')
        users.renew = request.FILES.get('renew')

        start = datetime.datetime.strptime(str(users.renew_startdate), '%Y-%m-%d').date()
        end = datetime.datetime.strptime(str(users.renew_enddate), '%Y-%m-%d').date()
        days_diff = (start - end).days
        users.renew_price = abs(days_diff * 25)

        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/rcustomexpired.html", context)

@login_required(login_url='/signin/')
def renewcustomexpired_accept(request, id):
    custom = Custom.objects.get(id=id)

    if len(custom.file) > 0:
        os.remove(custom.file.path)
    custom.file = None
    custom.file = custom.renew
    custom.renew = None
    
    custom.start_date = None
    custom.start_date = custom.renew_startdate
    custom.renew_startdate = None

    custom.end_date = None
    custom.end_date = custom.renew_enddate
    custom.renew_enddate = None

    custom.price = None
    custom.price = custom.renew_price
    custom.renew_price = None

    custom.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewcustomexpired_delete(request, id):
    custom = Custom.objects.get(id=id)
    if len(custom.renew) > 0:
        os.remove(custom.renew.path)
    custom.renew = None
    custom.renew_startdate = None
    custom.renew_enddate = None
    custom.renew_price = None

    custom.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def renewcustomexpired_view(request, id):
    custom = Custom.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'custom': custom,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/rcustomexpiredview.html", context)

@login_required(login_url='/signin/')
def cancel_monthly(request, id):
    # User = get_user_model()
    users = Monthly.objects.get(id=id)
   
    if request.method == "POST":
        users.payment = request.FILES.get('payment')
        users.ss_email = request.FILES.get('ss_email')
        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/cancelmonthly.html", context)

@login_required(login_url='/signin/')
def cancel_annual(request, id):
    # User = get_user_model()
    users = Annual.objects.get(id=id)
   
    if request.method == "POST":
        users.payment = request.FILES.get('payment')
        users.ss_email = request.FILES.get('ss_email')
        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/cancelannual.html", context)

@login_required(login_url='/signin/')
def cancel_custom(request, id):
    # User = get_user_model()
    users = Custom.objects.get(id=id)
   
    if request.method == "POST":
        users.payment = request.FILES.get('payment')
        users.ss_email = request.FILES.get('ss_email')
        users.save()
        return redirect('home')
    context = {
        'users': users
    }
    return render(request, "membership/cancelcustom.html", context)

@login_required(login_url='/signin/')
def cancelmonthly_view(request, id):
    monthly = Monthly.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'monthly': monthly,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/cancelmonthlyview.html", context)

@login_required(login_url='/signin/')
def cancelannual_view(request, id):
    annual = Annual.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'annual': annual,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/cancelannualview.html", context)

@login_required(login_url='/signin/')
def cancelcustom_view(request, id):
    custom = Custom.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'custom': custom,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/cancelcustomview.html", context)

@login_required(login_url='/signin/')
def monthly_delete(request, id):
    membership = Monthly.objects.get(id=id)

    if membership.file != '':
        if len(membership.file) > 0:
            os.remove(membership.file.path)
        if len(membership.photo) > 0:
            os.remove(membership.photo.path)
    

    membership.delete()
    return redirect('membership')

@login_required(login_url='/signin/')
def annual_delete(request, id):
    membership = Annual.objects.get(id=id)

    if len(membership.file) > 0:
        os.remove(membership.file.path)
    if len(membership.photo) > 0:
        os.remove(membership.photo.path)

    membership.delete()
    return redirect('membership')

@login_required(login_url='/signin/')
def custom_delete(request, id):
    membership = Custom.objects.get(id=id)

    if len(membership.file) > 0:
        os.remove(membership.file.path)
    if len(membership.photo) > 0:
        os.remove(membership.photo.path)

    membership.delete()
    return redirect('membership')

@login_required(login_url='/signin/')
def monthly_accept(request, id):
    monthly = Monthly.objects.get(id=id)
    monthly.is_verified = 1

    start = timezone.now()
    end = timedelta(days=30)

    monthly.start_date = start
    monthly.end_date = monthly.start_date + end
    
    monthly.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def annual_accept(request, id):
    annual = Annual.objects.get(id=id)
    annual.is_verified = 1
    
    start = timezone.now()
    end = timedelta(days=366)

    annual.start_date = start
    annual.end_date = annual.start_date + end
    
    annual.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def custom_accept(request, id):
    custom = Custom.objects.get(id=id)
    custom.is_verified = 1

    custom.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def monthlymembership_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(buffer, pagesize=(400,250), bottomup=0)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.translate(inch, inch)
    # Designate Model

    bg = MEDIA_ROOT + 'membership/static/files/Monthly-Front.png'
    c.saveState()
    c.scale(1, -1)
    x_val = -1*inch
    y_val = -2.5*inch
    c.drawImage(bg, x_val, y_val, 400, 250)
    c.restoreState()

    current_user = request.user
    user_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    )

    User = get_user_model()
    current_user = request.user
    user = User.objects.filter(
        email__exact=current_user.email
    )
 
    image = []
    for im in user_monthly:
        image.append(im.photo.url)

    img = MEDIA_ROOT + str(image)[1:-1].replace("'", "")
    c.saveState()
    c.scale(1, -1)
    x_val = -0.7*inch
    y_val = -1.2*inch
    c.drawImage(img, x_val, y_val, 1.2*inch, 1.2*inch)
    c.restoreState()

    c.setFillColorRGB(0.75390625,0.984375,0.44140625)
    c.setFont("Courier-Bold", 16)
    unique_id = []
    for unid in user_monthly:
        unique_id.append(unid.unique_id)

    c.drawString(-0.7*inch, 1.5*inch, str(unique_id)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 16)
    full_name = []
    for fn in user_monthly:
        full_name.append(fn.full_name)

    c.drawString(-0.7*inch, 1.75*inch, str(full_name)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    email = []
    for em in user:
        email.append(em.email)

    c.drawString(-0.7*inch, 2*inch, str(email)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    contact_no = []
    for cn in user_monthly:
        contact_no.append(cn.contact_no)

    c.drawString(-0.7*inch, 2.15*inch, "+63" + str(contact_no)[1:-1].replace("'", ""))

    c.setFillColorRGB(0.75390625,0.984375,0.44140625)
    c.setFont("Courier-Bold", 10)
    end_date = []
    for ed in user_monthly:
        end_date.append(ed.end_date.strftime('%Y-%m-%d'))

    c.drawString(2.3*inch, 2.25*inch, "EXPIRY DATE: ")
    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    c.drawString(3.4*inch, 2.26*inch, str(end_date)[1:-1].replace("'", ""))

    c.showPage()

    bg2 = MEDIA_ROOT + 'membership/static/files/Back.png'
    c.saveState()
    c.scale(1, -1)
    x_val = 0*inch
    y_val = -3.5*inch
    c.drawImage(bg2, x_val, y_val, 400, 250)
    c.restoreState()

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_fullname = []
    for emfn in user_monthly:
        em_fullname.append(emfn.em_fullname)

    c.drawString(2.75*inch, 1.55*inch, ": " + str(em_fullname)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_email = []
    for emem in user_monthly:
        em_email.append(emem.em_email)

    c.drawString(2.75*inch, 1.73*inch, ": " + str(em_email)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    relationship = []
    for emr in user_monthly:
        relationship.append(emr.relationship)

    c.drawString(3.14*inch, 1.915*inch, ": " + str(relationship)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_contactno = []
    for emcn in user_monthly:
        em_contactno.append(emcn.em_contactno)
    
    c.drawString(2.78*inch, 2.1*inch, ": +63" + str(em_contactno)[1:-1].replace("'", ""))

    c.showPage()
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='membership.pdf')

@login_required(login_url='/signin/')
def annualmembership_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(buffer, pagesize=(400,250), bottomup=0)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.translate(inch, inch)
    # Designate Model

    bg = MEDIA_ROOT + 'membership/static/files/Annual-Front.png'
    c.saveState()
    c.scale(1, -1)
    x_val = -1*inch
    y_val = -2.5*inch
    c.drawImage(bg, x_val, y_val, 400, 250)
    c.restoreState()

    current_user = request.user
    user_annual = Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    )

    User = get_user_model()
    current_user = request.user
    user = User.objects.filter(
        email__exact=current_user.email
    )
 
    image = []
    for im in user_annual:
        image.append(im.photo.url)

    img = MEDIA_ROOT + str(image)[1:-1].replace("'", "")
    c.saveState()
    c.scale(1, -1)
    x_val = -0.7*inch
    y_val = -1.2*inch
    c.drawImage(img, x_val, y_val, 1.2*inch, 1.2*inch)
    c.restoreState()

    c.setFillColorRGB(0.75390625,0.984375,0.44140625)
    c.setFont("Courier-Bold", 16)
    unique_id = []
    for unid in user_annual:
        unique_id.append(unid.unique_id)

    c.drawString(-0.7*inch, 1.5*inch, str(unique_id)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 16)
    full_name = []
    for fn in user_annual:
        full_name.append(fn.full_name)

    c.drawString(-0.7*inch, 1.75*inch, str(full_name)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    email = []
    for em in user:
        email.append(em.email)

    c.drawString(-0.7*inch, 2*inch, str(email)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    contact_no = []
    for cn in user_annual:
        contact_no.append(cn.contact_no)

    c.drawString(-0.7*inch, 2.15*inch, "+63" + str(contact_no)[1:-1].replace("'", ""))

    c.setFillColorRGB(0.75390625,0.984375,0.44140625)
    c.setFont("Courier-Bold", 10)
    end_date = []
    for ed in user_annual:
        end_date.append(ed.end_date.strftime('%Y-%m-%d'))

    c.drawString(2.3*inch, 2.25*inch, "EXPIRY DATE: ")
    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    c.drawString(3.4*inch, 2.26*inch, str(end_date)[1:-1].replace("'", ""))

    c.showPage()

    bg2 = MEDIA_ROOT + 'membership/static/files/Back.png'
    c.saveState()
    c.scale(1, -1)
    x_val = 0*inch
    y_val = -3.5*inch
    c.drawImage(bg2, x_val, y_val, 400, 250)
    c.restoreState()

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_fullname = []
    for emfn in user_annual:
        em_fullname.append(emfn.em_fullname)

    c.drawString(2.75*inch, 1.55*inch, ": " + str(em_fullname)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_email = []
    for emem in user_annual:
        em_email.append(emem.em_email)

    c.drawString(2.75*inch, 1.73*inch, ": " + str(em_email)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    relationship = []
    for emr in user_annual:
        relationship.append(emr.relationship)

    c.drawString(3.14*inch, 1.915*inch, ": " + str(relationship)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_contactno = []
    for emcn in user_annual:
        em_contactno.append(emcn.em_contactno)
    
    c.drawString(2.78*inch, 2.1*inch, ": +63" + str(em_contactno)[1:-1].replace("'", ""))

    c.showPage()
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='membership.pdf')

@login_required(login_url='/signin/')
def custommembership_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(buffer, pagesize=(400,250), bottomup=0)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.translate(inch, inch)
    # Designate Model

    bg = MEDIA_ROOT + 'membership/static/files/Custom-Front.png'
    c.saveState()
    c.scale(1, -1)
    x_val = -1*inch
    y_val = -2.5*inch
    c.drawImage(bg, x_val, y_val, 400, 250)
    c.restoreState()

    current_user = request.user
    user_custom = Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        email__exact=current_user.email
    )

    User = get_user_model()
    current_user = request.user
    user = User.objects.filter(
        email__exact=current_user.email
    )
 
    image = []
    for im in user_custom:
        image.append(im.photo.url)

    img = MEDIA_ROOT + str(image)[1:-1].replace("'", "")
    c.saveState()
    c.scale(1, -1)
    x_val = -0.7*inch
    y_val = -1.2*inch
    c.drawImage(img, x_val, y_val, 1.2*inch, 1.2*inch)
    c.restoreState()

    c.setFillColorRGB(0.75390625,0.984375,0.44140625)
    c.setFont("Courier-Bold", 16)
    unique_id = []
    for unid in user_custom:
        unique_id.append(unid.unique_id)

    c.drawString(-0.7*inch, 1.5*inch, str(unique_id)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 16)
    full_name = []
    for fn in user_custom:
        full_name.append(fn.full_name)

    c.drawString(-0.7*inch, 1.75*inch, str(full_name)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    email = []
    for em in user:
        email.append(em.email)

    c.drawString(-0.7*inch, 2*inch, str(email)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    contact_no = []
    for cn in user_custom:
        contact_no.append(cn.contact_no)

    c.drawString(-0.7*inch, 2.15*inch, "+63" + str(contact_no)[1:-1].replace("'", ""))

    c.setFillColorRGB(0.75390625,0.984375,0.44140625)
    c.setFont("Courier-Bold", 10)
    start_date = []
    for sd in user_custom:
        start_date.append(sd.start_date.strftime('%Y-%m-%d'))

    c.drawString(2.38*inch, 2.05*inch, "START DATE: ")
    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    c.drawString(3.4*inch, 2.06*inch, str(start_date)[1:-1].replace("'", ""))

    c.setFillColorRGB(0.75390625,0.984375,0.44140625)
    c.setFont("Courier-Bold", 10)
    end_date = []
    for ed in user_custom:
        end_date.append(ed.end_date.strftime('%Y-%m-%d'))

    c.drawString(2.3*inch, 2.25*inch, "EXPIRY DATE: ")
    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    c.drawString(3.4*inch, 2.26*inch, str(end_date)[1:-1].replace("'", ""))

    c.showPage()

    bg2 = MEDIA_ROOT + 'membership/static/files/Back.png'
    c.saveState()
    c.scale(1, -1)
    x_val = 0*inch
    y_val = -3.5*inch
    c.drawImage(bg2, x_val, y_val, 400, 250)
    c.restoreState()

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_fullname = []
    for emfn in user_custom:
        em_fullname.append(emfn.em_fullname)

    c.drawString(2.75*inch, 1.55*inch, ": " + str(em_fullname)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_email = []
    for emem in user_custom:
        em_email.append(emem.em_email)

    c.drawString(2.75*inch, 1.73*inch, ": " + str(em_email)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    relationship = []
    for emr in user_custom:
        relationship.append(emr.relationship)

    c.drawString(3.14*inch, 1.915*inch, ": " + str(relationship)[1:-1].replace("'", ""))

    c.setFillColorRGB(1,1,1)
    c.setFont("Courier-Bold", 10)
    em_contactno = []
    for emcn in user_custom:
        em_contactno.append(emcn.em_contactno)
    
    c.drawString(2.78*inch, 2.1*inch, ": +63" + str(em_contactno)[1:-1].replace("'", ""))

    c.showPage()
    c.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='membership.pdf')

@login_required(login_url='/signin/')
def admin_view(request):
    # Create a sidebar for Accounts, Membership
    # Accounts display all the regiestered accounts and their data
    # Membership display all the Membership + accept button
    # Use the exist() to check if email is already in the database and compare it to current_use.email
    # also if is_verified = false to display -please wait your membership is currently in process-
    # in their home instead of the 3 membership
    # If current_user.email not exist() in the database display 3 membership
    # If current_user.email exist() in the database and also if is_verified = true display ID download
    
    # If current_user.email exist() in the database
        # If is_verified=True
            # Display ID
        # Else
            # Display membership application currently in progress
    # Else 
        # Dislay 3 membership

    User = get_user_model()
    users = User.objects.all()
    monthly = Monthly.objects.all()
    annual = Annual.objects.all()

    numberof_user = len(User.objects.all())
    new_user = User.objects.filter(
        id__gt=0,
    ).order_by('id').reverse()[:5:1]


    context = {
        'users': users,
        'monthly': monthly,
        'annual': annual,
        'numberof_user': numberof_user,
        'new_user': new_user
    }
    return render(request, "membership/adminpage.html", context)

@login_required(login_url='/signin/')
def admin_search(request):
    if request.method == "POST":
        search = request.POST['search']
        User = get_user_model()
        users = User.objects.filter(Q(
            email__icontains=search
            ) | Q(
            user_name__icontains=search
            ))

        numberof_user = len(User.objects.filter(Q(
            email__icontains=search
            ) | Q(
            user_name__icontains=search
        )))
        new_user = User.objects.filter(
            id__gt=0,
        ).order_by('id').reverse()[:5:1]


        context = {
            'users': users,
            'numberof_user': numberof_user,
            'new_user': new_user,
            'search': search
        }
        return render(request, "membership/adminsearch.html", context)
    return redirect('adminpage')


@login_required(login_url='/signin/')
def users_edit(request, id):
    User = get_user_model()
    users = User.objects.get(id=id)
    new_user = User.objects.filter(
        id__gt=0,
    ).order_by('id').reverse()[:5:1]
    if request.method == "POST":
        users.email = request.POST.get('email')
        users.user_name = request.POST.get('user_name')
        users.is_superuser = request.POST.get('is_superuser')
        users.is_staff = request.POST.get('is_staff')
        if users.is_superuser == 'True':
            users.is_superuser = 1
            if users.is_staff == 'True':
                users.is_staff = 1
                users.save()
                return redirect('adminpage')
            else:
                users.is_staff = 0
                users.save()
                return redirect('adminpage')
        else:
            users.is_superuser = 0
        if users.is_staff == 'True':
            users.is_staff = 1
            users.save()
            return redirect('adminpage')
        else:
            users.is_staff = 0
        users.save()
        return redirect('adminpage')
    context = {
        'users': users,
        'new_user': new_user
        
    }
    return render(request, "membership/usersedit.html", context)

@login_required(login_url='/signin/')
def users_delete(request, id):
    User = get_user_model()
    users = User.objects.filter(id=id)
    users.delete()
    return redirect('adminpage')

@login_required(login_url='/signin/')
def monthlymembership_view(request, id):
    monthly = Monthly.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'monthly': monthly,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/monthlymembershipview.html", context)

@login_required(login_url='/signin/')
def annualmembership_view(request, id):
    annual = Annual.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'annual': annual,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/annualmembershipview.html", context)

@login_required(login_url='/signin/')
def custommembership_view(request, id):
    custom = Custom.objects.get(id=id)
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'custom': custom,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'customnew_application': customnew_application,
        'nvcustomnew_application': nvcustomnew_application
    }
    return render(request, "membership/custommembershipview.html", context)

@login_required(login_url='/signin/')
def monthlymembership_accept(request, id):
    monthly = Monthly.objects.get(id=id)
    monthly.is_verified = 1
    monthly.is_cancel = 0
    if len(monthly.ss_email) > 0:
        os.remove(monthly.ss_email.path)
    if len(monthly.payment) > 0:
        os.remove(monthly.payment.path)
    monthly.ss_email = None
    monthly.payment = None
    start = timezone.now()
    end = timedelta(days=30)

    monthly.start_date = start
    monthly.end_date = monthly.start_date + end
    
    monthly.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def annualmembership_accept(request, id):
    annual = Annual.objects.get(id=id)
    annual.is_verified = 1
    annual.is_cancel = 0
    if len(annual.ss_email) > 0:
        os.remove(annual.ss_email.path)
    if len(annual.payment) > 0:
        os.remove(annual.payment.path)
    annual.ss_email = None
    annual.payment = None
    start = timezone.now()
    end = timedelta(days=366)

    annual.start_date = start
    annual.end_date = annual.start_date + end
    
    annual.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def custommembership_accept(request, id):
    custom = Custom.objects.get(id=id)
    custom.is_verified = 1
    custom.is_cancel = 0
    if len(custom.ss_email) > 0:
        os.remove(custom.ss_email.path)
    if len(custom.payment) > 0:
        os.remove(custom.payment.path)
    custom.ss_email = None
    custom.payment = None

    custom.save()
    return redirect('membership')

@login_required(login_url='/signin/')
def monthlymembership_delete(request, id):
    membership = Monthly.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        message = request.POST['message']
        send_mail(
            title,
            message,
            'settings.EMAIL_HOST_USER',
            [membership.email],
            fail_silently=False,
        )
        membership.is_cancel = 1
        membership.save()
        return redirect('membership')
    return render(request, "membership/monthlymembershipdelete.html")

@login_required(login_url='/signin/')
def annualmembership_delete(request, id):
    membership = Annual.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        message = request.POST['message']
        send_mail(
            title,
            message,
            'settings.EMAIL_HOST_USER',
            [membership.email],
            fail_silently=False,
        )
        membership.is_cancel = 1
        membership.save()
        return redirect('membership')
    return render(request, "membership/annualmembershipdelete.html")

@login_required(login_url='/signin/')
def custommembership_delete(request, id):
    membership = Custom.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        message = request.POST['message']
        send_mail(
            title,
            message,
            'settings.EMAIL_HOST_USER',
            [membership.email],
            fail_silently=False,
        )
        membership.is_cancel = 1
        membership.save()
        return redirect('membership')
    return render(request, "membership/custommembershipdelete.html")

@login_required(login_url='/signin/')
def membership_search(request):
    if request.method == "POST":
        search = request.POST['search']
        User = get_user_model()
        users = User.objects.all()

        # Active Membership
        verified_monthly = Monthly.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            email__email__icontains=search,
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )).order_by('-end_date').reverse()
        verified_annual = Annual.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )).order_by('-end_date').reverse()
        verified_custom = Custom.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )).order_by('-end_date').reverse()
        
        # Active Membership Lenth
        nverified_monthly = len(Monthly.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )))
        nverified_annual = len(Annual.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )))
        nverified_custom = len(Custom.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )))

        # Renew Active Membership
        rverified_monthly = Monthly.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            unique_id__icontains=search
            )).exclude(renew__exact='').order_by('-end_date').reverse()
        rverified_annual = Annual.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            unique_id__icontains=search
            )).exclude(renew__exact='').order_by('-end_date').reverse()
        rverified_custom = Custom.objects.filter(Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__gt=timezone.now(),
            renew__isnull=False,
            unique_id__icontains=search
            )).exclude(renew__exact='').order_by('-end_date').reverse()

        
        # Renew Active Membership Length
        nrverified_monthly = len(Monthly.objects.filter(Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )).exclude(renew__exact=''))
        nrverified_annual = len(Annual.objects.filter(Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )).exclude(renew__exact=''))
        nrverified_custom = len(Custom.objects.filter(Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__gt=timezone.now(),
            unique_id__icontains=search
            )).exclude(renew__exact=''))

        # Membership 3 days
        previous = timezone.now() + timedelta(days=3)
        severified_monthly = Monthly.objects.filter(Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            unique_id__icontains=search
            ))
        severified_annual = Annual.objects.filter(Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            unique_id__icontains=search
            ))
        severified_custom = Custom.objects.filter(Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            unique_id__icontains=search
            ))
        
        # Membership 3 days Length
        previous = timezone.now() + timedelta(days=3)
        nseverified_monthly = len(Monthly.objects.filter(Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            unique_id__icontains=search
            )))
        nseverified_annual = len(Annual.objects.filter(Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            unique_id__icontains=search
            )))
        nseverified_custom = len(Custom.objects.filter(Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            unique_id__icontains=search
            )))

        # Not Verified
        monthly = Monthly.objects.filter(Q(
            is_verified=0,
            email__email__icontains=search
            ) | Q(
            is_verified=0,
            full_name__icontains=search
            ))
        annual = Annual.objects.filter(Q(
            is_verified=0,
            email__email__icontains=search
            ) | Q(
            is_verified=0,
            full_name__icontains=search
            ))
        custom = Custom.objects.filter(Q(
            is_verified=0,
            email__email__icontains=search
            ) | Q(
            is_verified=0,
            full_name__icontains=search
            ))

        # Not Verified Lenth
        nnotverified_monthly = len(Monthly.objects.filter(Q(
            is_verified=0,
            email__email__icontains=search
            ) | Q(
            is_verified=0,
            full_name__icontains=search
            )))
        nnotverified_annual = len(Annual.objects.filter(Q(
            is_verified=0,
            email__email__icontains=search
            ) | Q(
            is_verified=0,
            full_name__icontains=search
            )))
        nnotverified_custom = len(Custom.objects.filter(Q(
            is_verified=0,
            email__email__icontains=search
            ) | Q(
            is_verified=0,
            full_name__icontains=search
            )))

        # Expired
        expired_monthly = Monthly.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            ))
        expired_annual = Annual.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            ))
        expired_custom = Custom.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            ))
        
        # Expired Lenght
        nexpired_monthly = len( Monthly.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            )))
        nexpired_annual = len(Annual.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            )))
        nexpired_custom = len(Custom.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            )))


        # Renew Expired Membership
        rexpired_monthly = Monthly.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            unique_id__icontains=search
            )).exclude(renew__exact='').order_by('-end_date').reverse()
        rexpired_annual = Annual.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            unique_id__icontains=search
            )).exclude(renew__exact='').order_by('-end_date').reverse()
        rexpired_custom = Custom.objects.filter(Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            end_date__lte=timezone.now(),
            renew__isnull=False,
            unique_id__icontains=search
            )).exclude(renew__exact='').order_by('-end_date').reverse()

        # Renew Active Membership Length
        nrexpired_monthly = len(Monthly.objects.filter(Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            )).exclude(renew__exact=''))
        nrexpired_annual = len(Annual.objects.filter(Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            )).exclude(renew__exact=''))
        nrexpired_custom = len(Custom.objects.filter(Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            email__email__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            full_name__icontains=search
            ) | Q(
            is_verified=1,
            renew__isnull=False,
            end_date__lte=timezone.now(),
            unique_id__icontains=search
            )).exclude(renew__exact=''))


        # Right Side Bar
        monthlynew_application = Monthly.objects.filter(
            id__gt=0,
            is_verified=1,
            end_date__gt=timezone.now()
        ).order_by('id').reverse()[:2:1]
        nvmonthlynew_application = Monthly.objects.filter(
            id__gt=0,
            is_verified=0
        ).order_by('id').reverse()[:2:1]
        annualnew_application = Annual.objects.filter(
            id__gt=0,
            is_verified=1,
            end_date__gt=timezone.now()
        ).order_by('id').reverse()[:2:1]
        nvannualnew_application = Annual.objects.filter(
            id__gt=0,
            is_verified=0
        ).order_by('id').reverse()[:2:1]
        customnew_application = Custom.objects.filter(
            id__gt=0,
            is_verified=1,
            end_date__gt=timezone.now()
        ).order_by('id').reverse()[:2:1]
        nvcustomnew_application = Custom.objects.filter(
            id__gt=0,
            is_verified=0
        ).order_by('id').reverse()[:2:1]


        context = {
            'users': users,
            'verified_monthly': verified_monthly,
            'verified_annual': verified_annual,
            'verified_custom': verified_custom,
            'severified_monthly': severified_monthly,
            'severified_annual': severified_annual,
            'severified_custom': severified_custom,
            'nseverified_monthly': nseverified_monthly,
            'nseverified_annual': nseverified_annual,
            'nseverified_custom': nseverified_custom,
            'nverified_monthly': nverified_monthly,
            'nverified_annual': nverified_annual,
            'nverified_custom': nverified_custom,
            'rverified_monthly': rverified_monthly,
            'rverified_annual': rverified_annual,
            'rverified_custom': rverified_custom,
            'nrverified_monthly': nrverified_monthly,
            'nrverified_annual': nrverified_annual,
            'nrverified_custom': nrverified_custom,
            'expired_monthly': expired_monthly,
            'expired_annual': expired_annual,
            'expired_custom': expired_custom,
            'nexpired_monthly': nexpired_monthly,
            'nexpired_annual': nexpired_annual,
            'nexpired_custom': nexpired_custom,
            'rexpired_monthly': rexpired_monthly,
            'rexpired_annual': rexpired_annual,
            'rexpired_custom': rexpired_custom,
            'nrexpired_monthly': nrexpired_monthly,
            'nrexpired_annual': nrexpired_annual,
            'nrexpired_custom': nrexpired_custom,
            'monthly': monthly,
            'annual': annual,
            'custom': custom,
            'nnotverified_monthly': nnotverified_monthly,
            'nnotverified_annual': nnotverified_annual,
            'nnotverified_custom': nnotverified_custom,
            'monthlynew_application': monthlynew_application,
            'annualnew_application': annualnew_application,
            'customnew_application': customnew_application,
            'nvmonthlynew_application': nvmonthlynew_application,
            'nvannualnew_application': nvannualnew_application,
            'nvcustomnew_application': nvcustomnew_application,
            'search': search,
        }
        return render(request, "membership/membershipsearch.html", context)
    return redirect('membership')

@login_required(login_url='/signin/')
def membership_view(request):
    User = get_user_model()
    users = User.objects.all()

    # Active Membership
    verified_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ).order_by('-end_date').reverse()
    verified_annual = Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ).order_by('-end_date').reverse()
    verified_custom = Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ).order_by('-end_date').reverse()
    
    # Active Membership Lenth
    nverified_monthly = len( Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ))
    nverified_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ))
    nverified_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ))

    # Renew Active Membership
    rverified_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    rverified_annual = Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    rverified_custom = Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()

    
    # Renew Active Membership Length
    nrverified_monthly = len(Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    nrverified_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    nrverified_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))

    # Membership 3 days
    previous = timezone.now() + timedelta(days=3)
    severified_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        )
    severified_annual = Annual.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        )
    severified_custom = Custom.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        )

    # Membership 3 days Length
    previous = timezone.now() + timedelta(days=3)
    nseverified_monthly = len(Monthly.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        ))
    nseverified_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        ))
    nseverified_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        ))

    # Not Verified
    monthly = Monthly.objects.filter(
        is_verified=0,
        is_cancel=0
        )
    annual = Annual.objects.filter(
        is_verified=0,
        is_cancel=0
        )
    custom = Custom.objects.filter(
        is_verified=0,
        is_cancel=0
        )
    
    # Not Verified Length
    nnotverified_monthly = len(Monthly.objects.filter(
        is_verified=0,
        is_cancel=0
        ))
    nnotverified_annual = len(Annual.objects.filter(
        is_verified=0,
        is_cancel=0
        ))
    nnotverified_custom = len(Custom.objects.filter(
        is_verified=0,
        is_cancel=0
        ))

    # Cancel Membership
    cancel_monthly = Monthly.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact='')
    cancel_annual = Annual.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact='')
    cancel_custom = Custom.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact='')
    
    # Cancel Membership Length
    ncancel_monthly = len(Monthly.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact=''))
    ncancel_annual = len(Annual.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact=''))
    ncancel_custom = len(Custom.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact=''))

    # Expired Membership
    expired_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        )
    expired_annual = Annual.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        )
    expired_custom = Custom.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        )
    
    # Expired Membership Length
    nexpired_monthly = len( Monthly.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        ))
    nexpired_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        ))
    nexpired_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        ))
    
    # Renew Expired Membership
    rexpired_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    rexpired_annual = Annual.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    rexpired_custom = Custom.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()

    # Renew Expired Membership Length
    nrexpired_monthly = len(Monthly.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    nrexpired_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    nrexpired_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))

    # Right Side Bar
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'users': users,
        'verified_monthly': verified_monthly,
        'verified_annual': verified_annual,
        'verified_custom': verified_custom,
        'severified_monthly': severified_monthly,
        'severified_annual': severified_annual,
        'severified_custom': severified_custom,
        'nseverified_monthly': nseverified_monthly,
        'nseverified_annual': nseverified_annual,
        'nseverified_custom': nseverified_custom,
        'expired_monthly': expired_monthly,
        'expired_annual': expired_annual,
        'expired_custom': expired_custom,
        'nexpired_monthly': nexpired_monthly,
        'nexpired_annual': nexpired_annual,
        'nexpired_custom': nexpired_custom,
        'monthly': monthly,
        'annual': annual,
        'custom': custom,
        'nverified_monthly': nverified_monthly,
        'nverified_annual': nverified_annual,
        'nverified_custom': nverified_custom,
        'nnotverified_monthly': nnotverified_monthly,
        'nnotverified_annual': nnotverified_annual,
        'nnotverified_custom': nnotverified_custom,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'customnew_application': customnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'nvcustomnew_application': nvcustomnew_application,
        'rverified_monthly': rverified_monthly,
        'nrverified_monthly': nrverified_monthly,
        'rverified_annual': rverified_annual,
        'nrverified_annual': nrverified_annual,
        'rverified_custom': rverified_custom,
        'nrverified_custom': nrverified_custom,
        'rexpired_monthly': rexpired_monthly,
        'nrexpired_monthly': nrexpired_monthly,
        'rexpired_annual': rexpired_annual,
        'nrexpired_annual': nrexpired_annual,
        'rexpired_custom': rexpired_custom,
        'nrexpired_custom': nrexpired_custom,
        'cancel_monthly': cancel_monthly,
        'cancel_annual': cancel_annual,
        'cancel_custom': cancel_custom,
        'ncancel_monthly': ncancel_monthly,
        'ncancel_annual': ncancel_annual,
        'ncancel_custom': ncancel_custom,
    }
    return render(request, "membership/membership.html", context)

@login_required(login_url='/signin/')
def monthly_form(request):

    if request.method == "POST":
        User = get_user_model()
        current_user = request.user
        monthly_id = User.objects.get(id=current_user.id)
        user_monthly = monthly_id
        unique_id = get_random_string(8)
        users = User.objects.get(email=current_user.email)
        email = users
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        em_fullname = request.POST.get('em_fullname')
        relationship = request.POST.get('relationship')
        em_contactno = request.POST.get('em_contactno')
        em_email = request.POST.get('em_email')
        file = request.FILES.get('file')
        photo = request.FILES.get('photo')
        price = 550

        monthlyform = Monthly(user_monthly=user_monthly, unique_id=unique_id, full_name=full_name, age=age, address=address, contact_no=contact_no, email=email, weight=weight, height=height, em_fullname=em_fullname, relationship=relationship, em_contactno=em_contactno, em_email=em_email, file=file, photo=photo, price=price)
        monthlyform.save()
        return redirect('home')
    
    return render(request, "membership/monthlyform.html", {})

@login_required(login_url='/signin/')
def annual_form(request):

    if request.method == "POST":
        User = get_user_model()
        current_user = request.user
        annual_id = User.objects.get(id=current_user.id)
        user_annual = annual_id
        users = User.objects.get(email=current_user.email)
        email = users
        unique_id = get_random_string(8)
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        em_fullname = request.POST.get('em_fullname')
        relationship = request.POST.get('relationship')
        em_contactno = request.POST.get('em_contactno')
        em_email = request.POST.get('em_email')
        file = request.FILES.get('file')
        photo = request.FILES.get('photo')
        price = 6000

        annualform = Annual(user_annual=user_annual, unique_id=unique_id, full_name=full_name, age=age, address=address, contact_no=contact_no, email=email, weight=weight, height=height, em_fullname=em_fullname, relationship=relationship, em_contactno=em_contactno, em_email=em_email, file=file, photo=photo, price=price)
        annualform.save()
        return redirect('home')
    
    return render(request, "membership/annualform.html", {})

@login_required(login_url='/signin/')
def custom_form(request):

    if request.method == "POST":
        User = get_user_model()
        current_user = request.user
        custom_id = User.objects.get(id=current_user.id)
        user_custom = custom_id
        users = User.objects.get(email=current_user.email)
        email = users
        unique_id = get_random_string(8)
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        em_fullname = request.POST.get('em_fullname')
        relationship = request.POST.get('relationship')
        em_contactno = request.POST.get('em_contactno')
        em_email = request.POST.get('em_email')
        file = request.FILES.get('file')
        photo = request.FILES.get('photo')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
        end = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
        days_diff = (start - end).days
        price = abs(days_diff * 25)

        customform = Custom(user_custom=user_custom, unique_id=unique_id, full_name=full_name, age=age, address=address, contact_no=contact_no, email=email, weight=weight, height=height, em_fullname=em_fullname, relationship=relationship, em_contactno=em_contactno, em_email=em_email, file=file, photo=photo, start_date=start_date, end_date=end_date, price=price)
        customform.save()
        return redirect('home')
    
    return render(request, "membership/customform.html", {})

def signup_view(request):
    context = {}
    if request.method == "POST":
        email = request.POST['email']
        user_name = request.POST['user_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        context["email"] = email
        context["user_name"] = user_name

        User = get_user_model()
        if User.objects.filter(email=email):
            messages.error(request, "Email already exist! Please try a different email.")
            return render (request, 'membership/signup.html', context)

        if User.objects.filter(user_name=user_name):
            messages.error(request, "Username already exist! Please try a different username.")
            return render (request, 'membership/signup.html', context)

        if not user_name.isalnum():
            messages.error(request, "Username must be Alpha-Numerical!")
            return render (request, 'membership/signup.html', context)
        
        if len(user_name)>16:
            messages.error(request, "Username must be under 16 characters.")
            return render (request, 'membership/signup.html', context)

        if password != confirm_password:
            messages.error(request, "Password do not match!") 
            return render (request, 'membership/signup.html', context)

        if len(password)<8:
            messages.error(request, 
            "Password must contain atleast 8 characters. Password must contain at least 1 number. Password must contain at least 1 uppercase letter. Password must contain at least 1 lowercase letter"
            )
            return render (request, 'membership/signup.html', context)
        
        if sum(c.isdigit() for c in password) < 1:
            messages.error(request, 
            "Password must contain atleast 8 characters. Password must contain at least 1 number. Password must contain at least 1 uppercase letter. Password must contain at least 1 lowercase letter"
            )
            return render (request, 'membership/signup.html', context)
        
        if not any(c.isupper() for c in password):
            messages.error(request, 
            "Password must contain atleast 8 characters. Password must contain at least 1 number. Password must contain at least 1 uppercase letter. Password must contain at least 1 lowercase letter"
            )
            return render (request, 'membership/signup.html', context)
        
        if not any(c.islower() for c in password):
            messages.error(request, 
            "Password must contain atleast 8 characters. Password must contain at least 1 number. Password must contain at least 1 uppercase letter. Password must contain at least 1 lowercase letter"
            )
            return render (request, 'membership/signup.html', context)

        myuser = User.objects.create_user(email, user_name, password)
        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')

    return render(request, "membership/signup.html", {})

def signin_view(request):
    context = {}
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        context["email"] = email
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:               
                    return redirect('adminpage')
            elif user.is_superuser==False:
                    return redirect('home')           
        else:
            messages.error(request, "Incorrect email or password.")
            return render (request, 'membership/signin.html', context)

    return render(request, "membership/signin.html", {})

def signout_view(request):
    
    logout(request)
    return redirect('index')

@login_required(login_url='/signin/')
def all_send_email(request):
    if request.method == 'POST':
        previous = timezone.now() + timedelta(days=3)
        monthly = Monthly.objects.filter(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            )
        annual = Annual.objects.filter(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            )
        custom = Custom.objects.filter(
            is_verified=1,
            end_date=previous,
            renew__exact='',
            )
        
        for data in monthly:
            email_subject = "Your subscription is ending soon!"
            email_body = "Hi {}, your subscription is ending in 3 days on {}. Please renew your subscription to continue using our service.".format(data.full_name, data.end_date)
            send_mail(
                email_subject,
                email_body,
                'settings.EMAIL_HOST_USER',
                [data.email],
                fail_silently=False,
            )
        
        for data in annual:
            email_subject = "Your subscription is ending soon!"
            email_body = "Hi {}, your subscription is ending in 3 days on {}. Please renew your subscription to continue using our service.".format(data.full_name, data.end_date)
            send_mail(
                email_subject,
                email_body,
                'settings.EMAIL_HOST_USER',
                [data.email],
                fail_silently=False,
            )

        for data in custom:
            email_subject = "Your subscription is ending soon!"
            email_body = "Hi {}, your subscription is ending in 3 days on {}. Please renew your subscription to continue using our service.".format(data.full_name, data.end_date)
            send_mail(
                email_subject,
                email_body,
                'settings.EMAIL_HOST_USER',
                [data.email],
                fail_silently=False,
            )
            
        return redirect('membership')
    return render(request, 'membership.html')
    

@login_required(login_url='/signin/')
def monthly_send_email(request, id):
    monthly = Monthly.objects.get(id=id)
    # Get all subscriptions with end_date within 3 days from now
    # if monthly.end_date == timezone.now()+timezone.timedelta(days=3):
    email_subject = "Your subscription is ending soon!"
    email_body = "Hi {}, your subscription is ending in 3 days on {}. Please renew your subscription to continue using our service.".format(monthly.full_name, monthly.end_date)
    send_mail(
        email_subject,
        email_body,
        'settings.EMAIL_HOST_USER',
        [monthly.email],
        fail_silently=False,
    )
    return redirect('membership')

@login_required(login_url='/signin/')
def annual_send_email(request, id):
    annual = Annual.objects.get(id=id)
    email_subject = "Your subscription is ending soon!"
    email_body = "Hi {}, your subscription is ending in 3 days on {}. Please renew your subscription to continue using our service.".format(annual.full_name, annual.end_date)
    send_mail(
        email_subject,
        email_body,
        'settings.EMAIL_HOST_USER',
        [annual.email],
        fail_silently=False,
    )
    return redirect('membership')

@login_required(login_url='/signin/')
def custom_send_email(request, id):
    custom = Custom.objects.get(id=id)
    email_subject = "Your subscription is ending soon!"
    email_body = "Hi {}, your subscription is ending in 3 days on {}. Please renew your subscription to continue using our service.".format(custom.full_name, custom.end_date)
    send_mail(
        email_subject,
        email_body,
        'settings.EMAIL_HOST_USER',
        [custom.email],
        fail_silently=False,
    )
    return redirect('membership')

@login_required(login_url='/signin/')
def monthly_cancel_email(request, id):
    monthly = Monthly.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        message = request.POST['message']
        send_mail(
            title,
            message,
            'settings.EMAIL_HOST_USER',
            [monthly.email],
            fail_silently=False,
        )
        return redirect('membership')
    return render (request, 'membership/monthlycancelemail.html')

@login_required(login_url='/signin/')
def forecasting_view(request):
    # if request.method == 'POST':
    #     csv_file = request.FILES['csv_file']
    #     decoded_file = csv_file.read().decode('utf-8')
    #     csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

    #     # Skip the header row
    #     next(csv_data)

    #     for row in csv_data:
    #         unique_id = row[0]
    #         start_date = row[1]
    #         end_date = row[2]
    #         is_verified = row[3]

    #         # Convert start_date string to datetime object
    #         start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d')

    #         # Convert end_date string to datetime object
    #         end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y').strftime('%Y-%m-%d')

    #         # Create an instance of Monthly model and save it
    #         Monthly.objects.create(unique_id=unique_id, start_date=start_date, end_date=end_date, is_verified=is_verified)

    #     return render(request, 'membership/success.html')

    # Check if there is 2020 data in the database
    if not Monthly.objects.filter(start_date__year=2020).exists():
        return HttpResponse("Need Data for 2020-2023 to FORECAST")
    
    monthly_data = Monthly.objects.all()

    # Create a DataFrame from the Monthly model instances
    df_data = pd.DataFrame(list(monthly_data.values('start_date')))

    # Extract the year and month from the 'start_date' column
    df_data['Year'] = pd.DatetimeIndex(df_data['start_date']).year
    df_data['Month'] = pd.DatetimeIndex(df_data['start_date']).month

    # Group and count the records for each year and month
    monthly_counts = df_data.groupby(['Year', 'Month']).size().reset_index(name='Count')

    # Filter the data for training and test based on the desired years
    train_data = monthly_counts.loc[(monthly_counts['Year'] >= 2020) & (monthly_counts['Year'] <= 2022)]['Count'].values
    test_data = monthly_counts.loc[monthly_counts['Year'] == 2023]['Count'].values
    data_2020 = monthly_counts.loc[monthly_counts['Year'] == 2020]['Count'].values
    data_2021 = monthly_counts.loc[monthly_counts['Year'] == 2021]['Count'].values
    data_2022 = monthly_counts.loc[monthly_counts['Year'] == 2022]['Count'].values

    # Concatenate all years' data for overall count
    all_years_data = monthly_counts['Count'].values

    import warnings
    warnings.filterwarnings("ignore")

    # Use auto_arima to determine the best ARIMA model
    model = auto_arima(train_data, seasonal=False)

    # Fit the ARIMA model using the training data
    model_fit = ARIMA(train_data, order=model.order).fit()

    # Get the forecasted values for the test period
    forecast = model_fit.forecast(steps=12)

    # PLOT 1
    # Determine the length of available data for 2023
    data_2023_length = len(test_data)

    # Create the x-axis values
    months = np.arange(1, 13)

    # Plot the data for 2020-2023
    plt.figure(figsize=(8, 4))
    plt.plot(months, data_2020, label='Data (2020)', marker='o')
    plt.plot(months, data_2021, label='Data (2021)', marker='o')
    plt.plot(months, data_2022, label='Data (2022)', marker='o')
    plt.plot(np.arange(1, data_2023_length + 1), test_data, label='Data (2023)', marker='o')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.title('Monthly Records Count for Years 2020-2023')
    plt.legend()
    plt.xticks(months)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Convert the plot to a base64 encoded string
    graph_file1 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    # Close the plot to release resources
    plt.close()

    # TABLE 1    
    # Define a list of month names
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Prepare the real data for 2020-2023
    count_data1 = []
    for i in range(len(data_2020)):
        if i < len(test_data):
            count_data1.append((month_names[i], data_2020[i], data_2021[i], data_2022[i], test_data[i]))
        else:
            count_data1.append((month_names[i], data_2020[i], data_2021[i], data_2022[i], ''))  # Placeholder for missing test_data

    # PLOT 2
    # Generate the forecast for 2024-2026
    forecast_steps = 48  # Forecasting for 48 months (4 years)
    forecast_2023_2026 = model_fit.forecast(steps=forecast_steps)

    # Create the x-axis values for the forecasted period
    forecast_months = np.arange(1, forecast_steps + 1)

    # Set the x-axis ticks and labels
    years = [2023, 2024, 2025, 2026]
    year_ticks = np.arange(1, len(years) * 12 + 1, 12)

    # Plot the forecast for 2023-2026
    plt.figure(figsize=(8, 4))
    plt.plot(forecast_months[:12], forecast_2023_2026[:12], label='Forecast (2023)', linestyle='--')
    plt.plot(forecast_months[12:24], forecast_2023_2026[12:24], label='Forecast (2024)', linestyle='--')
    plt.plot(forecast_months[24:36], forecast_2023_2026[24:36], label='Forecast (2025)', linestyle='--')
    plt.plot(forecast_months[36:48], forecast_2023_2026[36:48], label='Forecast (2026)', linestyle='--')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title('Forecast for Years 2023-2026')
    plt.legend()
    plt.xticks(year_ticks, years)  # Set the x-axis ticks to represent 1-12 for each year
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Convert the plot to a base64 encoded string
    graph_file2 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    # Close the plot to release resources
    plt.close()

    # TABLE 2
    # Prepare the forecast data for 2023-2026
    count_data2 = []
    months_per_year = 12
    years = [2023, 2024, 2025, 2026]

    for month_index in range(months_per_year):
        month_name = month_names[month_index]
        forecast_counts = []

        for year in years:
            if year == 2023:
                forecast_counts.append(round(forecast_2023_2026[month_index], 2))
            else:
                forecast_counts.append(round(forecast_2023_2026[months_per_year * (year - 2023) + month_index], 2))

        count_data2.append((month_name,) + tuple(forecast_counts))

    # STRONGEST MONTH PER YEAR
    # Find the strongest month for each year
    strongest_data = []
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Find the strongest month for each year from 2023 to 2026
    for i in range(4):
        start_index = i * 12
        end_index = start_index + 12
        year_forecast = forecast_2023_2026[start_index:end_index]
        strongest_index = np.argmax(year_forecast)
        month_index = (start_index + strongest_index) % 12  # Adjust index and wrap around using modulo
        strongest_month = month_names[month_index]
        strongest_count = round(year_forecast[strongest_index], 2)
        strongest_data.append((years[i], strongest_month, strongest_count))


    # PLOT 3
    # Combine the data for 2020-2022 into a single line
    combined_data_2020_2022 = np.concatenate((data_2020, data_2021, data_2022))

    # Create the x-axis values for the combined data
    combined_months = np.arange(1, len(combined_data_2020_2022) + forecast_steps + 1)

    # Set the x-axis ticks and labels
    years = [2020, 2021, 2022] + [2023, 2024, 2025, 2026]
    year_ticks = np.arange(1, len(years) * 12 + 1, 12)
    plt.figure(figsize=(8, 4))
    plt.xticks(year_ticks, years)

    # Plot the combined data for 2020-2022 as a single line
    plt.plot(combined_months[:len(combined_data_2020_2022)], combined_data_2020_2022, label='Data (2020-2022)', linestyle='-')

    # Generate the forecast for 2023-2026
    forecast_steps = 48  # Forecasting for 48 months (4 years)
    forecast_2023_2026 = model_fit.forecast(steps=forecast_steps)

    # Create the x-axis values for the forecasted period
    forecast_months = np.arange(len(combined_data_2020_2022) + 1, len(combined_data_2020_2022) + forecast_steps + 1)

    # Plot the forecast for 2023-2026
    plt.plot(forecast_months[:48], forecast_2023_2026[:48], label='Forecast (2023-2026)', linestyle='--')

    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title('Yearly Records Count for Years 2020-2026')
    plt.legend()
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Convert the plot to a base64 encoded string
    graph_file3 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    # Close the plot to release resources
    plt.close()

    # Pass the file path to the template for rendering
    context = {
        'graph_file1': graph_file1,
        'count_data1': count_data1,
        'month_names': month_names,
        'graph_file2': graph_file2,
        'count_data2': count_data2,
        'years': years,
        'strongest_data': strongest_data,
        'graph_file3': graph_file3
        }

    return render(request, 'membership/forecasting.html', context)

@login_required(login_url='/signin/')
def success_view(request):
    
    return render(request, "membership/success.html", {})

@login_required(login_url='/signin/')
def membershipapplication_view(request):
    # Not Verified
    monthly = Monthly.objects.filter(
        is_verified=0,
        is_cancel=0
        )
    annual = Annual.objects.filter(
        is_verified=0,
        is_cancel=0
        )
    custom = Custom.objects.filter(
        is_verified=0,
        is_cancel=0
        )
    
    # Not Verified Length
    nnotverified_monthly = len(Monthly.objects.filter(
        is_verified=0,
        is_cancel=0
        ))
    nnotverified_annual = len(Annual.objects.filter(
        is_verified=0,
        is_cancel=0
        ))
    nnotverified_custom = len(Custom.objects.filter(
        is_verified=0,
        is_cancel=0
        ))
    
    numberof_user = len(User.objects.all())

    # Right Side Bar
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'monthly': monthly,
        'annual': annual,
        'custom': custom,
        'nnotverified_monthly': nnotverified_monthly,
        'nnotverified_annual': nnotverified_annual,
        'nnotverified_custom': nnotverified_custom,
        'numberof_user': numberof_user,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'customnew_application': customnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'nvcustomnew_application': nvcustomnew_application,
    }
    return render(request, "membership/membershipapplication.html", context)

@login_required(login_url='/signin/')
def cancelapplication_view(request):
    # Cancel Membership
    cancel_monthly = Monthly.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact='')
    cancel_annual = Annual.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact='')
    cancel_custom = Custom.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact='')
    
    # Cancel Membership Length
    ncancel_monthly = len(Monthly.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact=''))
    ncancel_annual = len(Annual.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact=''))
    ncancel_custom = len(Custom.objects.filter(
        is_verified=0,
        is_cancel=1,
        ss_email__isnull=False,
        payment__isnull=False,
        ).exclude(ss_email__exact='', payment__exact=''))
    
    numberof_user = len(User.objects.all())

    # Right Side Bar
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'cancel_monthly': cancel_monthly,
        'cancel_annual': cancel_annual,
        'cancel_custom': cancel_custom,
        'ncancel_monthly': ncancel_monthly,
        'ncancel_annual': ncancel_annual,
        'ncancel_custom': ncancel_custom,
        'numberof_user': numberof_user,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'customnew_application': customnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'nvcustomnew_application': nvcustomnew_application,
    }
    return render(request, "membership/cancelmembershipapplication.html", context)

@login_required(login_url='/signin/')
def threedaysremaining_view(request):
    # Membership 3 days
    previous = timezone.now() + timedelta(days=3)
    severified_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        )
    severified_annual = Annual.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        )
    severified_custom = Custom.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        )

    # Membership 3 days Length
    previous = timezone.now() + timedelta(days=3)
    nseverified_monthly = len(Monthly.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        ))
    nseverified_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        ))
    nseverified_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date=previous,
        renew__exact='',
        ))
    
    numberof_user = len(User.objects.all())

    # Right Side Bar
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'severified_monthly': severified_monthly,
        'severified_annual': severified_annual,
        'severified_custom': severified_custom,
        'nseverified_monthly': nseverified_monthly,
        'nseverified_annual': nseverified_annual,
        'nseverified_custom': nseverified_custom,
        'numberof_user': numberof_user,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'customnew_application': customnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'nvcustomnew_application': nvcustomnew_application,
    }
    return render(request, "membership/threedaysremaining.html", context)

@login_required(login_url='/signin/')
def renewactivemembership_view(request):
    # Renew Active Membership
    rverified_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    rverified_annual = Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    rverified_custom = Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    
    # Renew Active Membership Length
    nrverified_monthly = len(Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    nrverified_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    nrverified_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    
    numberof_user = len(User.objects.all())

    # Right Side Bar
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'rverified_monthly': rverified_monthly,
        'nrverified_monthly': nrverified_monthly,
        'rverified_annual': rverified_annual,
        'nrverified_annual': nrverified_annual,
        'rverified_custom': rverified_custom,
        'nrverified_custom': nrverified_custom,
        'numberof_user': numberof_user,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'customnew_application': customnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'nvcustomnew_application': nvcustomnew_application,
    }
    return render(request, "membership/renewactivemembership.html", context)

@login_required(login_url='/signin/')
def renewexpiredmembership_view(request):
    # Renew Expired Membership
    rexpired_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    rexpired_annual = Annual.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()
    rexpired_custom = Custom.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact='').order_by('-end_date').reverse()

    # Renew Expired Membership Length
    nrexpired_monthly = len(Monthly.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    nrexpired_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    nrexpired_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now(),
        renew__isnull=False,
        ).exclude(renew__exact=''))
    
    numberof_user = len(User.objects.all())

    # Right Side Bar
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'rexpired_monthly': rexpired_monthly,
        'nrexpired_monthly': nrexpired_monthly,
        'rexpired_annual': rexpired_annual,
        'nrexpired_annual': nrexpired_annual,
        'rexpired_custom': rexpired_custom,
        'nrexpired_custom': nrexpired_custom,
        'numberof_user': numberof_user,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'customnew_application': customnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'nvcustomnew_application': nvcustomnew_application,
    }
    return render(request, "membership/renewexpiredmembership.html", context)

@login_required(login_url='/signin/')
def activemembership_view(request):
    # Active Membership
    verified_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ).order_by('-end_date').reverse()
    verified_annual = Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ).order_by('-end_date').reverse()
    verified_custom = Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ).order_by('-end_date').reverse()
    
    # Active Membership Lenth
    nverified_monthly = len( Monthly.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ))
    nverified_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ))
    nverified_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date__gt=timezone.now()
        ))
    
    numberof_user = len(User.objects.all())

    # Right Side Bar
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'verified_monthly': verified_monthly,
        'verified_annual': verified_annual,
        'verified_custom': verified_custom,
        'nverified_monthly': nverified_monthly,
        'nverified_annual': nverified_annual,
        'nverified_custom': nverified_custom,
        'numberof_user': numberof_user,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'customnew_application': customnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'nvcustomnew_application': nvcustomnew_application,
    }
    return render(request, "membership/activemembership.html", context)

@login_required(login_url='/signin/')
def expiredmembership_view(request):
    # Expired Membership
    expired_monthly = Monthly.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        )
    expired_annual = Annual.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        )
    expired_custom = Custom.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        )
    
    # Expired Membership Length
    nexpired_monthly = len( Monthly.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        ))
    nexpired_annual = len(Annual.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        ))
    nexpired_custom = len(Custom.objects.filter(
        is_verified=1,
        end_date__lte=timezone.now()
        ))
    
    numberof_user = len(User.objects.all())

    # Right Side Bar
    monthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvmonthlynew_application = Monthly.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    annualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvannualnew_application = Annual.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]
    customnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=1,
        end_date__gt=timezone.now()
    ).order_by('id').reverse()[:2:1]
    nvcustomnew_application = Custom.objects.filter(
        id__gt=0,
        is_verified=0
    ).order_by('id').reverse()[:2:1]

    context = {
        'expired_monthly': expired_monthly,
        'expired_annual': expired_annual,
        'expired_custom': expired_custom,
        'nexpired_monthly': nexpired_monthly,
        'nexpired_annual': nexpired_annual,
        'nexpired_custom': nexpired_custom,
        'numberof_user': numberof_user,
        'monthlynew_application': monthlynew_application,
        'annualnew_application': annualnew_application,
        'customnew_application': customnew_application,
        'nvmonthlynew_application': nvmonthlynew_application,
        'nvannualnew_application': nvannualnew_application,
        'nvcustomnew_application': nvcustomnew_application,
    }
    return render(request, "membership/expiredmembership.html", context)


# MEAL

# @login_required(login_url='/signin/')
# def mealplan_view(request):
    
#     return render(request, "membership/mealplan.html")

def search_recipes(ingredient, num_results):
    base_url = 'https://api.edamam.com'
    app_id = 'fb5e84fe'
    app_key = '5babf971976ca7df485b0a89a1bbb5ec'

    endpoint = f'{base_url}/search'

    params = {
        'app_id': app_id,
        'app_key': app_key,
        'q': ingredient,
        'from': 0,
        'to': num_results,
        'diet': 'balanced',
        # 'singleRecipe': True,  # Add this parameter
        # 'singleRecipe.arg2': 'arg2',
        # 'singleRecipe.arg3': 'arg3',
        # 'singleRecipe.arg4': 'arg4'
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        # print(data)  # Add this line to inspect the API response
        return data
    else:
        print(response.text)  # Add this line to print the error message
        return None

def calculate_target_calories(height, weight, age, weight_plan, activity_level):
    BMR = 0

    # Calculate Basal Metabolic Rate (BMR) based on user's weight
    if weight_plan == 'Gain weight':
        BMR = 10 * weight + 6.25 * height - 5 * age + 500
    elif weight_plan == 'Maintain weight':
        BMR = 10 * weight + 6.25 * height - 5 * age
    elif weight_plan == 'Lose weight':
        BMR = 10 * weight + 6.25 * height - 5 * age - 500

    # Adjust BMR based on activity level
    if activity_level == 'Inactive':
        activity_multiplier = 1.2
    elif activity_level == 'Lightly Active':
        activity_multiplier = 1.375
    elif activity_level == 'Active':
        activity_multiplier = 1.55
    elif activity_level == 'Very Active':
        activity_multiplier = 1.725

    target_calories = BMR * activity_multiplier

    return target_calories

def filter_recipes_by_calories(recipe_results, target_calories):
    filtered_recipes = []

    for hit in recipe_results['hits']:
        recipe = hit['recipe']
        calories_per_serving = int(round(recipe['calories'] / recipe['yield']))
        protein_per_serving = int(round(recipe['totalNutrients']['PROCNT']['quantity'] / recipe['yield']))
        carbs_per_serving = int(round(recipe['totalNutrients']['CHOCDF']['quantity'] / recipe['yield']))
        fat_per_serving = int(round(recipe['totalNutrients']['FAT']['quantity'] / recipe['yield']))
        servings = round(target_calories / calories_per_serving, 2)
        meal_info = {
            'name': recipe['label'],
            'calories': calories_per_serving,
            'protein': protein_per_serving,
            'carbs': carbs_per_serving,
            'fat': fat_per_serving,
            'servings': servings,
            'image_path': recipe['image'],  # Add the image path
            'ingredients': recipe['ingredientLines'],  # Add the ingredient lines
            'instructions_link': recipe['url']  # Add the recipe URL as instructions link
        }
        filtered_recipes.append(meal_info)

    return filtered_recipes

def mealplan_form(request):
    if request.method == 'POST':
        height = float(request.POST['height'])
        weight = float(request.POST['weight'])
        age = int(request.POST['age'])
        weight_plan = request.POST['weight_plan']
        activity_level = request.POST['activity_level']
        num_days = int(request.POST['num_days'])

        target_calories = calculate_target_calories(height, weight, age, weight_plan, activity_level)

        # List of ingredients for different days
        
        main_ingredients = ['chicken', 'beef', 'fish', 'tofu', 'beans', 'quinoa', 'eggs', 'pork', 'lamb', 'shrimp']

        meals = []
        for i in range(num_days):
            random.shuffle(main_ingredients)  # Shuffle the ingredient list for each day

            # Select ingredients for each meal separately
            breakfast_ingredient = main_ingredients[0]
            lunch_ingredient = main_ingredients[1]
            dinner_ingredient = main_ingredients[2]

            breakfast_recipe_results = search_recipes(breakfast_ingredient, 10)
            lunch_recipe_results = search_recipes(lunch_ingredient, 10)
            dinner_recipe_results = search_recipes(dinner_ingredient, 10)

            if (
                breakfast_recipe_results
                and lunch_recipe_results
                and dinner_recipe_results
            ):
                breakfast_filtered_recipes = filter_recipes_by_calories(
                    breakfast_recipe_results,
                    target_calories
                )
                lunch_filtered_recipes = filter_recipes_by_calories(
                    lunch_recipe_results,
                    target_calories
                )
                dinner_filtered_recipes = filter_recipes_by_calories(
                    dinner_recipe_results,
                    target_calories
                )

                breakfast_recipe = random.choice(breakfast_filtered_recipes)  # Select a random breakfast recipe
                lunch_recipe = random.choice(lunch_filtered_recipes)  # Select a random lunch recipe
                dinner_recipe = random.choice(dinner_filtered_recipes)  # Select a random dinner recipe

                # Adjust servings, calculate calories, and other details
                total_calories = (
                    breakfast_recipe['calories'] * breakfast_recipe['servings'] +
                    lunch_recipe['calories'] * lunch_recipe['servings'] +
                    dinner_recipe['calories'] * dinner_recipe['servings']
                )

                adjustment_factor = target_calories / total_calories

                breakfast_recipe['servings'] = round(breakfast_recipe['servings'] * adjustment_factor, 2)
                lunch_recipe['servings'] = round(lunch_recipe['servings'] * adjustment_factor, 2)
                dinner_recipe['servings'] = round(dinner_recipe['servings'] * adjustment_factor, 2)

                breakfast_recipe['calories'] = int(round(breakfast_recipe['calories'] * breakfast_recipe['servings']))
                breakfast_recipe['protein'] = int(round(breakfast_recipe['protein'] * breakfast_recipe['servings']))
                breakfast_recipe['carbs'] = int(round(breakfast_recipe['carbs'] * breakfast_recipe['servings']))
                breakfast_recipe['fat'] = int(round(breakfast_recipe['fat'] * breakfast_recipe['servings']))

                lunch_recipe['calories'] = int(round(lunch_recipe['calories'] * lunch_recipe['servings']))
                lunch_recipe['protein'] = int(round(lunch_recipe['protein'] * lunch_recipe['servings']))
                lunch_recipe['carbs'] = int(round(lunch_recipe['carbs'] * lunch_recipe['servings']))
                lunch_recipe['fat'] = int(round(lunch_recipe['fat'] * lunch_recipe['servings']))

                dinner_recipe['calories'] = int(round(dinner_recipe['calories'] * dinner_recipe['servings']))
                dinner_recipe['protein'] = int(round(dinner_recipe['protein'] * dinner_recipe['servings']))
                dinner_recipe['carbs'] = int(round(dinner_recipe['carbs'] * dinner_recipe['servings']))
                dinner_recipe['fat'] = int(round(dinner_recipe['fat'] * dinner_recipe['servings']))

                day_meals = {
                    'day': i + 1,
                    'breakfast': breakfast_recipe,
                    'total_calories': total_calories,
                    'lunch': lunch_recipe,
                    'dinner': dinner_recipe
                }
                meals.append(day_meals)
            else:
                return render(request, 'membership/nomeal_plan.html')

        context = {
            'meals': meals,
            'target_calories': target_calories,
        }

        # Store the meals data in the session
        request.session['meals'] = meals

        return render(request, 'membership/mealplanform.html', context)
    
    else:
        # Get the current height, weight, and age of the user
        user = request.user

        if user.is_authenticated:
            height = None
            weight = None
            age = None

            if user.monthly_user.exists():
                subscription = user.monthly_user.first()
                height = subscription.height
                weight = subscription.weight
                age = subscription.age
            elif user.annual_user.exists():
                subscription = user.annual_user.first()
                height = subscription.height
                weight = subscription.weight
                age = subscription.age
            elif user.custom_user.exists():
                subscription = user.custom_user.first()
                height = subscription.height
                weight = subscription.weight
                age = subscription.age

            context = {
                'height': height,
                'weight': weight,
                'age': age,
            }
            return render(request, 'membership/mealplanform.html', context)

    return render(request, 'membership/mealplanform.html')

def generate_pdf(request):
    # Extract the meal plan data from the session
    target_calories = float(request.GET.get('target_calories'))
    meals = request.session.get('meals')

    if not meals:
        return HttpResponse("No meal plan found.")

    # Remove the meals data from the session
    del request.session['meals']

    # Create a new PDF document
    pdf_buffer = BytesIO()
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=(8.5*inch, 14*inch))  # Adjust the page size

    # Set up fonts
    title_font = "Helvetica-Bold"
    meal_font = "Helvetica"
    info_font = "Helvetica-Oblique"

    # Define the vertical position (y-coordinate) for drawing elements
    y = 13*inch  # Adjust the starting y-coordinate

    for meal in meals:
        total_calories = meal['breakfast']['calories'] + meal['lunch']['calories'] + meal['dinner']['calories']
        breakfast_servings = max(int(round(meal['breakfast']['servings'])), 1)
        lunch_servings = max(int(round(meal['lunch']['servings'])), 1)
        dinner_servings = max(int(round(meal['dinner']['servings'])), 1)

        # Draw the title and target calories on each page
        pdf_canvas.setFont(title_font, 20)
        pdf_canvas.drawString(0.5*inch, y, "Meal Plan")  # Adjust the x-position
        y -= 0.3*inch  # Adjust the vertical spacing
        pdf_canvas.setFont(info_font, 12)
        pdf_canvas.drawString(0.5*inch, y, f"Targeted Calories: {target_calories:.0f}")  # Adjust the x-position
        y -= 0.5*inch  # Adjust the vertical spacing

        # Draw the day and total calories
        pdf_canvas.setFont(meal_font, 16)
        pdf_canvas.drawString(0.5*inch, y, f"Day {meal['day']}")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.setFont(info_font, 12)
        pdf_canvas.drawString(0.5*inch, y, f"Total Calories of 3 Meals: {total_calories}")  # Adjust the x-position
        y -= 0.4*inch  # Adjust the vertical spacing

        # Draw the breakfast
        pdf_canvas.setFont(meal_font, 16)
        pdf_canvas.drawString(0.5*inch, y, "Breakfast")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.setFont(info_font, 12)
        pdf_canvas.drawString(0.5*inch, y, f"Name: {meal['breakfast']['name']}")  # Adjust the x-position
        y -= 0.3*inch  # Adjust the vertical spacing

        # Draw the meal image for breakfast
        meal_image_path = meal['breakfast']['image_path']
        if meal_image_path:
            meal_image = ImageReader(meal_image_path)
            pdf_canvas.drawImage(meal_image, 0.5*inch, y - 1.2*inch, width=100, height=100)  # Adjust the x-position
        else:
            pdf_canvas.drawString(0.5*inch, y, "Image Not Available")  # Adjust the x-position

        y -= 1.4*inch  # Adjust the vertical spacing

        pdf_canvas.drawString(0.5*inch, y, f"Servings: {breakfast_servings}")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Calories: {meal['breakfast']['calories']} kcal")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Protein: {meal['breakfast']['protein']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Fat: {meal['breakfast']['fat']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Carbs: {meal['breakfast']['carbs']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing

        # Draw the instruction link for breakfast
        pdf_canvas.setFont(info_font, 12)
        pdf_canvas.drawString(0.5*inch, y, "Instructions: ")  # Adjust the x-position
        pdf_canvas.setFillColorRGB(0,0,255)  # Set the link color
        instruction_link_x = pdf_canvas.stringWidth("Instructions: ", info_font, 12) + 0.5*inch + 2  # Adjust the x-position
        instruction_link_y = y  # Save the y-coordinate for the link
        instruction_link = meal['breakfast']['instructions_link']
        pdf_canvas.linkURL(instruction_link, (instruction_link_x, instruction_link_y), width=200, height=12, thickness=0)
        pdf_canvas.drawString(instruction_link_x, instruction_link_y, instruction_link)
        pdf_canvas.setFillColorRGB(0,0,0)  # Set the link color

        y -= 0.6*inch  # Adjust the vertical spacing

        # Draw the lunch
        pdf_canvas.setFont(meal_font, 16)
        pdf_canvas.drawString(0.5*inch, y, "Lunch")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.setFont(info_font, 12)
        pdf_canvas.drawString(0.5*inch, y, f"Name: {meal['lunch']['name']}")  # Adjust the x-position
        y -= 0.3*inch  # Adjust the vertical spacing

        # Draw the meal image for lunch
        meal_image_path = meal['lunch']['image_path']
        if meal_image_path:
            meal_image = ImageReader(meal_image_path)
            pdf_canvas.drawImage(meal_image, 0.5*inch, y - 1.2*inch, width=100, height=100)  # Adjust the x-position
        else:
            pdf_canvas.drawString(0.5*inch, y, "Image Not Available")  # Adjust the x-position

        y -= 1.4*inch  # Adjust the vertical spacing

        pdf_canvas.drawString(0.5*inch, y, f"Servings: {lunch_servings}")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Calories: {meal['lunch']['calories']} kcal")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Protein: {meal['lunch']['protein']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Fat: {meal['lunch']['fat']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Carbs: {meal['lunch']['carbs']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing

        # Draw the instruction link for lunch
        pdf_canvas.setFont(info_font, 12)
        pdf_canvas.drawString(0.5*inch, y, "Instructions: ")  # Adjust the x-position
        pdf_canvas.setFillColorRGB(0,0,255)  # Set the link color
        instruction_link_x = pdf_canvas.stringWidth("Instructions: ", info_font, 12) + 0.5*inch + 2  # Adjust the x-position
        instruction_link_y = y  # Save the y-coordinate for the link
        instruction_link = meal['lunch']['instructions_link']
        pdf_canvas.linkURL(instruction_link, (instruction_link_x, instruction_link_y), width=200, height=12, thickness=0)
        pdf_canvas.drawString(instruction_link_x, instruction_link_y, instruction_link)
        pdf_canvas.setFillColorRGB(0,0,0)  # Set the link color

        y -= 0.6*inch  # Adjust the vertical spacing

        # Draw the dinner
        pdf_canvas.setFont(meal_font, 16)
        pdf_canvas.drawString(0.5*inch, y, "Dinner")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.setFont(info_font, 12)
        pdf_canvas.drawString(0.5*inch, y, f"Name: {meal['dinner']['name']}")  # Adjust the x-position
        y -= 0.3*inch  # Adjust the vertical spacing

        # Draw the meal image for dinner
        meal_image_path = meal['dinner']['image_path']
        if meal_image_path:
            meal_image = ImageReader(meal_image_path)
            pdf_canvas.drawImage(meal_image, 0.5*inch, y - 1.2*inch, width=100, height=100)  # Adjust the x-position
        else:
            pdf_canvas.drawString(0.5*inch, y, "Image Not Available")  # Adjust the x-position

        y -= 1.4*inch  # Adjust the vertical spacing

        pdf_canvas.drawString(0.5*inch, y, f"Servings: {dinner_servings}")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Calories: {meal['dinner']['calories']} kcal")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Protein: {meal['dinner']['protein']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Fat: {meal['dinner']['fat']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing
        pdf_canvas.drawString(0.5*inch, y, f"Carbs: {meal['dinner']['carbs']} g")  # Adjust the x-position
        y -= 0.2*inch  # Adjust the vertical spacing

        # Draw the instruction link for dinner
        pdf_canvas.setFont(info_font, 12)
        pdf_canvas.drawString(0.5*inch, y, "Instructions: ")  # Adjust the x-position
        pdf_canvas.setFillColorRGB(0,0,255)  # Set the link color
        instruction_link_x = pdf_canvas.stringWidth("Instructions: ", info_font, 12) + 0.5*inch + 2  # Adjust the x-position
        instruction_link_y = y  # Save the y-coordinate for the link
        instruction_link = meal['dinner']['instructions_link']
        pdf_canvas.linkURL(instruction_link, (instruction_link_x, instruction_link_y), width=200, height=12, thickness=0)
        pdf_canvas.drawString(instruction_link_x, instruction_link_y, instruction_link)
        pdf_canvas.setFillColorRGB(0,0,0)  # Set the link color

        y -= 0.4*inch  # Adjust the vertical spacing

        y = 13*inch  # Reset the vertical position for the next page

        # Start a new page for each day
        pdf_canvas.showPage()

    pdf_canvas.save()

    # Get the PDF content from the buffer
    pdf_buffer.seek(0)
    response = FileResponse(pdf_buffer, as_attachment=True, filename='meal_plan.pdf')
    return response
