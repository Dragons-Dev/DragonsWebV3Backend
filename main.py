from contextlib import asynccontextmanager
from datetime import datetime
import logging

from database.database import DataBase
from utils import WebServer
from routers import *


class IgnoreConnectionResetFilter(logging.Filter):
    def filter(self, record):  # this ignores ConnectionResetError in the log. this was implemented during development to avoid cluttering the logs with connection reset errors that are not critical.
        return record.getMessage().startswith("ConnectionResetError")
logging.getLogger("asyncio").addFilter(IgnoreConnectionResetFilter())


@asynccontextmanager
async def lifespan(app_: WebServer):
    # Initialize the database connection here
    app_.db = DataBase("sqlite+aiosqlite:///data/main.sqlite")
    # make sure the folder already exists, otherwise the database connection will fail
    await app_.db.setup(boot=datetime.now())
    yield
    # Close the database connection here
    await app_.db.close()
    app_.db = None


app = WebServer(lifespan=lifespan)
app.include_router(base_router)
app.include_router(authentication_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="_wildcard.localhost+2-key.pem",
        ssl_certfile="_wildcard.localhost+2.pem"
    )
