from django.contrib import admin

from .models import(
    Customer,
    Location,
    CustomService,
    OrderService,
    Order,
    Offer,
    ExtraTask,
    DeliveryBook
)


class OrderServiceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer',
        'service',
        'orderd',

    ]

    list_filter = [
        'orderd',
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer',
        'orderd',
        'order_num',
        'complated',
        'date',

    ]

    search_fields = ('order_num', 'customer',)

    list_filter = [
        'orderd',
        'complated'
    ]


class Offerdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'label',
        'expenses',
        'Note',
        'order',
        'order_service',
        'location',
        'date',
        'accepted',
        'validate_conter_offer',
        'conter_offers_counter',
        'not_accepted',

    ]

    search_fields = ('labal', 'date',)

    list_filter = [
        'date',
        'location'
    ]

admin.site.register(OrderService, OrderServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryBook)
admin.site.register(ExtraTask)
admin.site.register(Offer, Offerdmin)
