from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from src.metadata_handler.metadata_database_hendler.postgres.metadata_reader.contact_details_reader import \
    read_contact_details_to_database, unique_id_validate
from src.metadata_handler.metadata_database_hendler.postgres.metadata_reader.general_data_reader import \
    route_id_validation
from src.metadata_handler.metadata_database_hendler.postgres.metadata_writer.contact_details_writer import \
    write_contact_details_to_database

router = APIRouter(
    prefix="/contact_details"
)

@router.post("/insert_contact_details")
def insert_contact(route_id: str, contact_info: str = 0, reliability_estimation: int = 0, description: str = 0, data_source: str = 0):
    if route_id_validation(route_id) and unique_id_validate(route_id):
        write_contact_details_to_db(route_id, contact_info, description, reliability_estimation, data_source)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid route_id")


def write_contact_details_to_db(route_id:str, contact_info:str|None, description:str|None,
                                   reliability_estimation:int|None, data_source:str|None):
    return write_contact_details_to_database(route_id, contact_info, description, reliability_estimation, data_source)


@router.get("/get_contact_details")
def get_contact(route_id: str):
    return read_contact_details_to_database(route_id)