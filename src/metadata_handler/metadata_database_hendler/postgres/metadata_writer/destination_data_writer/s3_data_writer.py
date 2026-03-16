from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import engine, S3ConactionData


def s3_data_writer(fk_id:UUID, destination_data: dict):
    if validate_s3_conaction_data(destination_data) and validate_s3_conaction_data_types(destination_data):
        with Session(engine) as session:
            data = S3ConactionData(
                general_info_id=fk_id,
                access_key_id=destination_data['access_key_id'],
                access_secret_key=destination_data['access_secret_key'],
                bucket_name=destination_data['bucket_name'],
                group_name=destination_data['group_name'],
                prefix=destination_data['prefix']
            )
            session.add(data)
            session.commit()
    else:
        raise HTTPException(status_code=400, detail="Incorrect data format, the required data for connect s3 is:" \
                                                    + "access_key_id: str, access_secret_key: str, bucket_name: str, "
                                                      "group_name: str, prefix: str")


def validate_s3_conaction_data(destination_data: dict):
    if destination_data.get('access_key_id') is not None and destination_data.get('access_secret_key') is not None and \
            destination_data.get('bucket_name') is not None and destination_data.get('group_name') is not None and \
            destination_data.get('prefix') is not None:
        return True
    else:
        return False


def validate_s3_conaction_data_types(destination_data: dict):
    if type(destination_data.get('access_key_id')) is str and type(destination_data.get('access_secret_key'))\
            is str and type(destination_data.get('bucket_name')) is str and\
            type(destination_data.get('group_name')) is str and\
            type(destination_data.get('prefix')) is str:
        return True
    else:
        return False
