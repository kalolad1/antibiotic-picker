import os
import llm
import re
from typing import List, Optional

from . import query_data
from . import parse_handp_prompts
from .query_data import Allergy
from .diagnosis import Diagnosis


# The temperature controls the creativeness of the model outputs.
# Since we want deterministic, consistent answers, we have set
# the temperature to a low value.
MODEL_TEMPERATURE = 1
MODEL_TOP_P = 0.2
MODEL = llm.get_model("gpt-3.5-turbo")
MODEL.key = os.environ.get("OPENAI_SECRET_API_KEY")


class ParseHandpError(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class ConversationWrapper:
    def __init__(self, conversation) -> None:
        self.conversation = conversation

    def get_response(self, prompt: str) -> str:
        response = self.conversation.prompt(
            prompt, temperature=MODEL_TEMPERATURE, top_p=MODEL_TOP_P
        )
        response = response.text().lower()

        # Remove any parenthetical additions, like
        # "spontaneous bacterial peritonitis (sbp)"
        parenthetical_addition_pattern = r"\([^)]*\)"
        response = re.sub(parenthetical_addition_pattern, "", response)

        response = response.rstrip()
        return response


def set_up_task(handp: str):
    conversation = ConversationWrapper(MODEL.conversation())
    conversation.get_response(parse_handp_prompts.INSTRUCTIONS_PROMPT)
    conversation.get_response(
        parse_handp_prompts.PRESENTING_HANDP_PREFACE_PROMPT + handp
    )
    return conversation


def is_element_supported(
    conversation: ConversationWrapper, element: str, options: List[str]
) -> bool:
    is_supported_prompt = parse_handp_prompts.generate_is_supported_prompt(
        element, options
    )
    return conversation.get_response(is_supported_prompt) == "yes"


def get_query_data_element_value(
    conversation: ConversationWrapper,
    element: str,
    options: Optional[List[str]] = None,
    required: bool = False,
):
    prompt = parse_handp_prompts.get_prompt_for_element(element)
    element_value = conversation.get_response(prompt)

    if element_value == "-1":
        if required:
            raise ParseHandpError(
                message=f"The patient's {element} is not found in h and p"
            )
        else:
            return None

    if options is None:
        return element_value

    if is_element_supported(conversation, element, options):
        if element not in options:
            which_element_is_the_same_prompt = (
                parse_handp_prompts.generate_which_element_is_the_same_prompt(
                    prompt, options
                )
            )
            supported_element_format = conversation.get_response(
                which_element_is_the_same_prompt
            )
            element = supported_element_format
    else:
        if required:
            raise ParseHandpError(
                message=(
                    f"The following element val is not supported - {element}:"
                    f" {element_value}"
                )
            )
        else:
            return None
    return element


def convert_element_to_enum(element_value, EnumClass):
    try:
        element = EnumClass(element_value)
    except ValueError:
        raise ValueError(f"{element_value} is not a valid {EnumClass}")
    return element


def parse_handp(handp):
    conversation = set_up_task(handp)
    age = get_query_data_element_value(conversation, "age", required=True)
    sex = get_query_data_element_value(
        conversation, "sex", ["male", "female"], required=True
    )

    diagnosis = get_query_data_element_value(
        conversation=conversation,
        element="diagnosis",
        options=Diagnosis.get_supported_diagnoses(),
        required=True,
    )
    allergy = get_query_data_element_value(
        conversation=conversation,
        element="allergy",
        options=query_data.Allergy.get_supported_allergies(),
    )

    sex = convert_element_to_enum(sex, query_data.Sex)
    allergy = Allergy.objects.get(name=allergy) if allergy is not None else None
    diagnosis = Diagnosis.objects.get(name=diagnosis)

    return query_data.QueryData(
        age=int(age), sex=sex, diagnosis=diagnosis, allergy=allergy
    )
