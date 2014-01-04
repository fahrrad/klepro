# producten/views.py
import codecs
from logging import getLogger
import os
from rexec import FileWrapper
import tempfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from klepro.settings import initiele_marge
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

    def get_context_data(self, **kwargs):
        context = super(ProductenListView, self).get_context_data(**kwargs)
        context['initiele_marge'] = initiele_marge
        context['na_te_kijken'] = False
        return context


class NaTeKijkenProductenListView(ProductenListView):

    def get_queryset(self):
        queryset = super(NaTeKijkenProductenListView, self).get_queryset()

        return queryset.filter(nakijken=True)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductenListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductenListView, self).get_context_data(**kwargs)
        context['na_te_kijken'] = True
        return context

def downloadPrijslijst(request):

    temp = codecs.open('test', 'w', 'utf-8')
    for product in SimpelProduct.objects.filter():
        temp.write(";".join([product.naam, product.leverancier.naam, str(product.prijs), product.eenheid.afkorting]))
        temp.write('\n')

    temp.close()                            # for writing
    temp = open('test')
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='text/plain; charset=utf-8')

    return response
