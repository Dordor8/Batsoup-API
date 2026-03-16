from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import engine, SqlConationData


def sql_data_writer(fk_id:UUID, destination_data: dict) -> None:
    if validate_sql_conaction_data(destination_data) and validate_sql_conaction_data_types(destination_data):
        with Session(engine) as session:
            data = SqlConationData(
                general_info_id=fk_id,
                table_name=destination_data['table_name'],
            )
            session.add(data)
            session.commit()
    else:
        raise HTTPException(status_code=400, detail="Incorrect data format: str, the required data for connect sql "
                                                    "is: table_name: str")

def validate_sql_conaction_data(destination_data: dict):
    if destination_data.get('table_name') is not None:
        return True
    else:
        return False


def validate_sql_conaction_data_types(destination_data: dict):
    if type(destination_data.get('table_name')) is str:
        return True
    else:
        return False
