from django.contrib import admin

from .models import Consumer


class ConsumerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'fcm_token')
    search_fields = ('name', 'email')
    ordering = ('name',)


admin.site.register(Consumer, ConsumerAdmin)
