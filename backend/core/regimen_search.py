from .regimen import Regimen
from .query_data import QueryData


def get_regimen_from_query_data(
    query_data: QueryData,
) -> Regimen:
    return query_data.diagnosis.get_regimen(query_data=query_data)
