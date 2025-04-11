from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
'''
    form for customer registration
'''

class Customer_registration_form(forms.ModelForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    retype_password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    
    class Meta:
        model = customer  # Your custom customer model
        exclude = ['account']  # Exclude the 'account' field from the form (as per your model)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email_address')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean_retype_password(self):
        password = self.cleaned_data.get('password')
        retype_password = self.cleaned_data.get('retype_password')

        if password != retype_password:
            raise forms.ValidationError("Passwords do not match.")
        return retype_password

    def save(self, commit=True):
        # Create the user instance first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email_address']
        ) 
        
        # let the newly account to have the customer permission
        customer_group = Group.objects.get(name="Customer")
        user.groups.add(customer_group)

        # Create the associated customer instance
        customer = super().save(commit=False)
        customer.account = user  # Link the user account to the customer model
        if commit:
            customer.save()
            
        return customer
