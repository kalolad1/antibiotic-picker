from django.test import TestCase, tag

from . import test_constants
from .generate_reference_documents import generate_reference_documents


class DecisionFunctionTestCase(TestCase):
    fixtures = test_constants.FIXTURES

    @tag(test_constants.SLOW_TEST_FLAG)
    def test_generate_reference_documents(self):
        generate_reference_documents()
