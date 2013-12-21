from django.db import IntegrityError
from django.test import TestCase
from logging import getLogger

from producten.models import Leverancier, SamengesteldProductLijn, SamengesteldProduct,\
    SimpelProduct, Eenheid

logger = getLogger('producten.tests')


# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        # eenheden
        self.h = Eenheid.objects.create(naam="uur", afkorting="h")
        self.kub = Eenheid.objects.create(naam="Kubiek", afkorting="m3")
        self.kg = Eenheid.objects.create(naam="kilogram", afkorting="kg")

        # leveranciers
        self.vdba = Leverancier.objects.create(naam="VDBA", email="vdba@gmail.com")
        self.tuinen = Leverancier.objects.create(naam="Tuinen Burssens")

        # simpel producten
        self.beton = SimpelProduct.objects.create(naam="beton", leverancier=self.vdba,
                                     beschrijving="Zeer hard", prijs=54.0,
                                     eenheid=self.kub)
        self.man_uur = SimpelProduct.objects.create(naam="man uur", prijs=35.0, leverancier=self.tuinen,
                                     eenheid=self.h)
        self.graszaad = graszaad = SimpelProduct.objects.create(naam="graszaad", prijs=12,
                                                eenheid=self.kg, leverancier=self.vdba)

        # Samengestelde producten
        self.gras_zaaien = SamengesteldProduct.objects.create(naam="Gras zaaien")
        SamengesteldProductLijn.objects.create(simpelProduct=graszaad,
                                               samengesteldProduct=self.gras_zaaien, aantal=2)
        SamengesteldProductLijn.objects.create(samengesteldProduct=self.gras_zaaien,
                                               simpelProduct=self.man_uur, aantal=1)

    def test_vind_product(self):
        p = SimpelProduct.objects.filter(naam='beton')
        self.assertIsNotNone(p)

    def test_vind_leverancier(self):
        l = Leverancier.objects.filter(email="vdba@gmail.com")
        count = l.count()
        self.assertEqual(count, 1)

        self.assertEqual(l[0].naam, "VDBA")

    def test_meerdere_leveranciers(self):
        map(lambda c: c.delete(), Leverancier.objects.all())
        Leverancier.objects.create(naam="abc", email="abc@gmail.com")
        Leverancier.objects.create(naam="123", email="xcv@gmail.com")
        Leverancier.objects.create(naam="456", email="xz@gmail.com")

        self.assertEqual(Leverancier.objects.exclude(naam__contains='4').count(), 2)

    def test_uniek_email(self):
        Leverancier.objects.create(naam="abc", email="abc@gmail.com")
        with self.assertRaises(IntegrityError):
            Leverancier.objects.create(naam="123", email="abc@gmail.com")

    def test_simpel_product(self):
        self.assertEqual("man uur (35.00/h)", self.man_uur.__unicode__())

    def test_prijs_samengesteld_product(self):
        self.assertAlmostEqual(59.00, self.gras_zaaien.prijs())










