from __future__ import annotations

import os
from typing import List, TYPE_CHECKING
import xml.etree.ElementTree as ET

from django.db import models

from .regimen import Regimen
from . import path_constants
from . import decision_functions

if TYPE_CHECKING:
    from .query_data import QueryData


class Diagnosis(models.Model):
    name = models.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(Diagnosis, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"<{self.name}>"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Diagnosis):
            return self.name == other.name
        return False

    @staticmethod
    def get_supported_diagnoses() -> List[str]:
        supported_diagnoses = [diagnosis.name for diagnosis in Diagnosis.objects.all()]
        return supported_diagnoses

    def get_regimen(self, query_data: QueryData) -> Regimen:
        # TODO - Need to optimize this code so new decision tree
        # is not made for every call
        return DecisionTree(self).get_regimen(query_data=query_data)


class DecisionTree:
    def __init__(self, diagnosis: Diagnosis):
        self.diagnosis = diagnosis
        xml_file_path: str = os.path.join(
            path_constants.XML_DIAGNOSIS_DECISION_TREES_DIR, diagnosis.name + ".xml"
        )
        xml_file = ET.parse(xml_file_path)

        xml_root = xml_file.getroot()
        self.root_node: DecisionNode = DecisionNode(xml_root)
        DecisionTree.construct_tree(self.root_node, xml_root)

    @staticmethod
    def construct_tree(parent_node, parent_xml_element):
        for child_xml_element in parent_xml_element:
            if child_xml_element.tag == "decision_node":
                child_node = DecisionNode(child_xml_element)
                parent_node.add_child(child_node)
                DecisionTree.construct_tree(child_node, child_xml_element)
            elif child_xml_element.tag == "regimen_node":
                child_node = RegimenNode(child_xml_element)
                parent_node.add_child(child_node)

    def get_regimen(self, query_data: QueryData) -> Regimen:
        curr_node = self.root_node
        while not isinstance(curr_node, RegimenNode):
            decision_function = decision_functions.get_decision_function_from_label(
                curr_node.decision_function_label
            )
            next_child_decision_key = decision_function(query_data)

            for child in curr_node.children:
                if next_child_decision_key == child.decision_key:
                    curr_node = child

        return curr_node.regimen


class DecisionNode:
    def __init__(self, xml_element):
        self.decision_function_label = xml_element.get("decision_function_label")
        if "decision_key" in xml_element.attrib:
            self.decision_key = xml_element.get("decision_key")
        self.children = []

    def add_child(self, child) -> None:
        self.children.append(child)


class RegimenNode:
    def __init__(self, xml_element):
        self.decision_key = xml_element.get("decision_key")
        self.regimen = Regimen.init_from_xml(xml_regimen=xml_element)
