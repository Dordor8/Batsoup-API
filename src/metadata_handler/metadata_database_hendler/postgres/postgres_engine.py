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


class ContactDetails(Base):
    __tablename__ = "contact_details"

    id = Column(Integer, Sequence("some_id_seq", start=1), primary_key=True, nullable=False)
    general_info_id = Column(Uuid, ForeignKey('general_info.id'), nullable=False, primary_key=True)
    contact_info = Column(String)
    reliability_estimation = Column(Integer)
    description = Column(String)
    data_source = Column(String)

    general_info = relationship("GeneralInfo")






try:
    conn = engine.connect()
except:
    print("Error connecting to PostgreSQL")

Session = sessionmaker(bind=engine)
session = Session()

def create_engine():
    Base.metadata.create_all(engine)

