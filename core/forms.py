
from django import forms
from .models import Client, Project, TimeEntry, Invoice, Payment


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'company']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'name', 'description', 'hourly_rate', 'status']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['project', 'date', 'hours', 'description']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'time_entries', 'due_date']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'time_entries': forms.CheckboxSelectMultiple(),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'date', 'method']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'method': forms.TextInput(attrs={'class': 'form-control'}),
        }