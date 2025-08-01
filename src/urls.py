# netbox_ssl_certificates/urls.py
from django.urls import path
from . import views

app_name = 'netbox_ssl_certificates'

urlpatterns = [
    path('', views.SSLCertificateListView.as_view(), name='sslcertificate_list'),
    path('add/', views.SSLCertificateEditView.as_view(), name='sslcertificate_add'),
    path('<int:pk>/', views.SSLCertificateView.as_view(), name='sslcertificate'),
    path('<int:pk>/edit/', views.SSLCertificateEditView.as_view(), name='sslcertificate_edit'),
    path('<int:pk>/delete/', views.SSLCertificateDeleteView.as_view(), name='sslcertificate_delete'),
]

