import uuid
from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from main import config
from src.metadata_handler.endpoint_validation.destination_validation.sql_dastination_validation import sql_validate
from src.metadata_handler.endpoint_validation.source_validation.http_source_validation import http_validate
from src.metadata_handler.endpoint_validation.destination_validation.s3_dastination_validation import s3_validate
from src.metadata_handler.endpoint_validation.source_validation.kapka_source_validation import kapka_validate
from src.metadata_handler.metadata_database_hendler.metadata_writer.postgres.destination_data_writer.s3_data_writer import \
    s3_data_writer
from src.metadata_handler.metadata_database_hendler.metadata_writer.postgres.destination_data_writer.sql_data_writer import \
    sql_data_writer
from src.metadata_handler.metadata_database_hendler.metadata_writer.postgres.general_data_writer import write_general_data_to_database
from src.metadata_handler.metadata_database_hendler.metadata_writer.postgres.source_data_writer.http_data_writer import \
    http_data_writer
from src.metadata_handler.metadata_database_hendler.metadata_writer.postgres.source_data_writer.kapka_data_writer import \
    kapka_data_writer

router = APIRouter(
    prefix="/route",
)

class Destination(BaseModel):
    destination_type: str
    destination_connection_details: dict

@router.post("/create")
def create_route(name:str, provider:str, data_format:str, schema_mapping:dict, frequency:int, file_size:int,
                 is_one_tine_route:bool, source_type:str, source_connection_details: dict,
                 destination: list[Destination]) -> str:

    return ""

#TODO: Priority B - Do not do this for now
def source_validation(source_type:str, source_connection_details:dict) -> bool:
    the_connection_is_proper = False

    match source_type:
        case config.get('Endpoint_types', 'kapka'):
            the_connection_is_proper = kapka_validate(source_connection_details)
        case config.get('Endpoint_types', 'http'):
            the_connection_is_proper = http_validate(source_connection_details)

    return the_connection_is_proper


#TODO: Priority B - Do not do this for now
def destination_validation(destination: list[Destination]) -> bool:
    the_connection_is_proper = False
    connections = True

    for destination_details in destination:
        match destination_details.destination_type:
            case config.get('Endpoint_types', 's3'):
                the_connection_is_proper = s3_validate(destination_details.destination_connection_details)
            case config.get('Endpoint_types', 'sql'):
                the_connection_is_proper = sql_validate(destination_details.destination_connection_details)

        if the_connection_is_proper and connections == True:
            connections = True
        else:
            connections = False

    return connections


def write_source_info_to_db(fk_id, source_type, source_connection_details):
    match source_type:
        case config.get('Endpoint_types', 'kapka'):
            kapka_data_writer(fk_id, source_connection_details)
        case config.get('Endpoint_types', 'http'):
            http_data_writer(fk_id, source_connection_details)


def write_destination_info_to_db(fk_id, destination):
    for destination_details in destination:
        match destination_details.destination_type:
            case config.get('Endpoint_types', 's3'):
                s3_data_writer(fk_id, destination_details.destination_connection_details)
            case config.get('Endpoint_types', 'sql'):
                sql_data_writer(fk_id, destination_details.destination_connection_details)


def write_route_to_db(name:str, provider:str, data_format:str, schema_mapping:dict, frequency:int, file_size:int,
                      source_type:str, source_connection_details: dict, destination: list[Destination]):
    pk_id = create_pk()
    creation_time = datetime.now()
    write_general_data_to_database(pk_id, name, provider ,creation_time, data_format,
                           schema_mapping ,frequency, file_size)
    write_source_info_to_db(pk_id, source_type, source_connection_details)
    write_destination_info_to_db(pk_id, destination)


def create_pk():
    pk_id = uuid.uuid4()
    return pk_id
