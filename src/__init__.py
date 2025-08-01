# netbox_ssl_certificates/__init__.py
from netbox.plugins import PluginConfig

class SSLCertificatesConfig(PluginConfig):
    name = 'netbox_ssl_certificates'
    verbose_name = 'SSL Certificates'
    description = 'Track SSL certificates and their expiry dates'
    version = '0.1'
    base_url = 'ssl-certificates'
    min_version = '3.0.0'

config = SSLCertificatesConfig

# netbox_ssl_certificates/models.py
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from datetime import datetime, timezone

class CertificateTypeChoices(ChoiceSet):
    key = 'CertificateType'
    CHOICES = [
        ('domain', 'Domain Validated (DV)', 'green'),
        ('organization', 'Organization Validated (OV)', 'blue'),
        ('extended', 'Extended Validation (EV)', 'purple'),
        ('wildcard', 'Wildcard', 'orange'),
        ('self_signed', 'Self-Signed', 'gray'),
    ]

class CertificateStatusChoices(ChoiceSet):
    key = 'CertificateStatus'
    CHOICES = [
        ('active', 'Active', 'green'),
        ('expired', 'Expired', 'red'),
        ('expiring_soon', 'Expiring Soon', 'yellow'),
        ('revoked', 'Revoked', 'gray'),
        ('pending', 'Pending', 'blue'),
    ]

class SSLCertificate(NetBoxModel):
    name = models.CharField(
        max_length=100,
        help_text="Friendly name for the certificate"
    )
    
    common_name = models.CharField(
        max_length=255,
        help_text="Primary domain name for the certificate"
    )
    
    subject_alternative_names = models.TextField(
        blank=True,
        help_text="Additional domain names (SANs), one per line"
    )
    
    certificate_type = models.CharField(
        max_length=50,
        choices=CertificateTypeChoices,
        default=CertificateTypeChoices.CHOICES[0][0]
    )
    
    issuer = models.CharField(
        max_length=255,
        help_text="Certificate Authority that issued the certificate"
    )
    
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Certificate serial number"
    )
    
    issued_date = models.DateField(
        help_text="Date when the certificate was issued"
    )
    
    expiry_date = models.DateField(
        help_text="Date when the certificate expires"
    )
    
    key_size = models.PositiveIntegerField(
        validators=[MinValueValidator(512), MaxValueValidator(8192)],
        default=2048,
        help_text="Key size in bits"
    )
    
    signature_algorithm = models.CharField(
        max_length=50,
        default='SHA256withRSA',
        help_text="Signature algorithm used"
    )
    
    status = models.CharField(
        max_length=50,
        choices=CertificateStatusChoices,
        default=CertificateStatusChoices.CHOICES[0][0]
    )
    
    auto_renewal = models.BooleanField(
        default=False,
        help_text="Whether this certificate has auto-renewal enabled"
    )
    
    certificate_pem = models.TextField(
        blank=True,
        help_text="PEM encoded certificate (optional)"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about this certificate"
    )

    class Meta:
        ordering = ['expiry_date', 'common_name']
        unique_together = ['common_name', 'serial_number']

    def __str__(self):
        return f"{self.name} ({self.common_name})"

    def get_absolute_url(self):
        return reverse('plugins:netbox_ssl_certificates:sslcertificate', args=[self.pk])

    @property
    def days_until_expiry(self):
        """Calculate days until certificate expires"""
        today = datetime.now().date()
        delta = self.expiry_date - today
        return delta.days

    @property
    def is_expired(self):
        """Check if certificate is expired"""
        return self.days_until_expiry < 0

    @property
    def is_expiring_soon(self):
        """Check if certificate expires within 30 days"""
        return 0 <= self.days_until_expiry <= 30

    def save(self, *args, **kwargs):
        # Auto-update status based on expiry date
        if self.is_expired:
            self.status = 'expired'
        elif self.is_expiring_soon:
            self.status = 'expiring_soon'
        elif self.status in ['expired', 'expiring_soon']:
            self.status = 'active'
        
        super().save(*args, **kwargs)
