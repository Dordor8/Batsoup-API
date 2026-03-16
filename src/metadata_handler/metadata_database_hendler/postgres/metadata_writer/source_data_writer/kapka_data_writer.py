from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import KapkaConactionData, engine


def kapka_data_writer(fk_id:UUID, source_connection_details: dict):
    if validate_kapka_conaction_data(source_connection_details) and validate_kapka_conaction_data_types(source_connection_details):
        with Session(engine) as session:
            data = KapkaConactionData(
                general_info_id=fk_id,
                topic=source_connection_details['topic'],
                bootstrap_server=source_connection_details['bootstrap_server'],
                group_id=source_connection_details['group_id'],
                inactive_time_ms=source_connection_details['inactive_time_ms']
            )
            session.add(data)
            session.commit()
    else:
        raise HTTPException(status_code=400, detail="Incorrect data format, the required data for connect kapka is:" \
                                                    + "topic: str, bootstrap_server: str, group_id: str, "
                                                      "inactive_time_ms: integer")


def validate_kapka_conaction_data(source_connection_details: dict):
    if source_connection_details.get('topic') is not None and source_connection_details.get('bootstrap_server')\
            is not None and source_connection_details.get('group_id') is not None and \
            source_connection_details.get('inactive_time_ms') is not None:
        return True
    else:
        return False


def validate_kapka_conaction_data_types(source_connection_details: dict):
    if type(source_connection_details.get('topic')) is str and type(source_connection_details.get('bootstrap_server'))\
            is str and type(source_connection_details.get('group_id')) is str and\
            type(source_connection_details.get('inactive_time_ms')) is int:
        return True
    else:
        return False
