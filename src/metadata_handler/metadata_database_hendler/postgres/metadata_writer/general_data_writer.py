from datetime import datetime
from uuid import UUID

import json

from sqlalchemy.orm.session import Session

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import engine, GeneralInfo


def write_general_data_to_database(pk_id:UUID, name:str, provider: str,creation_time:datetime, data_format: str,
                           schema_mapping ,frequency:int, file_size:int):
    with Session(engine) as session:
        data = GeneralInfo(
            id=pk_id,
            name=name,
            provider=provider,
            creation_time=creation_time,
            data_format=data_format,
            schema_mapping=schema_mapping,
            frequency=frequency,
            file_size=file_size
        )
        session.add(data)
        session.commit()