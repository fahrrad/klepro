from datetime import date

from django.contrib import admin

# Register your models here.
from django.http import HttpResponseRedirect
from producten.models import Leverancier, SimpelProduct, Eenheid


class SimpelProductAdmin(admin.ModelAdmin):

    def response_change(self, request, obj):
        return HttpResponseRedirect(request.GET['next'])

    def response_add(self, request, obj):
        return HttpResponseRedirect(request.GET['next'])

admin.site.register(Leverancier)
admin.site.register(SimpelProduct, SimpelProductAdmin)
admin.site.register(Eenheid)

