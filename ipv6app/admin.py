from django.contrib import admin
from ipv6app.models import Prefix

class PrefixAdmin(admin.ModelAdmin):
    list_display = ('ip', 'mask', 'name', 'possible', 'flag')


admin.site.register(Prefix, PrefixAdmin)
    
