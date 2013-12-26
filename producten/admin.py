from django.contrib import admin

# Register your models here.
from producten.models import Leverancier, SimpelProduct, Eenheid

admin.site.register(Leverancier)
admin.site.register(SimpelProduct)
admin.site.register(Eenheid)

