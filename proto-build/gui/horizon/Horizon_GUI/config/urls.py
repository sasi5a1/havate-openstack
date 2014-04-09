from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from config.views import HomePageView, SettingsView, NodeDiscoveryView, ScenarioDiscoveryView, SubmitSettingsView, SettingsTextView


urlpatterns = patterns('',
    # url(r'^$', 'app_name.views.home', name='home'),
    # url(r'^openstack_installer/', include('openstack_installer.foo.urls')),
    url(r'^$', SettingsView.as_view(), name='home'),
    url(r'^test/$', TemplateView.as_view(template_name="dbbase.html"), name = 'test_page'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
    url(r'^submit_settings/$', SubmitSettingsView.as_view(), name='submit_settings'),
    url(r'^settings_text_view/$', SettingsTextView.as_view(), name='settings_text_view'),
    url(r'^node_discovery/$', NodeDiscoveryView.as_view(), name='node_discovery'),
    url(r'^scenario_discovery/$', ScenarioDiscoveryView.as_view(), name='scenario_discovery'),
)
