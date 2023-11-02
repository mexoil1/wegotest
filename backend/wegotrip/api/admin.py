from datetime import datetime
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.html import format_html

from .models import Order, Payment, Product
from .tasks import confirm_order
from .consts import Constants


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_of_create', 'sum_price', 'status',
                    'date_of_confirm', 'payment_link')

    def payment_link(self, obj):
        if obj.payment and obj.payment.status == Constants.PAYMENT_PAID and obj.status != Constants.ORDER_CONFIRMED:
            return format_html('<a class="button" href="{}">Подтвердить заказ</a>',
                               reverse('admin:confirm_order', args=[obj.id]))
        return ''

    payment_link.short_description = "Действия"

    def confirm_order(self, request, object_id):
        order = Order.objects.get(pk=object_id)
        order.status = Constants.ORDER_CONFIRMED
        order.date_of_confirm = datetime.now()
        order.save()
        confirm_order.delay(object_id)
        return redirect('http://127.0.0.1/admin/api/order/')

    def get_urls(self):
        from django.urls import path

        custom_urls = [
            path('confirm_order/<int:object_id>/',
                 self.admin_site.admin_view(self.confirm_order), name='confirm_order'),
        ]
        return custom_urls + super().get_urls()


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Product)
