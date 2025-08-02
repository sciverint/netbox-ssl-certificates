# netbox_ssl_certificates/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from netbox.views import generic
from .models import SSLCertificate
from .forms import SSLCertificateForm, SSLCertificateFilterForm
from datetime import datetime, timedelta

class SSLCertificateListView(generic.ObjectListView):
    queryset = SSLCertificate.objects.all()
    template_name = 'netbox_ssl_certificates/sslcertificate_list.html'
    filterset_form = SSLCertificateFilterForm
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply search filter
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(common_name__icontains=q) |
                Q(subject_alternative_names__icontains=q) |
                Q(issuer__icontains=q)
            )
        
        # Apply certificate type filter
        cert_type = self.request.GET.get('certificate_type')
        if cert_type:
            queryset = queryset.filter(certificate_type=cert_type)
        
        # Apply status filter
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Apply issuer filter
        issuer = self.request.GET.get('issuer')
        if issuer:
            queryset = queryset.filter(issuer__icontains=issuer)
        
        # Apply expiring within filter
        expiring_within = self.request.GET.get('expiring_within')
        if expiring_within:
            days = int(expiring_within)
            cutoff_date = datetime.now().date() + timedelta(days=days)
            queryset = queryset.filter(expiry_date__lte=cutoff_date, expiry_date__gte=datetime.now().date())
        
        return queryset

class SSLCertificateView(generic.ObjectView):
    queryset = SSLCertificate.objects.all()
    template_name = 'netbox_ssl_certificates/sslcertificate.html'

class SSLCertificateEditView(generic.ObjectEditView):
    queryset = SSLCertificate.objects.all()
    form = SSLCertificateForm
    template_name = 'netbox_ssl_certificates/sslcertificate_edit.html'

class SSLCertificateDeleteView(generic.ObjectDeleteView):
    queryset = SSLCertificate.objects.all()
    template_name = 'netbox_ssl_certificates/sslcertificate_delete.html'

