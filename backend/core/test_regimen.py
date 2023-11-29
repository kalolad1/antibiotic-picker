from django.test import TestCase

from .regimen import Duration


class RegimenTestCase(TestCase):
    def test_duration__str__(self):
        self.assertEqual(str(Duration(num_days=10)), "1 week and 3 days")
        self.assertEqual(str(Duration(num_days=5)), "5 days")
        self.assertEqual(str(Duration(num_days=1)), "1 day")
        self.assertEqual(str(Duration(num_days=21)), "3 weeks")
        self.assertEqual(str(Duration(num_days=25)), "3 weeks and 4 days")
