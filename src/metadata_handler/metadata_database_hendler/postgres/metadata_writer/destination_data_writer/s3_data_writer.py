from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import engine, S3ConactionData


def s3_data_writer(fk_id:UUID, destination_data: dict):
    if validate_s3_conaction_data(destination_data) and validate_s3_conaction_data_types(destination_data):
        with Session(engine) as session:
            data = S3ConactionData(
                general_info_id=fk_id,
                access_key_id=destination_data['ACCESS_KEY'],
                access_secret_key=destination_data['SECRET_ACCESS'],
                bucket_name=destination_data['BUCKET_NAME'],
                group_name=destination_data['GROUP_NAME'],
                prefix=destination_data['S3_PREFIX']
            )
            session.add(data)
            session.commit()
    else:
        raise HTTPException(status_code=400, detail="Incorrect data format, the required data for connect s3 is:" \
                                                    + "ACCESS_KEY: str, SECRET_ACCESS: str, BUCKET_NAME: str, "
                                                      "GROUP_NAME: str, S3_PREFIX: str")


def validate_s3_conaction_data(destination_data: dict):
    if destination_data.get('ACCESS_KEY') is not None and destination_data.get('SECRET_ACCESS') is not None and \
            destination_data.get('BUCKET_NAME') is not None and destination_data.get('GROUP_NAME') is not None and \
            destination_data.get('S3_PREFIX') is not None:
        return True
    else:
        return False


def validate_s3_conaction_data_types(destination_data: dict):
    if type(destination_data.get('ACCESS_KEY')) is str and type(destination_data.get('SECRET_ACCESS'))\
            is str and type(destination_data.get('BUCKET_NAME')) is str and\
            type(destination_data.get('GROUP_NAME')) is str and\
            type(destination_data.get('S3_PREFIX')) is str:
        return True
    else:
        return False
