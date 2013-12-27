# producten/views.py
from logging import getLogger
from django.forms import forms

from django.views.generic import DetailView, ListView
from klepro.commons import FilterMixin

from .models import SimpelProduct

logger = getLogger(__name__)


class ProductenListView(FilterMixin, ListView):
    allowed_filters = {'naam': 'naam__icontains',
                       'leverancier': 'leverancier__naam__icontains'}
    model = SimpelProduct
    paginate_by = 2
