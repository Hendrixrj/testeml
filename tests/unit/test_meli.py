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
