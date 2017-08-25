# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import datetime as dt

from tinydb import database
from schematics.exceptions import DataError

from financeager.entries import BaseEntry, CategoryEntry, create_base_entry
from financeager.config import CONFIG


def suite():
    suite = unittest.TestSuite()
    tests = [
            'test_name',
            'test_value',
            'test_date',
            'test_eid'
            ]
    suite.addTest(unittest.TestSuite(map(BaseEntryTestCase, tests)))
    tests = [
            'test_name',
            'test_value',
            'test_str'
            ]
    suite.addTest(unittest.TestSuite(map(NegativeBaseEntryTestCase, tests)))
    suite.addTest(unittest.TestSuite(map(CategoryEntryTestCase, tests)))
    suite.addTest(unittest.TestSuite(map(LongNegativeCategoryEntryTestCase, tests)))
    tests = [
            'test_name',
            'test_value',
            'test_str',
            'test_eid'
            ]
    suite.addTest(unittest.TestSuite(map(BaseEntryFromTinyDbElementTestCase, tests)))
    tests = ['test_invalid_entry']
    suite.addTest(unittest.TestSuite(map(InvalidBaseEntryTestCase, tests)))
    tests = [
            'test_date',
            'test_date_str'
            ]
    suite.addTest(unittest.TestSuite(map(CreateBaseEntryTestCase, tests)))
    return suite

class BaseEntryTestCase(unittest.TestCase):
    def setUp(self):
        self.entry = BaseEntry({"name": "Groceries", "value": 123.45, "date": "2016-08-10"})

    def test_name(self):
        self.assertEqual(self.entry.name, "groceries")

    def test_value(self):
        self.assertAlmostEqual(self.entry.value, 123.45, places=5)

    def test_date(self):
        self.assertEqual(self.entry.date, dt.date(2016, 8, 10))

    def test_eid(self):
        self.assertEqual(self.entry.eid, -1)

class NegativeBaseEntryTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entry = BaseEntry({"name": "VW Bully", "value": -6000, "date":
            "2017-01-01"})

    def test_name(self):
        self.assertEqual(self.entry.name, "vw bully")

    def test_value(self):
        self.assertEqual(self.entry.value, -6000)

    def test_str(self):
        self.assertEqual(str(self.entry),
                "Vw Bully".ljust(BaseEntry.NAME_LENGTH) + " " + " 6000.00 01-01")

class InvalidBaseEntryTestCase(unittest.TestCase):
    def test_invalid_entry(self):
        entry = BaseEntry({"name": "", "value": 1})
        self.assertRaises(DataError, entry.validate)

class CreateBaseEntryTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entry = create_base_entry("Chinese Büffet", -9.90)

    def test_date(self):
        self.assertEqual(self.entry.date, dt.date.today())

    def test_date_str(self):
        self.assertEqual(self.entry.date_str,
                dt.date.today().strftime(CONFIG["DATABASE"]["date_format"]))

class CategoryEntryTestCase(unittest.TestCase):
    def setUp(self):
        self.entry = CategoryEntry({"name": "Gifts"})

    def test_name(self):
        self.assertEqual(self.entry.name, "gifts")

    def test_value(self):
        self.assertEqual(self.entry.value, 0.0)

    def test_str(self):
        self.assertEqual(str(self.entry),
                "Gifts".ljust(CategoryEntry.NAME_LENGTH) + " " +
                "0.00".rjust(BaseEntry.VALUE_LENGTH) + " " +
                BaseEntry.DATE_LENGTH*" ")

class LongNegativeCategoryEntryTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entry = CategoryEntry({"name": "This is quite a LOOONG Category",
            "value": -100, "entries": [create_base_entry("entry", -100, "08-13")]})

    def test_name(self):
        self.assertEqual(self.entry.name, "this is quite a looong category")

    def test_value(self):
        self.assertEqual(self.entry.value, -100)

    def test_str(self):
        self.assertEqual(str(self.entry),
                "This Is Quite A Lo " + "  100.00" + 6*" " + "\n" +
                "  Entry            " + "  100.00" + " 08-13")

class BaseEntryFromTinyDbElementTestCase(unittest.TestCase):
    def setUp(self):
        self.name = "dinner for one"
        self.value = 99.9
        self.date = "2016-12-31"
        self.eid = 1
        element = database.Element(value=dict(name=self.name, value=self.value,
            date=self.date), eid=self.eid)
        self.entry = BaseEntry.from_tinydb(element)

    def test_name(self):
        self.assertEqual(self.entry.name, "dinner for one")

    def test_value(self):
        self.assertAlmostEqual(self.entry.value, self.value, places=5)

    def test_str(self):
        self.assertEqual(str(self.entry), "Dinner For One      99.90 12-31")

    def test_eid(self):
        self.assertEqual(self.entry.eid, self.eid)

if __name__ == '__main__':
    unittest.main()
