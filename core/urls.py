from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/update/', views.client_update, name='client_update'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),

    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/update/', views.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    path('time-entries/', views.timeentry_list, name='timeentry_list'),
    path('time-entries/create/', views.timeentry_create, name='timeentry_create'),
    path('time-entries/<int:pk>/update/', views.timeentry_update, name='timeentry_update'),
    path('time-entries/<int:pk>/delete/', views.timeentry_delete, name='timeentry_delete'),

    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:pk>/send/', views.invoice_send, name='invoice_send'),
    path('invoices/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),

    path('invoices/<int:invoice_id>/payments/create/', views.payment_create, name='payment_create'),
]