from random import choice
from dateutil.relativedelta import relativedelta
import datetime
from decimal import Decimal

from django.db import models


class Eenheid(models.Model):
    """Class staat voor een eenheid waarin een prijs kan uitgedrukt
    worden. \ vb: Liter(L), Kubiek (Kb)"""

    naam = models.CharField(max_length=255, unique=True)
    afkorting = models.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return "%s (%s)" % (self.naam, self.afkorting)

    class Meta:
        verbose_name_plural='Eenheden'


class Leverancier(models.Model):
    """Class die een leverancier voorsteld"""

    naam = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    adres = models.CharField(max_length=255, blank=True)
    telefoon = models.CharField(max_length=255, blank=True)
    contactpersoon = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.naam, self.email)


class Product(models.Model):
    naam = models.CharField(max_length=255)
    beschrijving = models.CharField(max_length=4000, blank=True)

    class Meta:
        abstract = True
        ordering = ["naam"]

class SimpelProduct(Product):
    """Een simpel product. Simpel betekent hier niet samengesteld"""

    leverancier = models.ForeignKey(Leverancier)
    prijs = models.DecimalField(max_digits=6, decimal_places=2)
    minimum_hoeveelheid = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    eenheid = models.ForeignKey(Eenheid)


    laatste_aanpassing = models.DateField(null=True, default=datetime.date.today())

    nakijken = models.BooleanField(default=False)

    img_url = models.CharField(max_length=1000, blank=True)

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
        verbose_name_plural = 'producten'
        ordering = ["naam"]

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


def import_product(naam_q, prijs, eenheid_q, lev_q, minimum, datum, te_checken):
    try:
        leverancier = Leverancier.objects.get(naam__iexact=lev_q)
    except:
        leverancier = Leverancier.objects.create(naam=lev_q)

    try:
        eenheid = Eenheid.objects.get(afkorting__iexact=eenheid_q)
    except:
        eenheid = Eenheid.objects.create(afkorting=eenheid_q, naam=eenheid_q)

    SimpelProduct.objects.create(naam=naam_q,
                                 leverancier=leverancier, eenheid=eenheid, prijs=prijs,
                                 minimum_hoeveelheid=minimum, nakijken=(te_checken == 1),
                                 laatste_aanpassing=datum)


def import_producten_file(filename):
    for naam, prijs, eenheid, leverancier, minimum, datum, check in \
            (x.split('\t') for x in open(filename, 'rb')):

        print '|'.join([naam, prijs, eenheid, leverancier, minimum,
                        repr(datetime.datetime.strptime(datum, '%d/%m/%Y',)), check])

        import_product(naam, prijs, eenheid, leverancier, minimum,
                       datetime.datetime.strptime(datum, '%d/%m/%Y',), check)