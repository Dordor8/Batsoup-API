import configparser

import uvicorn
from fastapi import FastAPI

from src.routes import route

app = FastAPI()
app.include_router(route.router)

config = configparser.ConfigParser()
config.read("config.ini")

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
