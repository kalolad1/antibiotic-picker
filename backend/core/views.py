import json
import os

from django.http import HttpResponse, HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import parse_handp
from . import path_constants
from .regimen_search import get_regimen_from_query_data


def dummy_home(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "This is the dummy home for the backend. Why did I keep it? It makes me feel"
        " better to have my backend have some frontend too instead of a series of"
        " disembodied REST APIs. Judith Faulkner, I'm coming for you."
    )


@api_view(["GET"])
def reference_document(request: HttpRequest, diagnosis: str) -> HttpResponse:
    # Open file according to diagnosis
    # Get markdown text and return it as response.
    path_to_file = os.path.join(path_constants.REFERENCE_DOCUMENTS_DIR, diagnosis)

    with open(path_to_file, "r") as file:
        markdown_text = file.read()

    return Response({"text": markdown_text})


@api_view(["GET", "POST", "OPTIONS"])
def regimen_search(request: HttpRequest) -> HttpResponse:
    # TODO - DELETE. Used only to get to API testing page.
    if request.method == "GET":
        return HttpResponse()

    handp: str = request.data["handp_text"]
    try:
        query_data = parse_handp.parse_handp(handp)
    except parse_handp.ParseHandpError as e:
        response_data = {"error_message": str(e)}
        return HttpResponse(
            json.dumps(response_data),
            status=400,
        )

    regimen = get_regimen_from_query_data(query_data)
    response_data = {"regimen": regimen.to_json(), "query_data": query_data.to_json()}
    return Response(response_data)
