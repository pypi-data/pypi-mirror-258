from dcim.forms import DeviceFilterForm
from dcim.models import RackRole
from django.utils.translation import gettext_lazy as _
from utilities.forms.fields import DynamicModelMultipleChoiceField


class SPDeviceFilterForm(DeviceFilterForm):
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_role', 'rack_id')),
        (_('Operation'), ('status', 'role_id', 'airflow', 'serial', 'asset_tag', 'mac_address')),
        (_('Hardware'), ('manufacturer_id', 'device_type_id', 'platform_id')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group')),
        (_('Components'), (
            'console_ports', 'console_server_ports', 'power_ports', 'power_outlets', 'interfaces', 'pass_through_ports',
        )),
        (_('Miscellaneous'), (
            'has_primary_ip', 'has_oob_ip', 'virtual_chassis_member', 'config_template_id', 'local_context_data',
        ))
    )

    rack_role = DynamicModelMultipleChoiceField(
        queryset=RackRole.objects.all(),
        required=False,
        label="Rack role",
    )
