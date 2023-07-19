from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.forms import CharField, PasswordInput
# from .models import Monthly, User
# from django.contrib.auth.password_validation import validate_password
# from django.core import validators

# class MonthlyForm(forms.ModelForm):
#     class Meta:
#         model = Monthly
#         fields = ['full_name', 'age', 'address', 'contact_no', 'email', 'weight', 'height', 'em_fullname', 'relationship', 'em_contactno', 'em_email', 'file']  

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields['email'] = User.email
#         self.fields['email'].disabled = True
#         # Or to set READONLY
#         # self.fields['email'].widget.attrs["readonly"] = True
