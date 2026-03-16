from sqlalchemy import select

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import engine, GeneralInfo


def route_id_validation(route_id):
    stmt = select(GeneralInfo.id).where(GeneralInfo.id == route_id)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            if str(row) == "(UUID('" + route_id + "'),)":
                return True
            else:
                return False
        return None
