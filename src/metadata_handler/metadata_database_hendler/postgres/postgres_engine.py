from sqlalchemy import MetaData, create_engine, Column, Integer, String, Uuid, ForeignKey, DateTime, Sequence
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm.session import sessionmaker

postgres_db_url = "postgresql://postgres:postgres@localhost/metadata"

meta_data = MetaData()

engine = create_engine(postgres_db_url, echo=False)

Base = declarative_base()


class GeneralInfo(Base):
    __tablename__ = "general_info"
    id = Column(Uuid, primary_key=True, nullable=False)
    name = Column(String)
    provider = Column(String)
    creation_time = Column(DateTime)
    data_format = Column(String)
    schema_mapping = Column(JSONB)
    frequency = Column(Integer)
    file_size = Column(Integer)

    contact_details = relationship("ContactDetails", backref="GeneralInfo")
    sql_conation_data = relationship("SqlConationData", backref="GeneralInfo")
    kapka_conaction_data = relationship("KapkaConactionData", backref="GeneralInfo")
    s3_conaction_data = relationship("S3ConactionData", backref="GeneralInfo")


class ContactDetails(Base):
    __tablename__ = "contact_details"

    id = Column(Integer, Sequence("id", start=1), primary_key=True, nullable=False)
    general_info_id = Column(Uuid, ForeignKey('general_info.id'), unique=True, nullable=False)
    contact_info = Column(String)
    reliability_estimation = Column(Integer)
    description = Column(String)
    data_source = Column(String)

    general_info = relationship("GeneralInfo")


class SqlConationData(Base):
    __tablename__ = "sql_conation_data"
    id = Column(Integer, Sequence("id_seq", start=1), primary_key=True, nullable=False)
    general_info_id = Column(Uuid, ForeignKey('general_info.id'), nullable=False)
    table_name = Column(String)

    general_info = relationship("GeneralInfo")


class KapkaConactionData(Base):
    __tablename__ = "kapka_conaction_data"
    id = Column(Integer, Sequence("some_id", start=1), primary_key=True, nullable=False)
    general_info_id = Column(Uuid, ForeignKey('general_info.id'), nullable=False)
    topic = Column(String)
    bootstrap_server = Column(String)
    group_id = Column(String)
    inactive_time_ms = Column(Integer)

    general_info = relationship("GeneralInfo")


class S3ConactionData(Base):
    __tablename__ = "s3_conaction_data"
    id = Column(Integer, Sequence("id_sequence", start=1), primary_key=True, nullable=False)
    general_info_id = Column(Uuid, ForeignKey('general_info.id'), nullable=False)
    access_key_id = Column(String)
    access_secret_key = Column(String)
    bucket_name = Column(String)
    group_name = Column(String)
    prefix = Column(String)

    general_info = relationship("GeneralInfo")


try:
    conn = engine.connect()
except:
    print("Error connecting to PostgreSQL")

def create_engine():
    Base.metadata.create_all(engine)

