import zipfile

import datetime
from functools import reduce

from django.views.generic import TemplateView, CreateView

from permissions.mixins import LoginRequiredMixin
from rma.models import ReturnMerchandiseAuthorization
from utils.views import CreateUpdateView


class RMAInitView(LoginRequiredMixin, CreateUpdateView):
    template_name = 'myaccount/rma-init.html'
    model = ReturnMerchandiseAuthorization
    slug_url_kwarg = 'order_hash'
    slug_field = 'order'
    fields = ['shipper']
    # todo make sure that this view is protected and that others can not create rmas for any orders

    def form_valid(self, form):
        # todo build form manually and show description of selected shipper and add orderitem select
        # todo set defaults on save (eg. contact,...)
        # todo select orderitem too
        print('asd')
