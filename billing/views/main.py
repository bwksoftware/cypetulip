import os
from datetime import timedelta, datetime
from io import BytesIO

from django.db.models import FloatField, F
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from billing.utils import calculate_sum, Round
from home import settings
from management.models.models import LegalSetting
from payment.models import PaymentDetail
from permissions.mixins import PermissionOwnsObjectMixin
from shop.models.orders import Order, OrderDetail, OrderItem


class HTMLPreview(PermissionOwnsObjectMixin, View):
    model = OrderDetail
    slug_field = "order__order_hash"
    slug_url_kwarg = "order"
    field_name = "contact"

    def get(self, request, order):
        _order = Order.objects.get(order_hash=order)
        order_detail = OrderDetail.objects.get(order=_order)
        contact = order_detail.contact
        company = _order.company
        order_items = OrderItem.objects.filter(order=_order, order_item__isnull=True).annotate(
            price_t=Round(F('price') * Cast(F('count'), FloatField()),2),
        )
        if not order_detail.date_bill:
            order_detail.date_bill = datetime.now()
        order_detail.date_due = order_detail.date_bill + timedelta(days=company.term_of_payment)

        legal_settings = LegalSetting.objects.first()
        total_without_tax = calculate_sum(order_items)
        total_with_tax = calculate_sum(order_items, True)
        payment_detail = PaymentDetail.objects.get(order=_order)
        tax_rate = int(round(total_with_tax / total_without_tax, 2)*100)-100 if total_without_tax > 0 else 0

        context = {
            'total': total_with_tax,
            'total_without_tax': total_without_tax,
            'tax': round(order_detail.total_wt() - order_detail.total(), 2),
            'tax_rate': tax_rate,
            'order': _order,
            'order_detail': order_detail,
            'order_items': order_items,
            'contact': contact,
            'company': company,
            'payment_detail': payment_detail,
            'invoice_settings': legal_settings,
        }

        return render(request, 'billing/invoice.html', context)



class GeneratePDFFile():
    def generate(self, _order):
        order_detail = OrderDetail.objects.get(order=_order)
        contact = order_detail.contact
        company = _order.company
        order_items = OrderItem.objects.filter(order=_order, order_item__isnull=True).annotate(
            price_t=Round(F('price') * Cast(F('count'), FloatField()),2),
        )
        if not order_detail.date_bill:
            order_detail.date_bill = datetime.now()
        order_detail.date_due = order_detail.date_bill + timedelta(days=company.term_of_payment)

        legal_settings = LegalSetting.objects.first()
        total_without_tax = calculate_sum(order_items)
        total_with_tax = calculate_sum(order_items, True)
        payment_detail = PaymentDetail.objects.get(order=_order)
        tax_rate = int(round(total_with_tax / total_without_tax, 2)*100)-100

        context = {
            'total': total_with_tax,
            'total_without_tax': total_without_tax,
            'tax': round(order_detail.total_discounted_wt() - order_detail.total_discounted(), 2),
            'tax_rate': tax_rate,
            'order': _order,
            'order_detail': order_detail,
            'order_items': order_items,
            'contact': contact,
            'company': company,
            'payment_detail': payment_detail,
            'invoice_settings': legal_settings,
        }
        return self.render_to_pdf('billing/invoice.html', context)

    def render_to_pdf(self, template_src, context_dict=None):
        if context_dict is None:
            context_dict = {}
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=self.link_callback)
        if not pdf.err:
            return result
        return None

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path



class GeneratePDF(GeneratePDFFile,PermissionOwnsObjectMixin, View):
    model = OrderDetail
    slug_field = "order__order_hash"
    slug_url_kwarg = "order"
    field_name = "contact"

    def get(self, request, order):
        _order = Order.objects.get(order_hash=order)
        pdf = HttpResponse(self.generate(_order).getvalue(), content_type='application/pdf')
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % _order.order_hash
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
