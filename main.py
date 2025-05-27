from utils import WebServer
from contextlib import asynccontextmanager

from routers import *


@asynccontextmanager
async def lifespan(app_: WebServer):
    # Initialize the database connection here
    app_.db = "Database connection"
    yield
    # Close the database connection here
    app_.db = None


app = WebServer()
app.include_router(base_router)
app.include_router(cookie_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="_wildcard.localhost+2-key.pem",
        ssl_certfile="_wildcard.localhost+2.pem"
    )
