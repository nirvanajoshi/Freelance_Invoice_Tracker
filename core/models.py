from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.client.name})"


class TimeEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    invoiced = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project.name} - {self.date} - {self.hours}h"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    time_entries = models.ManyToManyField(TimeEntry)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Invoice #{self.pk} - {self.client.name} - {self.status}"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    method = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.invoice} - {self.amount}"