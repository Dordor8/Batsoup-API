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
                topic=source_connection_details['TOPIC'],
                bootstrap_server=source_connection_details['BOOTSTRAP_SERVERS'],
                group_id=source_connection_details['GROUP_ID'],
                messages_amount=source_connection_details['MESSAGES_AMOUNT']
            )
            session.add(data)
            session.commit()
    else:
        raise HTTPException(status_code=400, detail="Incorrect data format, the required data for connect kapka is:" \
                                                    + "TOPIC: str, BOOTSTRAP_SERVERS: str, GROUP_ID: str, "
                                                      "MESSAGES_AMOUNT: integer")


def validate_kapka_conaction_data(source_connection_details: dict):
    if source_connection_details.get('TOPIC') is not None and source_connection_details.get('BOOTSTRAP_SERVERS')\
            is not None and source_connection_details.get('GROUP_ID') is not None and \
            source_connection_details.get('MESSAGES_AMOUNT') is not None:
        return True
    else:
        return False


def validate_kapka_conaction_data_types(source_connection_details: dict):
    if type(source_connection_details.get('TOPIC')) is str and type(source_connection_details.get('BOOTSTRAP_SERVERS'))\
            is str and type(source_connection_details.get('GROUP_ID')) is str and\
            type(source_connection_details.get('MESSAGES_AMOUNT')) is int:
        return True
    else:
        return False
