from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Div

from config.models import OpenstackSettings, NodeSettings


class NoFormTagCrispyFormMixin(object):
    @property
    def helper(self):
        if not hasattr(self, '_helper'):
            self._helper = FormHelper()
            self._helper.form_tag = False
        return self._helper


class OpenstackSettingsForm(forms.ModelForm, NoFormTagCrispyFormMixin):
    class Meta:
        model = OpenstackSettings
        widgets = {
            'cluster_type': forms.RadioSelect(),
            'os_cluster_type': forms.RadioSelect(),
            'os_type': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(OpenstackSettingsForm, self).__init__(*args, **kwargs)
        self.fields['cluster_type'].choices = self.fields['cluster_type'].choices[1:]
        self.fields['os_cluster_type'].choices = self.fields['os_cluster_type'].choices[1:]
        self.fields['os_type'].choices = self.fields['os_type'].choices[1:]


class ClusterSettingsForm(forms.ModelForm, NoFormTagCrispyFormMixin):
    class Meta:
        model = OpenstackSettings
        fields = ('cluster_name', 'cluster_type')
        widgets = {
            'cluster_type': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(ClusterSettingsForm, self).__init__(*args, **kwargs)
        self.initialize_helper()
        self.fields['cluster_type'].choices = self.fields['cluster_type'].choices[1:]

    def initialize_helper(self):
        self.helper.layout = Layout(
            Div( Div( Field('cluster_name'), css_class='col-md-4'), css_class='row'),
            Div( Div( Field('cluster_type'), css_class='col-md-4'), css_class='row'),
        )


class UCSMSettingsForm(forms.ModelForm, NoFormTagCrispyFormMixin):
    class Meta:
        model = OpenstackSettings
        fields = ('ucsm_hostname', 'username', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UCSMSettingsForm, self).__init__(*args, **kwargs)
        self.initialize_helper()

    def initialize_helper(self):
        self.helper.layout = Layout(
            Div( Div( Field('ucsm_hostname'), css_class='col-md-4'), css_class='row'),
            Div( Div( Field('username'), css_class='col-md-4'), css_class='row'),
            Div( Div( Field('password'), css_class='col-md-4'), css_class='row'),
            
        )


class OSSettingsForm(forms.ModelForm, NoFormTagCrispyFormMixin):
    class Meta:
        model = OpenstackSettings
        fields = ('os_cluster_type', 'os_type')
        widgets = {
            'os_cluster_type': forms.RadioSelect(),
            'os_type': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(OSSettingsForm, self).__init__(*args, **kwargs)
        self.fields['os_cluster_type'].choices = self.fields['os_cluster_type'].choices[1:]
        self.fields['os_type'].choices = self.fields['os_type'].choices[1:]


class NetworkSettingsForm(forms.ModelForm, NoFormTagCrispyFormMixin):
    class Meta:
        model = OpenstackSettings
        fields = ('mgmt_vlan', 'pxe_vlan', 'iscsi_vlan', 'storage_vlan', 'public_provider_vlan', 'private_vlan', 'tenants_vlan', 'mgmt_subnet', 'pxe_subnet', 'iscsi_subnet', 'storage_subnet', 'public_provider_subnet', 'private_subnet', 'tenants_subnet', 'mac_pool', 'mac_pool_size',)

    def __init__(self, *args, **kwargs):
        super(NetworkSettingsForm, self).__init__(*args, **kwargs)
        self.initialize_helper()
        self.fields['mac_pool_size'].label = "Size"
        self.fields['mgmt_vlan'].label = "Mgmt"
        self.fields['pxe_vlan'].label = "PXE Private"
        self.fields['iscsi_vlan'].label = "iSCSI"
        self.fields['storage_vlan'].label = "Storage"
        self.fields['public_provider_vlan'].label = "Public Provider"
        self.fields['private_vlan'].label = "Private"
        self.fields['tenants_vlan'].label = "Tenants"
        self.fields['mgmt_subnet'].label = ""
        self.fields['pxe_subnet'].label = ""
        self.fields['iscsi_subnet'].label = ""
        self.fields['storage_subnet'].label = ""
        self.fields['public_provider_subnet'].label = ""
        self.fields['private_subnet'].label = ""
        self.fields['tenants_subnet'].label = ""

    def initialize_helper(self):
        self.helper.layout = Layout(
            Div(
                Div(Field('mgmt_vlan'), css_class='col-md-4 vlan-field'),
                Div(Field('mgmt_subnet'), css_class='col-md-4 subnet-field'),
                css_class='row'
            ),
            Div(
                Div(Field('pxe_vlan'), css_class='col-md-4 vlan-field'),
                Div(Field('pxe_subnet'), css_class='col-md-4 subnet-field'),
                css_class='row'
            ),
            Div(
                Div(Field('iscsi_vlan'), css_class='col-md-4 vlan-field'),
                Div(Field('iscsi_subnet'), css_class='col-md-4 subnet-field'),
                css_class='row'
            ),
            Div(
                Div(Field('storage_vlan'), css_class='col-md-4 vlan-field'),
                Div(Field('storage_subnet'), css_class='col-md-4 subnet-field'),
                css_class='row'
            ),
            Div(
                Div(Field('public_provider_vlan'), css_class='col-md-4 vlan-field'),
                Div(Field('public_provider_subnet'), css_class='col-md-4 subnet-field'),
                css_class='row'
            ),
            Div(
                Div(Field('private_vlan'), css_class='col-md-4 vlan-field'),
                Div(Field('private_subnet'), css_class='col-md-4 subnet-field'),
                css_class='row'
            ),
            Div(
                Div(Field('tenants_vlan'), css_class='col-md-4 vlan-field'),
                Div(Field('tenants_subnet'), css_class='col-md-4 subnet-field'),
                css_class='row'
            ),
            HTML('<hr>'),
            Div(
                Div(Field('mac_pool'), css_class='col-md-4'),
                Div(Field('mac_pool_size'), css_class='col-md-4'),
                css_class='row'
            ),
        )


class HostSettingsForm(forms.ModelForm, NoFormTagCrispyFormMixin):
    class Meta:
        model = OpenstackSettings
        fields = ('hostname_prefix_compute_nodes', 'hostname_prefix_swift_nodes')

    def __init__(self, *args, **kwargs):
        super(HostSettingsForm, self).__init__(*args, **kwargs)
        self.initialize_helper()
        

    def initialize_helper(self):
        self.helper.layout = Layout(
            Div( Div( Field('hostname_prefix_compute_nodes'), css_class='col-md-4'), css_class='row'),
            Div( Div( Field('hostname_prefix_swift_nodes'), css_class='col-md-4'), css_class='row'),
        )


class NodeSettingsForm(forms.ModelForm, NoFormTagCrispyFormMixin):
    class Meta:
        model = NodeSettings
        widgets = {
            'aio': forms.RadioSelect(),
            'network': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(NodeSettingsForm, self).__init__(*args, **kwargs)
        self.initialize_helper()
        self.fields['aio'].label = ""
        self.fields['aio'].choices = [('true', '')]
        self.fields['compute'].label = ""
        self.fields['network'].label = ""
        self.fields['network'].choices = [('true', '')]
        self.fields['swift'].label = ""
        self.fields['cinder'].label = ""


    def initialize_helper(self):
        self.helper.layout = Layout(
            Div(
                Div(HTML('Node Location<br> CPU/Mem/Disk/Adapter'), css_class='col-md-2'),
                Div(Field('aio'), css_class='col-md-2'),
                Div(Field('compute'), css_class='col-md-2'),
                Div(Field('network'), css_class='col-md-2'),
                Div(Field('swift'), css_class='col-md-2'),
                Div(Field('cinder'), css_class='col-md-2'),
                css_class='row'
            ),
        )






