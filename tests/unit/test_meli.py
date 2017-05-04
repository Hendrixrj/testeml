# -*- coding: utf-8 -*-

"""
Unit tests for functions
"""

import datetime

from unittest import TestCase
from meli import *


class TestMeli(TestCase):

    source = "florianopolis"
    destiny = "brasilia"
    invoice = "50"
    weight = "7"

    meli_class = ""

    def test_round_value(self):

        self.meli_class = Meli(self.source, self.destiny, self.invoice, self.weight)
        result = self.meli_class.round_value(50.5)
        self.assertTrue(result, 51)

    def test_apply_icms(self):
        self.meli_class = Meli(self.source, self.destiny, self.invoice, self.weight)
        result = self.meli_class.apply_icms(51)
        self.assertTrue(result, 54.2553191489)

    def test_define_insurance(self):

        self.meli_class = Meli(self.source, self.destiny, self.invoice, self.weight)
        result = self.meli_class.define_insurance(51, 2)
        self.assertTrue(result, 1.02)

    def test_open_route_csv(self):

        self.meli_class = Meli(self.source, self.destiny, self.invoice, self.weight)
        self.meli_class.open_route_csv('tabela', 'rotas.csv')
        self.assertEquals(self.meli_class.row_route, {'kg': 'flo', 'prazo': '3', 'seguro': '3', 'destino': 'brasilia', 'origem': 'florianopolis', 'fixa': '13'})

    def test_open_kg_price_csv(self):

        self.meli_class = Meli(self.source, self.destiny, self.invoice, self.weight)
        self.meli_class.open_route_csv('tabela', 'rotas.csv')
        self.meli_class.open_kg_price_csv('tabela', 'preco_por_kg.csv')
        self.assertEquals(self.meli_class.row_kg_price, {'preco': '12', 'final': '10', 'inicial': '0', 'nome': 'flo'})
