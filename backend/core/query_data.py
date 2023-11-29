from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from enum import Enum

from .allergy import Allergy

if TYPE_CHECKING:
    from .diagnosis import Diagnosis


class Sex(Enum):
    MALE = "male"
    FEMALE = "female"


class BloodPressureMeasurement:
    def __init__(self, systolic: int, diastolic: int) -> None:
        self.systolic = systolic
        self.diastolic = diastolic

    def is_in_shock(self) -> bool:
        return self.systolic < 90


class Vitals:
    def __init__(
        self,
        heart_rate: Optional[int] = None,
        blood_pressure: Optional[BloodPressureMeasurement] = None,
    ) -> None:
        self.heart_rate = heart_rate
        self.blood_pressure = blood_pressure

    def to_json(self):
        return {
            "heart_rate": self.heart_rate,
            "blood_pressure": {
                "systolic": self.blood_pressure.systolic,
                "diastolic": self.blood_pressure.diastolic,
            },
        }


class QueryData:
    def __init__(
        self,
        age: int,
        sex: Sex,
        diagnosis: Diagnosis,
        allergy: Optional[Allergy] = None,
        vitals: Optional[Vitals] = None,
    ):
        if age < 0 or age > 200:
            raise ValueError(f"{age} is not a valid age!")
        self.age = age
        self.sex = sex
        self.diagnosis = diagnosis
        self.allergy = allergy
        self.vitals = vitals

    def __str__(self) -> str:
        return f"{self.age} {self.sex.value} {self.diagnosis.name} {self.allergy}"

    def to_json(self):
        json_data = {
            "age": self.age,
            "sex": self.sex.value,
            "diagnosis": self.diagnosis.name,
        }
        if self.allergy:
            json_data["allergy"] = self.allergy.name

        if self.vitals:
            json_data["vitals"] = self.vitals.to_json()

        return json_data
