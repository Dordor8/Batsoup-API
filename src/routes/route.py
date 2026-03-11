import json

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/route",
)

class Destination(BaseModel):
    destination_type: str
    destination_connection_details: dict

@router.post("/create")
def create_route(name:str, description:str, provider:str, data_format:str, data_schema:dict, frequency:int, file_size:int,
                 is_one_tine_route:bool, source_type:str, source_connection_details: dict,
                 destination: list[Destination]) -> str:

    return ""