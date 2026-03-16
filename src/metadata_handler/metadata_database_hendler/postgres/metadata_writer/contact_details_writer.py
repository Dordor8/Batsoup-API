from sqlalchemy.orm.session import Session

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import engine, ContactDetails


def write_contact_details_to_database(route_id:str, contact_info:str|None, description:str|None,
                                   reliability_estimation:int|None, data_source:str|None):
    with Session(engine) as session:
        data = ContactDetails(
            general_info_id=route_id,
            contact_info=contact_info,
            reliability_estimation=reliability_estimation,
            description=description,
            data_source=data_source
        )
        session.add(data)
        session.commit()
