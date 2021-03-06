from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View

from payment.models import Payment, PaymentDetail
from shop.views.mixins import EmailConfirmView
from shop.models.orders import Order, OrderDetail, OrderItem
from shop.models.products import Product
from shop.utils import create_hash

__author__ = 'Anselm'


class PrepaymentConfirmView(View):
    template_name = 'bill/confirm.html'

    def get(self, request, order):
        _order = Order.objects.filter(uuid=order)
        order_details = OrderDetail.objects.get(uuid=order)
        order_items = OrderItem.objects.filter(order=_order[0], order_item__isnull=True,
                                               product__in=Product.objects.all())
        payment_details = PaymentDetail.objects.get(order=_order[0])
        return render(request, self.template_name,
                      {'order_items': order_items, 'payment_details': payment_details, 'contact': order_details.contact, 'order_detail': order_details,
                       'shipment': order_details.shipment_address})

class PrepaymentSubmitView(EmailConfirmView, View):

    def get(self, request, order):
        _order = Order.objects.filter(uuid=order)
        order_items = OrderItem.objects.filter(order=_order[0], order_item__isnull=True,
                                               product__in=Product.objects.all())
        payment_details = PaymentDetail.objects.get(order=_order[0])
        payment = Payment(is_paid=False, token=create_hash(), details=payment_details)
        payment.save()
        return redirect(reverse("shop:confirmed_order", args=[order]))

    def post(self, request, order):

        _order = Order.objects.filter(uuid=order)
        order_items = OrderItem.objects.filter(order=_order[0], order_item__isnull=True,
                                               product__in=Product.objects.all())
        payment_details = PaymentDetail.objects.get(order=_order[0])
        payment = Payment(is_paid=False, token=create_hash(), details=payment_details)
        payment.save()
        self.object = _order[0]
        self.notify_client(self.object.orderdetail_set.first().contact)
        self.notify_staff()
        return redirect(reverse("shop:confirmed_order", args=[order]))
