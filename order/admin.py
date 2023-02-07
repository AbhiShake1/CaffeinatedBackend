from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'items_str', 'date_ordered', 'status')
    list_filter = ('status', )
    search_fields = ('items__name', )
    ordering = ('-date_ordered',)
    actions = ['mark_done']

    def items_str(self, obj):
        return obj.id

    items_str.short_description = "Items"

    def mark_done(self, request, queryset):
        queryset.update(status=Order.DONE)

    mark_done.short_description = "Mark selected orders as Done"


admin.site.register(Order, OrderAdmin)
