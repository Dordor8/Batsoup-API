import uvicorn
from fastapi import FastAPI

from src import routes
from src.routes import route

app = FastAPI()
app.include_router(route.router)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
