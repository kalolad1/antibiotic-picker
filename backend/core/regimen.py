from enum import Enum
from typing import List

from django.db import models


class Drug(models.Model):
    name = models.CharField(max_length=200)


class AdministrationRoute(Enum):
    PARENTERAL = "PARENTERAL"
    ORAL = "ORAL"
    SUBLINGUAL = "SUBLINGUAL"
    IM_INJECTION = "IM_INJECTION"
    SUBCUTANEOUS = "SUBCUTANEOUS"

    READABLE_FORMAT = {
        PARENTERAL: "IV",
        ORAL: "oral",
        SUBLINGUAL: "sublingual",
        IM_INJECTION: "intramuscular injection",
        SUBCUTANEOUS: "subcutaneous",
    }

    def __str__(self) -> str:
        return AdministrationRoute.READABLE_FORMAT.value[self.name]


class DoseUnit(Enum):
    MICROGRAM = "mcg"
    MILLIGRAM = "mg"
    GRAM = "g"


class Dose:
    def __init__(self, unit: DoseUnit, value: float) -> None:
        self.unit = unit
        self.value = value

    @classmethod
    def from_string(cls, dose_as_string: str):
        """
        Converts a dose as a string into a Dose object.
        Example: "10g" -> Dose(unit=Unit.GRAM, value=10)
        """
        for unit in DoseUnit:
            if unit.value in dose_as_string:
                dose_as_string = dose_as_string.replace(unit.value, "")
                return cls(unit=unit, value=float(dose_as_string))
        raise ValueError(f"Could not parse dose from string: {dose_as_string}")

    def __str__(self) -> str:
        # If dose value is X.0, convert to X for better
        # readability
        to_str_value = ""
        if self.value == int(self.value):
            to_str_value = str(int(self.value))
        else:
            to_str_value = str(self.value)
        return f"{to_str_value}{self.unit.value}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Dose):
            return other.unit == self.unit and other.value == self.value
        return False


class Duration:
    def __init__(self, num_days: int) -> None:
        self.num_days = num_days

    def __str__(self):
        weeks = self.num_days // 7
        remainder_days = self.num_days % 7

        weeks_word = "weeks" if weeks > 1 else "week"
        days_word = "days" if remainder_days > 1 else "day"

        output_str = ""
        if weeks > 0:
            output_str += f"{weeks} {weeks_word}"
            if remainder_days > 0:
                output_str += f" and {remainder_days} {days_word}"
        else:
            output_str = f"{remainder_days} {days_word}"
        return output_str

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Duration):
            return other.num_days == self.num_days
        return False


class Frequency(Enum):
    Q1D = "Q1D"
    B1D = "B1D"
    T1D = "T1D"
    Qu1D = "Qu1D"

    Q2D = "Q2D"
    Q3D = "Q3D"
    Q1W = "Q1W"
    Q2W = "Q2W"
    Q1M = "Q1M"

    Q1H = "Q1H"
    Q2H = "Q2H"
    Q4H = "Q4H"
    Q6H = "Q6H"
    Q8H = "Q8H"
    Q12H = "Q12H"

    SINGLE_DOSE = "SINGLE_DOSE"

    EVERY_MEAL = "EVERY_MEAL"
    PRN = "PRN"

    READABLE_FORMAT = {
        Q1D: "every day",
        B1D: "twice a day",
        T1D: "three times a day",
        Qu1D: "four times a day",
        Q2D: "every two days",
        Q3D: "every three days",
        Q1W: "every week",
        Q2W: "every two weeks",
        Q1M: "every month",
        Q1H: "every hour",
        Q2H: "every 2 hours",
        Q6H: "every 6 hours",
        Q4H: "every 4 hours",
        Q8H: "every 8 hours",
        Q12H: "every 12 hours",
        SINGLE_DOSE: "single dose",
        EVERY_MEAL: "every meal",
        PRN: "as needed",
    }

    def __str__(self) -> str:
        return Frequency.READABLE_FORMAT.value[self.name]


class Prescription:
    def __init__(
        self,
        drug: Drug,
        dose: Dose,
        frequency: Frequency,
        route: AdministrationRoute,
        start_day: int,
        end_day: int,
    ):
        self.drug = drug
        self.dose = dose
        self.frequency = frequency
        self.route = route
        self.start_day = start_day
        self.end_day = end_day

    @classmethod
    def init_from_xml(cls, xml_prescription):
        return cls(
            drug=Drug.objects.get(name=xml_prescription.find("drug").text),
            dose=Dose.from_string(xml_prescription.find("dose").text),
            frequency=Frequency(xml_prescription.find("frequency").text),
            route=AdministrationRoute(xml_prescription.find("route").text),
            start_day=int(xml_prescription.find("start_day").text),
            end_day=int(xml_prescription.find("end_day").text),
        )

    def to_json(self):
        return {
            "drug": self.drug.name,
            "dose": str(self.dose),
            "frequency": str(self.frequency),
            "route": str(self.route),
            "start_day": self.start_day,
            "end_day": self.end_day,
        }

    def __str__(self):
        return (
            f"{self.drug.name} {str(self.dose)} {str(self.frequency)} "
            f"{str(self.route)} "
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, Prescription):
            for attr in other.__dict__:
                if getattr(other, attr) != getattr(self, attr):
                    print(f"NOT EQUAL: {attr}")
                    return False
        return True


class Regimen:
    def __init__(self, prescriptions: List[Prescription]):
        self.prescriptions = prescriptions

    @classmethod
    def init_from_xml(cls, xml_regimen):
        prescriptions = []
        for xml_prescription in xml_regimen:
            prescriptions.append(
                Prescription.init_from_xml(xml_prescription=xml_prescription)
            )
        return cls(prescriptions=prescriptions)

    def to_json(self):
        json = {"prescriptions": [i.to_json() for i in self.prescriptions]}
        return json

    def __str__(self):
        output = ""
        for i in self.prescriptions:
            output += str(i) + "\n"
        return output

    def __eq__(self, other) -> bool:
        if not isinstance(other, Regimen):
            return False

        if not (len(self.prescriptions) == len(other.prescriptions)):
            return False

        for index, value in enumerate(self.prescriptions):
            if value != other.prescriptions[index]:
                return False

        return True
