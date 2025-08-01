# netbox_ssl_certificates/management/commands/check_certificate_expiry.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from netbox_ssl_certificates.models import SSLCertificate
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Check for expiring SSL certificates and send notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days before expiry to send notification (default: 30)'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send notifications to'
        )

    def handle(self, *args, **options):
        days_threshold = options['days']
        email = options['email']
        
        cutoff_date = datetime.now().date() + timedelta(days=days_threshold)
        expiring_certs = SSLCertificate.objects.filter(
            expiry_date__lte=cutoff_date,
            expiry_date__gte=datetime.now().date()
        )
        
        if expiring_certs.exists():
            message = "The following SSL certificates are expiring soon:\n\n"
            for cert in expiring_certs:
                days_left = cert.days_until_expiry
                message += f"- {cert.name} ({cert.common_name}): expires in {days_left} days ({cert.expiry_date})\n"
            
            self.stdout.write(self.style.WARNING(message))
            
            if email:
                send_mail(
                    subject=f'SSL Certificates Expiring Within {days_threshold} Days',
                    message=message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                    recipient_list=[email],
                    fail_silently=False,
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Notification email sent to {email}')
                )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'No certificates expiring within {days_threshold} days')
            )

