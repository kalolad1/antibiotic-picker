from __future__ import annotations
from typing import Dict, Callable, TYPE_CHECKING

from .query_data import Sex
from .allergy import Allergy

if TYPE_CHECKING:
    from .query_data import QueryData


# Decision functions
def if_male(query_data: QueryData) -> str:
    if query_data.sex == Sex.MALE:
        return "YES"
    else:
        return "NO"


def if_penicillin_allergy(query_data: QueryData) -> str:
    if query_data.allergy is None:
        return "NO"

    if query_data.allergy == Allergy.objects.get(name="penicillin"):
        return "YES"
    else:
        return "NO"


def if_quinolone_prophylaxis(query_data: QueryData) -> str:
    # TODO - implement actual logic by including prophylaxis in query data.
    # Used in SBP decision tree.
    return "NO"


def if_in_shock(query_data: QueryData) -> str:
    assert query_data.vitals is not None
    assert query_data.vitals.blood_pressure is not None

    blood_pressure = query_data.vitals.blood_pressure
    if blood_pressure is not None and blood_pressure.is_in_shock():
        return "YES"

    return "NO"


def if_pregnant(query_data: QueryData) -> str:
    # TODO - implement actual logic by pregnancy status in query data.
    # Used in chlamydia treatment to determine antibiotic.
    return "NO"


def if_curb_score_is(query_data: QueryData) -> str:
    # TODO - implement actual logic by determining CURB score.
    # return GREATER_THAN_2
    return "LESS_THAN_1"


def if_yes(query_data: QueryData) -> str:
    # Placeholder function for those regimen decision trees
    # that have depth=1 and therefore do not branch.
    return "YES"


# Decision functions
IF_MALE = "IF_MALE"
IF_PENICILLIN_ALLERGY = "IF_PENICILLIN_ALLERGY"
IF_QUINOLONE_PROPHYLAXIS = "IF_QUINOLONE_PROPHYLAXIS"
IF_IN_SHOCK = "IF_IN_SHOCK"
IF_PREGNANT = "IF_PREGNANT"
IF_YES = "IF_YES"
IF_CURB_SCORE_IS = "IF_CURB_SCORE_IS"
decision_function_mapping: Dict[str, Callable[[QueryData], str]] = {
    IF_MALE: if_male,
    IF_PENICILLIN_ALLERGY: if_penicillin_allergy,
    IF_QUINOLONE_PROPHYLAXIS: if_quinolone_prophylaxis,
    IF_IN_SHOCK: if_in_shock,
    IF_PREGNANT: if_pregnant,
    IF_YES: if_yes,
    IF_CURB_SCORE_IS: if_curb_score_is,
}


def get_decision_function_from_label(
    decision_function_label: str,
) -> Callable[[QueryData], str]:
    return decision_function_mapping[decision_function_label]
