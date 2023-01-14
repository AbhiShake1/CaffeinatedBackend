from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'items_str', 'date_ordered', 'total_price', 'status')
    list_filter = ('student', 'status')
    search_fields = ('student__username', 'items__name')
    ordering = ('-date_ordered',)
    actions = ['mark_done']

    def items_str(self, obj):
        return ", ".join([str(i) for i in obj.items.all()])

    items_str.short_description = "Items"

    def mark_done(self, request, queryset):
        queryset.update(status=Order.DONE)

    mark_done.short_description = "Mark selected orders as Done"


admin.site.register(Order, OrderAdmin)
