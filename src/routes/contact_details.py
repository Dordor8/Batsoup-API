from fastapi import APIRouter

from src.metadata_handler.metadata_database_hendler.metadata_writer.postgres.contact_details_writer import \
    write_contact_details_to_database

router = APIRouter(
    prefix="/contact_details"
)

#TODO: add route_id validation
@router.post("/insert_contact_details")
def insert_contact(route_id: str, contact_info: str = 0, reliability_estimation: int = 0, description: str = 0, data_source: str = 0):
    write_contact_details_to_db(route_id, contact_info, description, reliability_estimation, data_source)


def write_contact_details_to_db(route_id:str, contact_info:str|None, description:str|None,
                                   reliability_estimation:int|None, data_source:str|None):
    write_contact_details_to_database(route_id, contact_info, description, reliability_estimation, data_source)