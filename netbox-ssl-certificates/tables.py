# netbox_ssl_certificates/tables.py
import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import SSLCertificate

class SSLCertificateTable(NetBoxTable):
    name = tables.LinkColumn()
    common_name = tables.Column()
    certificate_type = ChoiceFieldColumn()
    issuer = tables.Column()
    expiry_date = tables.DateColumn()
    days_until_expiry = tables.Column(
        verbose_name='Days Until Expiry',
        accessor='days_until_expiry',
        attrs={'td': {'class': lambda record: 'text-danger' if record.is_expired else 'text-warning' if record.is_expiring_soon else ''}}
    )
    status = ChoiceFieldColumn()
    
    class Meta(NetBoxTable.Meta):
        model = SSLCertificate
        fields = ('pk', 'name', 'common_name', 'certificate_type', 'issuer', 'expiry_date', 'days_until_expiry', 'status')
        default_columns = ('name', 'common_name', 'certificate_type', 'issuer', 'expiry_date', 'days_until_expiry', 'status')

