from django.contrib import admin

from .models import Activity, UserActivity, UserActivityLog

# Register your models here.
admin.site.register(Activity, admin.ModelAdmin)
admin.site.register(UserActivity, admin.ModelAdmin)
admin.site.register(UserActivityLog, admin.ModelAdmin)