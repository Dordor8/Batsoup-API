import uvicorn
from fastapi import FastAPI

from src.metadata_handler.metadata_database_hendler.postgres.postgres_engine import create_engine
from src.routes import route, contact_details

app = FastAPI()
app.include_router(route.router)
app.include_router(contact_details.router)

def main():
    create_engine()
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()
