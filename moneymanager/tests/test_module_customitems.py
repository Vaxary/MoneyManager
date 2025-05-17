"""Tests for custom modules involving custom StandardItem implementations"""
import unittest

from PyQt6.QtGui import QStandardItemModel

from moneymanager.utils.customitems import (NumStandardItem,
                                            CaseInsensitiveStandardItem)


class TestNumAndCaseInsensitiveStandardItem(unittest.TestCase):
    """Tests for custom modules involving
     custom StandardItem implementations"""
    def setUp(self):
        """Test setting up"""
        self.self_test_model = QStandardItemModel()

        self.num_item1_num = 100
        self.num_item2_num = 200
        self.num_item3_num = 150
        self.num_item4_num = 0
        self.num_item1 = NumStandardItem(str(self.num_item1_num))
        self.num_item2 = NumStandardItem(str(self.num_item2_num))
        self.num_item3 = NumStandardItem(str(self.num_item3_num))
        self.num_item4 = NumStandardItem(str(self.num_item4_num))

        self.case_ins_item1_text = "Asd"
        self.case_ins_item2_text = "zasd"
        self.case_ins_item3_text = "Zasd"
        self.case_ins_item4_text = "asd"
        self.case_ins_item1 = (
            CaseInsensitiveStandardItem(self.case_ins_item1_text))
        self.case_ins_item2 = (
            CaseInsensitiveStandardItem(self.case_ins_item2_text))
        self.case_ins_item3 = (
            CaseInsensitiveStandardItem(self.case_ins_item3_text))
        self.case_ins_item4 = (
            CaseInsensitiveStandardItem(self.case_ins_item4_text))

        self.self_test_model.appendRow([self.num_item1, self.case_ins_item1])
        self.self_test_model.appendRow([self.num_item2, self.case_ins_item2])
        self.self_test_model.appendRow([self.num_item3, self.case_ins_item3])
        self.self_test_model.appendRow([self.num_item4, self.case_ins_item4])

    def test_num_standard_items_all_true(self):
        """True tests for the currency
        numeric based sorting implementation"""
        self.assertTrue(self.num_item1 < self.num_item2)
        self.assertTrue(self.num_item1 < self.num_item3)
        self.assertTrue(self.num_item3 < self.num_item2)
        self.assertTrue(self.num_item4 < self.num_item1)
        self.assertTrue(self.num_item4 < self.num_item2)
        self.assertTrue(self.num_item4 < self.num_item3)

        self.assertTrue(self.num_item1.data(role=2).value() ==
                        str(self.num_item1_num) + " Ft")
        self.assertTrue(self.num_item2.data(role=2).value() ==
                        str(self.num_item2_num) + " Ft")
        self.assertTrue(self.num_item3.data(role=2).value() ==
                        str(self.num_item3_num) + " Ft")
        self.assertTrue(self.num_item4.data(role=2).value() ==
                        str(self.num_item4_num) + " Ft")

    def test_case_insensitive_standard_items_all_true(self):
        """True tests for the case-insensitive
        based sorting implementation"""
        self.assertTrue(self.case_ins_item1 < self.case_ins_item3)
        self.assertTrue(self.case_ins_item1 < self.case_ins_item2)
        self.assertTrue(self.case_ins_item4 < self.case_ins_item2)
        self.assertTrue(self.case_ins_item4 < self.case_ins_item3)

        self.assertTrue(self.case_ins_item1.data(role=2).value() ==
                        self.case_ins_item1_text)
        self.assertTrue(self.case_ins_item2.data(role=2).value() ==
                        self.case_ins_item2_text)
        self.assertTrue(self.case_ins_item3.data(role=2).value() ==
                        self.case_ins_item3_text)
        self.assertTrue(self.case_ins_item4.data(role=2).value() ==
                        self.case_ins_item4_text)

    def test_num_standard_items_all_false(self):
        """False tests for the currency
        numeric based sorting implementation"""
        self.assertFalse(self.num_item2 < self.num_item2)
        self.assertFalse(self.num_item1 < self.num_item1)
        self.assertFalse(self.num_item2 < self.num_item1)
        self.assertFalse(self.num_item2 < self.num_item4)
        self.assertFalse(self.num_item1 < self.num_item4)
        self.assertFalse(self.num_item3 < self.num_item4)

        self.assertFalse(self.num_item1.data(role=2).value()
                         == str(self.num_item1_num) + " Euro")
        self.assertFalse(self.num_item2.data(role=2).value()
                         == str(self.num_item2_num))
        self.assertFalse(self.num_item3.data(role=2).value()
                         == str(self.num_item2_num) + " ft")
        self.assertFalse(self.num_item4.data(role=2).value()
                         == str(self.num_item2_num) + " FT")

    def test_case_insensitive_standard_items_all_false(self):
        """False tests for the case-insensitive
        based sorting implementation"""
        self.assertFalse(self.case_ins_item1 < self.case_ins_item1)
        self.assertFalse(self.case_ins_item2 < self.case_ins_item2)
        self.assertFalse(self.case_ins_item3 < self.case_ins_item3)
        self.assertFalse(self.case_ins_item4 < self.case_ins_item4)
        self.assertFalse(self.case_ins_item2 < self.case_ins_item4)
        self.assertFalse(self.case_ins_item3 < self.case_ins_item4)
        self.assertFalse(self.case_ins_item2 < self.case_ins_item1)
        self.assertFalse(self.case_ins_item3 < self.case_ins_item1)

        self.assertFalse(self.case_ins_item1.data(role=2).value() ==
                         self.case_ins_item1_text + " Ft")
        self.assertFalse(self.case_ins_item2.data(role=2).value() ==
                         self.case_ins_item2_text + " Ft")
        self.assertFalse(self.case_ins_item3.data(role=2).value() ==
                         self.case_ins_item3_text + " Ft")
        self.assertFalse(self.case_ins_item4.data(role=2).value() ==
                         self.case_ins_item4_text + " Ft")
