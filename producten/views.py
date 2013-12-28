# producten/views.py
from logging import getLogger
from django.contrib.auth.decorators import login_required
from django.forms import forms
from django.utils.decorators import method_decorator

from django.views.generic import DetailView, ListView
from klepro.commons import FilterMixin

from .models import SimpelProduct

logger = getLogger(__name__)


class ProductenListView(FilterMixin, ListView):
    allowed_filters = {'naam': 'naam__icontains',
                       'leverancier': 'leverancier__naam__icontains'}
    model = SimpelProduct
    paginate_by = 25

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductenListView, self).dispatch(request, *args, **kwargs)


