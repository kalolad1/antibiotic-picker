from django.test import TestCase

from . import decision_functions
from .query_data import QueryData, Sex, Vitals, BloodPressureMeasurement
from .diagnosis import Diagnosis
from .allergy import Allergy
from . import test_constants


class DecisionFunctionTestCase(TestCase):
    fixtures = test_constants.FIXTURES

    def test_if_male_YES(self):
        query_data = QueryData(
            age=24, sex=Sex.MALE, diagnosis=Diagnosis.objects.first()
        )
        decision_key = decision_functions.if_male(query_data=query_data)
        expected_decision_key = "YES"
        self.assertEqual(decision_key, expected_decision_key)

    def test_if_male_NO(self):
        query_data = QueryData(
            age=24, sex=Sex.FEMALE, diagnosis=Diagnosis.objects.first()
        )
        decision_key = decision_functions.if_male(query_data=query_data)
        expected_decision_key = "NO"
        self.assertEqual(decision_key, expected_decision_key)

    def test_if_penicillin_allergy_YES(self):
        query_data = QueryData(
            age=24,
            sex=Sex.FEMALE,
            diagnosis=Diagnosis.objects.first(),
            allergy=Allergy.objects.get(name="penicillin"),
        )
        decision_key = decision_functions.if_penicillin_allergy(query_data=query_data)
        expected_decision_key = "YES"
        self.assertEqual(decision_key, expected_decision_key)

    def test_if_penicillin_allergy_NO(self):
        query_data = QueryData(
            age=24, sex=Sex.FEMALE, diagnosis=Diagnosis.objects.first()
        )
        decision_key = decision_functions.if_penicillin_allergy(query_data=query_data)
        expected_decision_key = "NO"
        self.assertEqual(decision_key, expected_decision_key)

    def test_if_in_shock_YES(self):
        query_data = QueryData(
            age=24,
            sex=Sex.FEMALE,
            diagnosis=Diagnosis.objects.first(),
            vitals=Vitals(
                heart_rate=60,
                blood_pressure=BloodPressureMeasurement(systolic=40, diastolic=20),
            ),
        )
        decision_key = decision_functions.if_in_shock(query_data=query_data)
        expected_decision_key = "YES"
        self.assertEqual(decision_key, expected_decision_key)

    def test_if_in_shock_NO(self):
        query_data = QueryData(
            age=24,
            sex=Sex.FEMALE,
            diagnosis=Diagnosis.objects.first(),
            vitals=Vitals(
                heart_rate=60,
                blood_pressure=BloodPressureMeasurement(systolic=120, diastolic=80),
            ),
        )
        decision_key = decision_functions.if_in_shock(query_data=query_data)
        expected_decision_key = "NO"
        self.assertEqual(decision_key, expected_decision_key)
