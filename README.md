# netbox-ssl-certificates
The plugin integrates with NetBox's existing UI patterns and provides a solution for SSL certificate lifecycle management.
Key Features:

SSL Certificate Model with fields for:

Certificate metadata (name, common name, SANs)
Certificate details (issuer, serial number, key size)
Expiry tracking (issued date, expiry date, auto-renewal status)
Certificate type and status management
Optional PEM storage


Automatic Status Management:

Auto-updates status based on expiry dates
Calculates days until expiry
Flags expired and expiring-soon certificates


Web Interface:

List view with filtering and search
Detail view for individual certificates
Add/edit/delete functionality
Color-coded expiry warnings


Management Command:

check_certificate_expiry command for monitoring
Email notifications for expiring certificates
Configurable threshold days



Installation Steps:

Install the plugin:
bashpip install -e /path/to/netbox-ssl-certificates

Add to NetBox configuration (configuration.py):
pythonPLUGINS = [
    'netbox_ssl_certificates',
]

Run migrations:
bashpython manage.py migrate

Create templates (you'll need to create these in your NetBox templates directory):

netbox_ssl_certificates/sslcertificate_list.html
netbox_ssl_certificates/sslcertificate.html
netbox_ssl_certificates/sslcertificate_edit.html
netbox_ssl_certificates/sslcertificate_delete.html



Usage Examples:
Check expiring certificates via command line:
bashpython manage.py check_certificate_expiry --days 30 --email admin@example.com
Set up automated monitoring (add to crontab):
bash0 9 * * * cd /opt/netbox && python manage.py check_certificate_expiry --days 30 --email admin@example.com
The plugin integrates seamlessly with NetBox's existing UI patterns and provides a complete solution for SSL certificate lifecycle management. Would you like me to help you with any specific customizations or the template files?RetryClaude does not have the ability to run the code it generates yet.Claude can make mistakes. Please double-check responses.
