from random import choice
from dateutil.relativedelta import relativedelta
import datetime

from django.db import models


class Eenheid(models.Model):
    """Class staat voor een eenheid waarin een prijs kan uitgedrukt
    worden. \ vb: Liter(L), Kubiek (Kb)"""

    naam = models.CharField(max_length=255, unique=True)
    afkorting = models.CharField(max_length=5, unique=True)

    def __unicode__(self):
        return "%s (%s)" % (self.naam, self.afkorting)


class Leverancier(models.Model):
    """Class die een leverancier voorsteld"""

    naam = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True)
    adres = models.CharField(max_length=255, null=True)
    telefoon = models.CharField(max_length=255, null=True)
    contactpersoon = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.naam, self.email)


class Product(models.Model):
    naam = models.CharField(max_length=255)
    beschrijving = models.CharField(max_length=4000, null=True)

    class Meta:
        abstract = True
        ordering = ["naam"]

class SimpelProduct(Product):
    """Een simpel product. Simpel betekent hier niet samengesteld"""

    leverancier = models.ForeignKey(Leverancier)
    prijs = models.DecimalField(max_digits=6, decimal_places=2)
    eenheid = models.ForeignKey(Eenheid)

    laatste_aanpassing = models.DateField( null=True)

    def klembord_lijn(self):
        return "%s\t%.2f\t%s" % (self.naam, self.prijs, self.eenheid.afkorting, )

    def __unicode__(self):
        return "%s (%.2f/%s)" % (self.naam, self.prijs, self.eenheid.afkorting)

    def prijs_code(self):
        today = datetime.date.today()
        td_1y = relativedelta(years=1)
        td_2y = relativedelta(years=2)

        if self.laatste_aanpassing:
            if today - td_1y < self.laatste_aanpassing <= today:
                return 'normaal'
            elif today - td_2y < self.laatste_aanpassing <= today - td_1y:
                return 'waarschuwing'
            return 'fout'

        return 'geen'

    class Meta:
        unique_together = ['naam', 'leverancier']

class SamengesteldProductLijn(models.Model):
    """Een simpel product met aantal, dat deel is van een samengesteld
    product"""

    simpelProduct = models.ForeignKey(SimpelProduct)
    samengesteldProduct = models.ForeignKey("SamengesteldProduct")
    aantal = models.IntegerField()


class SamengesteldProduct(Product):
    """Een samengesteld product bevat een aantal simpele producten, plus
    een aantal"""

    items = models.ManyToManyField(SimpelProduct, through=SamengesteldProductLijn)

    def __unicode__(self):
        return "%s <%s>" % (self.naam, ','.join(self.simpeleProducten))

    def prijs(self):
        """Berekent de prijs door de individuele prijzen op te tellen"""
        return sum((p.simpelProduct.prijs * p.aantal for p in self.samengesteldproductlijn_set.all()))


def import_product(naam_q, lev_q, eenheid_q, prijs):
    leverancier = Leverancier.objects.get(naam=lev_q)
    eenheid = Eenheid.objects.get(afkorting=eenheid_q)
    SimpelProduct.objects.create(naam=naam_q.lower(),
                                 leverancier=leverancier, eenheid=eenheid, prijs=prijs)

def import_producten_file(filename):
    for naam, leverancier, eenheid, prijs in \
        (x.split('\t') for x in open(filename, 'rb')):

        print naam, leverancier, eenheid, prijs