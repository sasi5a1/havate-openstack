from django.contrib import admin
from config.models import OpenstackSettings, NodeSettings


admin.site.register(OpenstackSettings)
admin.site.register(NodeSettings)
