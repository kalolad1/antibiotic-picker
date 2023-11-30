import os
import json

from django.test import TestCase, tag

from . import path_constants
from . import test_constants


class ViewsTestCase(TestCase):
    fixtures = test_constants.FIXTURES

    @tag(test_constants.SLOW_TEST_FLAG)
    def test_regimen_search_succeeds(self):
        path_to_test_data = os.path.join(
            path_constants.PATH_TO_HANDP_SAMPLES_DIR, "handp_succeeds_1_sbp.txt"
        )

        with open(path_to_test_data, "r") as file:
            test_handp = file.read()

        response = self.client.post("/regimen_search", {"handp_text": test_handp})
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content.decode("utf-8"))
        first_prescription = response_data["regimen"]["prescriptions"][0]
        self.assertEqual(first_prescription["drug"], "cefotaxime")
        self.assertEqual(first_prescription["route"], "IV")
        self.assertEqual(first_prescription["dose"], "1g")
        self.assertEqual(first_prescription["frequency"], "every 8 hours")
        self.assertEqual(first_prescription["start_day"], 1)
        self.assertEqual(first_prescription["end_day"], 7)

        self.assertEqual(response_data["query_data"]["age"], 62)
        self.assertEqual(response_data["query_data"]["sex"], "female")
        self.assertEqual(
            response_data["query_data"]["diagnosis"],
            "spontaneous bacterial peritonitis",
        )

    @tag(test_constants.SLOW_TEST_FLAG)
    def test_regimen_search_raises_error_insufficient_info(self):
        path_to_test_data = os.path.join(
            path_constants.PATH_TO_HANDP_SAMPLES_DIR, "handp_insufficient_info.txt"
        )

        with open(path_to_test_data, "r") as file:
            test_handp = file.read()

        response = self.client.post("/regimen_search", {"handp_text": test_handp})
        self.assertEqual(response.status_code, 400)

        expected_error_message = "The patient's age is not found in h and p"
        response_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response_data["error_message"], expected_error_message)

    @tag(test_constants.SLOW_TEST_FLAG)
    def test_regimen_search_raises_error_diagnosis_not_supported(self):
        path_to_test_data = os.path.join(
            path_constants.PATH_TO_HANDP_SAMPLES_DIR,
            "handp_diagnosis_not_supported.txt",
        )

        with open(path_to_test_data, "r") as file:
            test_handp = file.read()

        response = self.client.post("/regimen_search", {"handp_text": test_handp})
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content.decode("utf-8"))
        expected_error_message = (
            "The following element val is not supported - diagnosis: bacterial"
            " meningitis"
        )
        self.assertEqual(response_data["error_message"], expected_error_message)
