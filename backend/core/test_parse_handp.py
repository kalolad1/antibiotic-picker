from django.test import TestCase, tag
import os

from . import parse_handp
from .query_data import Allergy, Sex
from .diagnosis import Diagnosis
from .path_constants import PATH_TO_HANDP_SAMPLES_DIR
from .test_constants import SLOW_TEST_FLAG, FIXTURES


class ParseHandpTestCase(TestCase):
    fixtures = FIXTURES

    @tag(SLOW_TEST_FLAG)
    def test_parse_handp_sbp(self):
        path_to_test_data = os.path.join(
            PATH_TO_HANDP_SAMPLES_DIR, "handp_succeeds_1_sbp.txt"
        )

        with open(path_to_test_data, "r") as file:
            test_handp = file.read()

        query_data_instance = parse_handp.parse_handp(test_handp)
        self.assertEqual(query_data_instance.age, 62)
        self.assertEqual(query_data_instance.sex, Sex.FEMALE)
        self.assertEqual(
            query_data_instance.diagnosis,
            Diagnosis.objects.get(name="spontaneous bacterial peritonitis"),
        )

    @tag(SLOW_TEST_FLAG)
    def test_parse_handp_pyelonephritis(self):
        path_to_test_data = os.path.join(
            PATH_TO_HANDP_SAMPLES_DIR, "handp_pyelonephritis.txt"
        )

        with open(path_to_test_data, "r") as file:
            test_handp = file.read()

        query_data_instance = parse_handp.parse_handp(test_handp)
        self.assertEqual(query_data_instance.age, 32)
        self.assertEqual(query_data_instance.sex, Sex.FEMALE)
        self.assertEqual(
            query_data_instance.diagnosis, Diagnosis.objects.get(name="pyelonephritis")
        )

    @tag(SLOW_TEST_FLAG)
    def test_parse_handp_insufficient_info(self):
        path_to_test_data = os.path.join(
            PATH_TO_HANDP_SAMPLES_DIR, "handp_insufficient_info.txt"
        )

        with open(path_to_test_data, "r") as file:
            test_handp = file.read()

        self.assertRaises(
            parse_handp.ParseHandpError,
            parse_handp.parse_handp,
            test_handp,
        )

    @tag(SLOW_TEST_FLAG)
    def test_parse_handp_similar_diagnosis(self):
        # If the detected diagnosis is similar in semantics
        # to one that we support, we should set the diagnosis
        # to be equal to the one ground truth representation.
        # For example: "acute bacterial cystitis" -> "acute cystitis"
        path_to_test_data = os.path.join(
            PATH_TO_HANDP_SAMPLES_DIR, "handp_acute_bacterial_cystitis.txt"
        )

        with open(path_to_test_data, "r") as file:
            test_handp = file.read()

        # Should result in DiagnosisNotSupported
        query_data_instance = parse_handp.parse_handp(test_handp)
        self.assertEqual(query_data_instance.age, 28)
        self.assertEqual(query_data_instance.sex, Sex.FEMALE)
        self.assertEqual(
            query_data_instance.diagnosis, Diagnosis.objects.get(name="acute cystitis")
        )

    @tag(SLOW_TEST_FLAG)
    def test_parse_handp_sbp_penicillin_allergy(self):
        path_to_test_data = os.path.join(
            PATH_TO_HANDP_SAMPLES_DIR, "handp_sbp_penicillin_allergy.txt"
        )

        with open(path_to_test_data, "r") as file:
            test_handp = file.read()

        query_data_instance = parse_handp.parse_handp(test_handp)
        self.assertEqual(query_data_instance.age, 62)
        self.assertEqual(query_data_instance.sex, Sex.FEMALE)
        self.assertEqual(
            query_data_instance.allergy,
            Allergy.objects.get(name="penicillin"),
        )
        self.assertEqual(
            query_data_instance.diagnosis,
            Diagnosis.objects.get(name="spontaneous bacterial peritonitis"),
        )
