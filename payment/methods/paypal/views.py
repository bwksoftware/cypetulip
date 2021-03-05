from django.apps import apps
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest

from payment.models import Payment, PaymentDetail
from shop.views.mixins import EmailConfirmView
from shop.models.orders import OrderState, Order, OrderDetail, OrderItem
from shop.models.products import Product
from shop.utils import create_hash

__author__ = 'Anselm'


class PaymentResponse:
    status = ""
    self_link = ""
    approve_link = ""
    update_link = ""
    capture_link = ""
    payer_action = ""


class PaypalPaymentConfirmationView(View):
    template_name = 'bill/confirm.html'
    model = Payment
    client = None
    fields = []

    def __init__(self):
        super(PaypalPaymentConfirmationView, self).__init__()
        self.client = apps.get_app_config("payment").paypal_client

    def get(self, request, order):
        _order = Order.objects.filter(uuid=order)
        order_details = OrderDetail.objects.get(uuid=order)
        order_items = OrderItem.objects.filter(order=_order[0], order_item__isnull=True,
                                               product__in=Product.objects.all())
        payment_details = PaymentDetail.objects.get(order=_order[0])
        return render(request, self.template_name,
                      {'order_items': order_items,
                       'payment_details': payment_details, 'contact': order_details.contact,
                       'shipment': order_details.shipment_address})


class PaypalSubmitView(EmailConfirmView, View):
    client = None

    def __init__(self):
        super(PaypalSubmitView, self).__init__()
        self.client = apps.get_app_config("payment").paypal_client

    # called when being redirect back to shop from paypal
    def get(self, request, order):
        _order = Order.objects.get(uuid=order)
        order_items = OrderItem.objects.filter(order=_order, order_item__isnull=True,
                                               product__in=Product.objects.all())
        payment_details = PaymentDetail.objects.get(order=_order)
        payment_details.paypal.paypal_payer_id = request.GET['PayerID']
        payment_details.paypal.save()
        order_detail = OrderDetail.objects.get(order=_order)
        order_detail.state = OrderState.objects.get(is_paid_state=True)
        capture_request = OrdersCaptureRequest(payment_details.paypal.paypal_order_id)
        try:
            response = self.client.execute(capture_request)

            if 200 <= response.status_code < 300:
                payment_response = PaymentResponse()
                for link in response.result.links:
                    if link.rel == "approve":
                        payment_response.approve_link = link.href
                    elif link.rel == "payer-action":
                        payment_response.payer_action = link.href

                payment_details.paypal.paypal_transaction_id = response.result.purchase_units[0].payments.captures[0].id
                payment_details.paypal.save()
                order_detail.save()
                if response.result.status == "COMPLETED":
                    payment = Payment(is_paid=True, token=create_hash(), details=payment_details)
                    payment.save()

                    self.object = _order
                    self.notify_client(order_detail.contact)
                    self.notify_staff()
                    return redirect(reverse("shop:confirmed_order", args=[order]))
                elif response.result.status == "PAYER_ACTION_REQUIRED":
                    return HttpResponseRedirect(payment_response.payer_action)

        except IOError as ioe:
            print(ioe.message)
            messages.error(self.request, _("Something went wrong while processing your payment:\n") + ioe.message)
            return HttpResponseRedirect(reverse("payment:paypal",
                                                kwargs={"order": _order.uuid}))
        messages.error(self.request, _("Something went wrong while processing your payment"))
        return HttpResponseRedirect(reverse("payment:paypal",
                                            kwargs={"order": _order.uuid}))

    # called by client when sending order (PayPalConfirmationView)
    def post(self, request, order):
        paypal_request = OrdersCreateRequest()
        order_object = Order.objects.get(uuid=order)
        order_detail = OrderDetail.objects.get(order=order_object)
        order_items = OrderItem.objects.filter(order=order_object)
        total_with_tax = order_detail.total_discounted_wt()

        paypal_request.prefer('return=representation')
        paypal_request.request_body(
            {"intent": "CAPTURE",
             "application_context": {
                 "return_url": "http://" + self.request.META['HTTP_HOST'] + reverse("payment:paypal_submit",
                                                                                    kwargs={
                                                                                        "order": order_object.uuid}),
                 "cancel_url": "http://" + self.request.META['HTTP_HOST'] + reverse("payment:payment",
                                                                                    kwargs={
                                                                                        "order": order_object.uuid})
             },
             "purchase_units": [
                 {
                     "amount": {
                         "currency_code": "EUR",
                         "value": f"{total_with_tax}",
                     },
                     "invoice_id": order_detail.unique_nr()
                 }
             ]}
        )
        try:
            response = self.client.execute(paypal_request)
            if 200 <= response.status_code < 300:
                payment_response = PaymentResponse()
                for link in response.result.links:
                    if link.rel == "approve":
                        payment_response.approve_link = link.href
                    elif link.rel == "payer-action":
                        payment_response.payer_action = link.href
                if response.result.status == "CREATED":
                    payment_detail = PaymentDetail.objects.get(order=order_object)
                    payment_detail.paypal.paypal_order_id = response.result.id
                    payment_detail.paypal.save()

                    self.object = order_object
                    self.notify_client(order_detail.contact)
                    self.notify_staff()
                    return HttpResponseRedirect(payment_response.approve_link)
                elif response.result.status == "PAYER_ACTION_REQUIRED":
                    return HttpResponseRedirect(payment_response.payer_action)
                else:
                    messages.error(self.request, _("Something went wrong while processing your payment"))
                    return HttpResponseRedirect(reverse("payment:paypal",
                                                        kwargs={"order": order_object.uuid}))
        except IOError as ioe:
            pass
