import pandas as pd
from sqlalchemy import select

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import engine, ContactDetails
from src.routes import contact_details


def read_contact_details_to_database(route_id:str):
    data = ""
    stmt = select(ContactDetails).where(ContactDetails.general_info_id == route_id)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            data += str(row) + "/n"
    return data