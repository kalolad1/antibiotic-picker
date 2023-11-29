import os

from . import decision_functions
from . import path_constants
from .diagnosis import Diagnosis, DecisionTree, RegimenNode

DECISION_FUNCTION_KEY_HEADER_MAP = {
    (decision_functions.IF_PENICILLIN_ALLERGY, "NO"): "",
    (
        decision_functions.IF_PENICILLIN_ALLERGY,
        "YES",
    ): "If the patient has a pencillin allergy",
    (decision_functions.IF_MALE, "NO"): "If the patient is female",
    (decision_functions.IF_MALE, "YES"): "If the patient is male",
    (decision_functions.IF_PREGNANT, "NO"): "",
    (decision_functions.IF_PREGNANT, "YES"): "If the patient is pregnant",
    (
        decision_functions.IF_CURB_SCORE_IS,
        "LESS_THAN_1",
    ): "If the patient's CURB-65 score is < 1",
    (
        decision_functions.IF_CURB_SCORE_IS,
        "GREATER_THAN_2",
    ): "If the patient's CURB-65 score is > 2",
    (decision_functions.IF_YES, "YES"): "",
    (decision_functions.IF_IN_SHOCK, "NO"): "",
    (decision_functions.IF_IN_SHOCK, "YES"): "If the patient is in shock",
    (decision_functions.IF_QUINOLONE_PROPHYLAXIS, "NO"): "",
    (
        decision_functions.IF_QUINOLONE_PROPHYLAXIS,
        "YES",
    ): "If the patient is on quinolone prophylaxis",
}


def get_segment_header(decision_function_label: str, decision_key: str) -> str:
    segment_header = DECISION_FUNCTION_KEY_HEADER_MAP[
        (decision_function_label, decision_key)
    ]

    if segment_header == "":
        return ""

    return f"##### {segment_header}\n"


def generate_document_segment(root_node) -> str:
    if isinstance(root_node, RegimenNode):
        return f"- {str(root_node.regimen)}"

    segment_text = ""
    for child in root_node.children:
        segment_header = get_segment_header(
            root_node.decision_function_label, child.decision_key
        )
        segment_body = generate_document_segment(child)
        segment_text += segment_header + segment_body + "\n\n"
    return segment_text + "------"


def generate_reference_document_body(diagnosis: Diagnosis) -> str:
    root_node = DecisionTree(diagnosis=diagnosis).root_node
    body = generate_document_segment(root_node)

    lines = body.splitlines()
    lines.pop()
    body = "\n".join(lines)
    return body


def generate_reference_document(diagnosis: Diagnosis) -> str:
    document_text = ""
    # Add title
    title = f"# {diagnosis.name.title()}\n\n"

    # Add body
    body = generate_reference_document_body(diagnosis=diagnosis)

    document_text = title + body
    return document_text


def generate_reference_documents():
    for diagnosis in Diagnosis.objects.all():
        reference_document_text = generate_reference_document(diagnosis=diagnosis)

        path_to_new_file = os.path.join(
            path_constants.REFERENCE_DOCUMENTS_DIR, diagnosis.name
        )
        with open(path_to_new_file, "w") as file:
            file.write(reference_document_text)
