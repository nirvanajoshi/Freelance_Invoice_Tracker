from django.contrib import admin
from .models import Client, Project, TimeEntry, Invoice, Payment

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(TimeEntry)
admin.site.register(Invoice)
admin.site.register(Payment)
