
import datetime
from dateutil.relativedelta import relativedelta
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
        self.vdba = Leverancier.objects.create(naam="VDBA", email="test@gmail.com")
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
        l = Leverancier.objects.filter(email="test@gmail.com")
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

    def test_prijs_code(self):
        self.beton.laatste_aanpassing = datetime.date.today() - relativedelta(weeks=6)
        self.assertEqual('normaal', self.beton.prijs_code())


        self.beton.laatste_aanpassing = datetime.date.today() - relativedelta(years=1, months=6)
        self.assertEqual('waarschuwing', self.beton.prijs_code())

        self.beton.laatste_aanpassing = datetime.date.today() - relativedelta(years=2)
        self.assertEqual('fout', self.beton.prijs_code())


    def test_unq_naam_leverancier(self):
        # save nog een beton, van andere leverancier
        SimpelProduct.objects.create(naam="beton", leverancier=self.tuinen,
                                     beschrijving="Zeer hard", prijs=54.0,
                                     eenheid=self.kub)

        betons = SimpelProduct.objects.filter(naam="beton")
        self.assertEqual(2, betons.count())

        # maar 2 * beton bij tuinen kan niet!
        fout_beton = SimpelProduct(naam="beton", leverancier=self.tuinen,
                                     beschrijving="Zeer hard", prijs=54.0,
                                     eenheid=self.kub)

        with self.assertRaises(IntegrityError):
            fout_beton.save()


    def test_unieke_leverancier(self):
        with self.assertRaises(IntegrityError):
            Leverancier.objects.create(naam="VDBA", email="test_2dwefg@gmail.com")




