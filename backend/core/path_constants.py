import os
from pathlib import Path


CORE_PARENT_PATH = Path(__file__).parent

PATH_TO_HANDP_SAMPLES_DIR = os.path.join(CORE_PARENT_PATH, "test_data/handp_samples")
XML_DIAGNOSIS_DECISION_TREES_DIR = os.path.join(
    CORE_PARENT_PATH, "xml_diagnosis_decision_trees"
)
REFERENCE_DOCUMENTS_DIR = os.path.join(CORE_PARENT_PATH, "reference_documents")
