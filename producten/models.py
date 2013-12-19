from django.db import models


class Leverancier(models.Model):
    """Class die een leverancier voorsteld"""
    naam = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)


class SimpelProduct(models.Model):
    """Een simpel product. Simpel betekend hier niet samengesteld"""
    leverancier = models.ForeignKey(Leverancier)
    prijs = models.DecimalField(max_digits=6, decimal_places=2)

    naam = models.CharField(max_length=255)
    beschrijving = models.CharField(max_length = 4000)

class SamengesteldProductLijn(models.Model):
    """Een simpel product met aantal, dat deel is van een samengesteld
    product"""

    simpelProduct = models.ForeignKey(SimpelProduct)
    aantal = models.IntegerField()

class SamengesteldProduct(models.Model):
    """Een samengesteld product bevat een aantal simpele producten, plus
    een aantal"""

    simpeleProducten = models.ManyToManyField(SamengesteldProductLijn)
    naam = models.CharField(max_length=255)
    beschrijving = models.CharField(max_length = 4000)
