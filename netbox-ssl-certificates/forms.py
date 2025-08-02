# netbox_ssl_certificates/forms.py
from django import forms
from netbox.forms import NetBoxModelForm
from .models import SSLCertificate, CertificateTypeChoices, CertificateStatusChoices

class SSLCertificateForm(NetBoxModelForm):
    class Meta:
        model = SSLCertificate
        fields = [
            'name', 'common_name', 'subject_alternative_names', 'certificate_type',
            'issuer', 'serial_number', 'issued_date', 'expiry_date', 'key_size',
            'signature_algorithm', 'status', 'auto_renewal', 'certificate_pem', 'notes'
        ]
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'subject_alternative_names': forms.Textarea(attrs={'rows': 3}),
            'certificate_pem': forms.Textarea(attrs={'rows': 8}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class SSLCertificateFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search certificates...'})
    )
    
    certificate_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + CertificateTypeChoices.CHOICES,
        label='Certificate Type'
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + CertificateStatusChoices.CHOICES,
        label='Status'
    )
    
    issuer = forms.CharField(
        required=False,
        label='Issuer',
        widget=forms.TextInput(attrs={'placeholder': 'Certificate Authority...'})
    )
    
    expiring_within = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Any time'),
            ('7', 'Next 7 days'),
            ('30', 'Next 30 days'),
            ('90', 'Next 90 days'),
        ],
        label='Expiring Within'
    )

