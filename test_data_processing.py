import unittest

from data_processing import autocorrect_phone


class TestDataProcessing(unittest.TestCase):
    def test_autocorrect_phone(self):
        output = autocorrect_phone(123456789.0)
        self.assertEqual(output, "01 23 45 67 89")

        output = autocorrect_phone(623456780.0)
        self.assertEqual(output, "06 23 45 67 80")

        output = autocorrect_phone("06 23 45 67 80")
        self.assertEqual(output, "06 23 45 67 80")
