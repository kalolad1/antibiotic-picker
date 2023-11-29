from typing import List


# Base prompts
PRESENTING_HANDP_PREFACE_PROMPT = "Here is the history and physical: \n"
INSTRUCTIONS_PROMPT = (
    "Please answer questions based on the information in the provided "
    "history and physical. "
)
NO_ACRONYMS_PROMPT = (
    "For the rest of the conversation, do not provide acronyms in the answers. "
)
IF_UNSURE_RETURN_NEG_1_PROMPT = (
    "If the information is not present in the history and physical, please "
    "return the output as '-1'."
)
OUTPUT_FORMAT_PROMPT = (
    "Only respond in this output format, words in <> are "
    "to be replaced with the content it describes. Do not include any "
    "supplementary words or parenthetical additions. Do not include "
    "introductory phases such as 'the diagnosis of the patient is'."
)
ONLY_OUTPUT_NUMBER_PROMPT = "Only output the number."


def get_prompt_for_element(element: str) -> str:
    output_prompt = f"<{element}>"
    return (
        GET_ELEMENT_PROMPTS[element]
        + OUTPUT_FORMAT_PROMPT
        + IF_UNSURE_RETURN_NEG_1_PROMPT
        + output_prompt
    )


def generate_is_supported_prompt(element: str, options: List[str]) -> str:
    options_as_str = ", ".join(f"{option}" for option in options)
    is_supported_prompt = (
        f"Is the previous {element} the same as any of the {element}'s in the following"
        f" list: \nLIST: [{options_as_str}]\nReply 'yes' or 'no'. If you are not"
        " confident in your answer, reply 'no'."
    )
    return is_supported_prompt


def generate_which_element_is_the_same_prompt(element: str, options: List[str]) -> str:
    options_as_str = ", ".join(f"{option}" for option in options)
    which_element_is_same_prompt = (
        f"What {element} in following list is the same? Only provide the EXACT"
        f" {element} from the list as a word or short phrase with no additions or "
        " acronyms. \n"
        f"LIST: [{options_as_str}] \n"
    )
    return which_element_is_same_prompt


# Attribute specific prompts
# Age
GET_AGE_PROMPT = "What is the age in years of the patient? "

# Sex
GET_SEX_PROMPT = "What is the sex of the patient? "

# Diagnosis
GET_DIAGNOSIS_PROMPT = "What is the diagnosis of the patient? "

# Allergy
GET_ALLERGY_PROMPT = "What allergy does the patient have? "

GET_ELEMENT_PROMPTS = {
    "age": GET_AGE_PROMPT,
    "sex": GET_SEX_PROMPT,
    "diagnosis": GET_DIAGNOSIS_PROMPT,
    "allergy": GET_ALLERGY_PROMPT,
}
