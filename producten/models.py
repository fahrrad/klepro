from django.db import models


class Eenheid(models.Model):
    """Class staat voor een eenheid waarin een prijs kan uitgedrukt
    worden. \ vb: Liter(L), Kubiek (Kb)"""

    naam = models.CharField(max_length=255)
    afkorting = models.CharField(max_length=5)

    def __unicode__(self):
        return "%s (%s)" % (self.naam, self.afkorting)


class Leverancier(models.Model):
    """Class die een leverancier voorsteld"""

    naam = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    def __unicode__(self):
        return "%s (%s)" % (self.naam, self.email)


class Product(models.Model):
    naam = models.CharField(max_length=255, unique=True)
    beschrijving = models.CharField(max_length=4000, null=True)

    class Meta:
        abstract = True
        ordering = ["-naam"]

class SimpelProduct(Product):
    """Een simpel product. Simpel betekend hier niet samengesteld"""

    leverancier = models.ForeignKey(Leverancier)
    prijs = models.DecimalField(max_digits=6, decimal_places=2)
    eenheid = models.ForeignKey(Eenheid)

    def klembord_lijn(self):
        return "%s\t%.2f" % (self.naam, self.prijs)

    def __unicode__(self):
        return "%s (%.2f/%s)" % (self.naam, self.prijs, self.eenheid.afkorting)


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

