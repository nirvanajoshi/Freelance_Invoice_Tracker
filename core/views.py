from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from .models import Client, Project, TimeEntry, Invoice, Payment
from .forms import ClientForm, ProjectForm, TimeEntryForm, InvoiceForm, PaymentForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('client_list')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('client_list')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- Client ----------

@login_required
def client_list(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, 'core/client_list.html', {'clients': clients})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'core/client_form.html', {'form': form})

@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'core/client_form.html', {'form': form})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, user=request.user)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'core/client_confirm_delete.html', {'client': client})


# ---------- Project ----------

@login_required
def project_list(request):
    projects = Project.objects.filter(client__user=request.user)
    return render(request, 'core/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.fields['client'].queryset = Client.objects.filter(user=request.user)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
        form.fields['client'].queryset = Client.objects.filter(user=request.user)
    return render(request, 'core/project_form.html', {'form': form})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk, client__user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        form.fields['client'].queryset = Client.objects.filter(user=request.user)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
        form.fields['client'].queryset = Client.objects.filter(user=request.user)
    return render(request, 'core/project_form.html', {'form': form})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, client__user=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'core/project_confirm_delete.html', {'project': project})


# ---------- TimeEntry ----------

@login_required
def timeentry_list(request):
    entries = TimeEntry.objects.filter(project__client__user=request.user)
    return render(request, 'core/timeentry_list.html', {'entries': entries})

@login_required
def timeentry_create(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        form.fields['project'].queryset = Project.objects.filter(client__user=request.user)
        if form.is_valid():
            form.save()
            return redirect('timeentry_list')
    else:
        form = TimeEntryForm()
        form.fields['project'].queryset = Project.objects.filter(client__user=request.user)
    return render(request, 'core/timeentry_form.html', {'form': form})

@login_required
def timeentry_update(request, pk):
    entry = get_object_or_404(TimeEntry, pk=pk, project__client__user=request.user)
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, instance=entry)
        form.fields['project'].queryset = Project.objects.filter(client__user=request.user)
        if form.is_valid():
            form.save()
            return redirect('timeentry_list')
    else:
        form = TimeEntryForm(instance=entry)
        form.fields['project'].queryset = Project.objects.filter(client__user=request.user)
    return render(request, 'core/timeentry_form.html', {'form': form})

@login_required
def timeentry_delete(request, pk):
    entry = get_object_or_404(TimeEntry, pk=pk, project__client__user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('timeentry_list')
    return render(request, 'core/timeentry_confirm_delete.html', {'entry': entry})


# ---------- Invoice ----------

@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(client__user=request.user)
    return render(request, 'core/invoice_list.html', {'invoices': invoices})

@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        form.fields['client'].queryset = Client.objects.filter(user=request.user)
        form.fields['time_entries'].queryset = TimeEntry.objects.filter(
            project__client__user=request.user, invoiced=False
        )
        if form.is_valid():
            invoice = form.save()  # M2M needs the object saved first before attaching entries

            total = 0
            for entry in invoice.time_entries.all():
                total += entry.hours * entry.project.hourly_rate
                entry.invoiced = True
                entry.save()

            invoice.total_amount = total
            invoice.save()

            return redirect('invoice_list')
    else:
        form = InvoiceForm()
        form.fields['client'].queryset = Client.objects.filter(user=request.user)
        form.fields['time_entries'].queryset = TimeEntry.objects.filter(
            project__client__user=request.user, invoiced=False
        )
    return render(request, 'core/invoice_form.html', {'form': form})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, client__user=request.user)
    return render(request, 'core/invoice_detail.html', {'invoice': invoice})

@login_required
def invoice_send(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, client__user=request.user)
    if request.method == 'POST':
        invoice.status = 'sent'
        invoice.save()
        return redirect('invoice_list')
    return render(request, 'core/invoice_confirm_send.html', {'invoice': invoice})

@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, client__user=request.user)
    if request.method == 'POST':
        # freeing up the time entries so they can be invoiced again
        invoice.time_entries.update(invoiced=False)
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'core/invoice_confirm_delete.html', {'invoice': invoice})


# ---------- Payment ----------

@login_required
def payment_create(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, client__user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()

            total_paid = sum(p.amount for p in invoice.payments.all()) if hasattr(invoice, 'payments') else sum(
                p.amount for p in Payment.objects.filter(invoice=invoice)
            )
            if total_paid >= invoice.total_amount:
                invoice.status = 'paid'
                invoice.save()

            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = PaymentForm()
    return render(request, 'core/payment_form.html', {'form': form, 'invoice': invoice})