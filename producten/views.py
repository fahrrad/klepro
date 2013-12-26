# producten/views.py
from logging import getLogger

from django.views.generic import DetailView, ListView
from klepro.commons import FilterMixin

from .models import SimpelProduct

logger = getLogger(__name__)


class ProductenListView(FilterMixin, ListView):
    allowed_filters = {'naam': 'naam__contains',
                       'leverancier': 'leverancier__naam__contains'}
    model = SimpelProduct


class ProductDetailView(DetailView):
    model = SimpelProduct
