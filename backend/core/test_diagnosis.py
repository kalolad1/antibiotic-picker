from django.test import TestCase

from . import query_data
from . import test_constants
from .diagnosis import Diagnosis, DecisionTree, DecisionNode
from .regimen import (
    Regimen,
    Prescription,
    Drug,
    AdministrationRoute,
    Dose,
    Frequency,
)
from .allergy import Allergy
from .query_data import Vitals, BloodPressureMeasurement


class DiagnosisDecisionTreesTestCase(TestCase):
    fixtures = test_constants.FIXTURES

    def test_diagnosis_decision_tree_construction(self):
        decision_tree = DecisionTree(
            diagnosis=Diagnosis.objects.get(name="spontaneous bacterial peritonitis")
        )
        root_node = decision_tree.root_node
        self.assertTrue(isinstance(root_node, DecisionNode))
        self.assertEqual(len(root_node.children), 2)

    def test_get_regimen_sbp_penicillin_allergy(self):
        diagnosis = Diagnosis.objects.get(name="spontaneous bacterial peritonitis")
        query_data_instance = query_data.QueryData(
            age=25,
            sex=query_data.Sex.MALE,
            diagnosis=diagnosis,
            allergy=Allergy.objects.get(name="penicillin"),
        )
        regimen = diagnosis.get_regimen(query_data_instance)
        expected_regimen = Regimen(
            [
                Prescription(
                    drug=Drug.objects.get(name="ceftriaxone"),
                    dose=Dose.from_string("2g"),
                    frequency=Frequency.Q1D,
                    route=AdministrationRoute.PARENTERAL,
                    start_day=1,
                    end_day=7,
                )
            ]
        )
        self.assertEqual(regimen, expected_regimen)

    def test_get_regimen_sbp_no_p_allergy_no_q_proph(self):
        diagnosis = Diagnosis.objects.get(name="spontaneous bacterial peritonitis")
        query_data_instance = query_data.QueryData(
            age=25,
            sex=query_data.Sex.MALE,
            diagnosis=diagnosis,
        )
        regimen = diagnosis.get_regimen(query_data_instance)
        expected_regimen = Regimen(
            [
                Prescription(
                    drug=Drug.objects.get(name="cefotaxime"),
                    dose=Dose.from_string("1g"),
                    frequency=Frequency.Q8H,
                    route=AdministrationRoute.PARENTERAL,
                    start_day=1,
                    end_day=7,
                )
            ]
        )
        self.assertEqual(regimen, expected_regimen)

    def test_get_regimen_pyelonephritis_penicillin_allergy(self):
        diagnosis = Diagnosis.objects.get(name="pyelonephritis")
        query_data_instance = query_data.QueryData(
            age=25,
            sex=query_data.Sex.FEMALE,
            diagnosis=diagnosis,
            allergy=Allergy.objects.get(name="penicillin"),
        )
        regimen = diagnosis.get_regimen(query_data_instance)
        expected_regimen = Regimen(
            [
                Prescription(
                    drug=Drug.objects.get(name="ciprofloxacin"),
                    dose=Dose.from_string("500mg"),
                    frequency=Frequency.Q12H,
                    route=AdministrationRoute.ORAL,
                    start_day=1,
                    end_day=7,
                )
            ]
        )

        self.assertEqual(regimen, expected_regimen)

    def test_get_regimen_pyelonephritis_no_penicillin_allergy(self):
        diagnosis = Diagnosis.objects.get(name="pyelonephritis")
        query_data_instance = query_data.QueryData(
            age=25,
            sex=query_data.Sex.FEMALE,
            diagnosis=diagnosis,
            vitals=Vitals(
                heart_rate=60,
                blood_pressure=BloodPressureMeasurement(systolic=120, diastolic=80),
            ),
        )
        regimen = diagnosis.get_regimen(query_data_instance)
        expected_regimen = Regimen(
            [
                Prescription(
                    drug=Drug.objects.get(name="cefuroxime"),
                    dose=Dose.from_string("750mg"),
                    frequency=Frequency.Q8H,
                    route=AdministrationRoute.PARENTERAL,
                    start_day=1,
                    end_day=7,
                )
            ]
        )

        self.assertEqual(regimen, expected_regimen)

    def test_get_regimen_pyelonephritis_no_p_allergy_with_shock(self):
        diagnosis = Diagnosis.objects.get(name="pyelonephritis")
        query_data_instance = query_data.QueryData(
            age=25,
            sex=query_data.Sex.FEMALE,
            diagnosis=diagnosis,
            vitals=Vitals(
                heart_rate=60,
                blood_pressure=BloodPressureMeasurement(systolic=60, diastolic=40),
            ),
        )
        regimen = diagnosis.get_regimen(query_data_instance)
        prescriptions = [
            Prescription(
                drug=Drug.objects.get(name="cefuroxime"),
                dose=Dose.from_string("750mg"),
                frequency=Frequency.Q8H,
                route=AdministrationRoute.PARENTERAL,
                start_day=1,
                end_day=7,
            ),
            Prescription(
                drug=Drug.objects.get(name="gentamicin"),
                dose=Dose.from_string("1g"),
                frequency=Frequency.Q1D,
                route=AdministrationRoute.PARENTERAL,
                start_day=1,
                end_day=7,
            ),
        ]
        expected_regimen = Regimen(prescriptions=prescriptions)
        self.assertEqual(regimen, expected_regimen)
