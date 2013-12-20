from django.db import IntegrityError
from django.test import TestCase
from logging import getLogger

from producten.models import Leverancier, SamengesteldProductLijn, SamengesteldProduct,\
    SimpelProduct, Eenheid

logger = getLogger('producten.tests')

# Create your tests here.
class ProductTestCase(TestCase):

    def setUp(self):
        self.h = Eenheid.objects.create(naam="uur", afkorting="h")
        self.kub = Eenheid.objects.create(naam="Kubiek", afkorting="m3")
        self.kg = Eenheid.objects.create(naam="kilogram", afkorting="kg")

        self.vdba = Leverancier.objects.create(naam="VDBA", email="vdba@gmail.com")

        SimpelProduct.objects.create(naam="beton", leverancier=self.vdba,
                                     beschrijving="Zeer hard", prijs=54.0,
                                     eenheid=self.kub)

    def test_vind_product(self):
        p = SimpelProduct.objects.filter(naam='beton')
        self.assertIsNotNone(p)

    def test_vind_leverancier(self):
        l = Leverancier.objects.filter(email="vdba@gmail.com")
        count = l.count()
        self.assertEqual(count, 1)

        self.assertEqual(l[0].naam, "VDBA")

    def test_meerdere_leveranciers(self):
        Leverancier.objects.create(naam="abc", email="abc@gmail.com")
        Leverancier.objects.create(naam="123", email="xcv@gmail.com")
        Leverancier.objects.create(naam="456", email="xz@gmail.com")

        self.assertEqual(Leverancier.objects.count(), 4)
        self.assertEqual(Leverancier.objects.exclude(naam__contains='4').count(), 3)

    def test_uniek_email(self):
        Leverancier.objects.create(naam="abc", email="abc@gmail.com")
        with self.assertRaises(IntegrityError):
            Leverancier.objects.create(naam="123", email="abc@gmail.com")

    def test_simpel_product(self):
        h = Eenheid.objects.get(naam='uur')
        mh = SimpelProduct.objects.create(naam="man uur", beschrijving="Een man uur",
                                          prijs=35.5, eenheid=h, leverancier=self.vdba)
        self.assertEqual("man uur (35.50/h)", mh.__unicode__())

    def test_dubbele_namen(self):
        graszaad = SimpelProduct.objects.create(naam="graszaad", prijs=12,
                                                eenheid=self.kg, leverancier=self.vdba)
        gras_zaaien = SamengesteldProduct(naam="Gras zaaiend", )






