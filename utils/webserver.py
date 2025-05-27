import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.requests import Request
from fastapi.responses import Response


class SuppressConnectionResetMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ConnectionResetError:
            # Logge nur minimal oder ignoriere komplett
            logging.warning("Verbindung vom Client abgebrochen (ConnectionResetError).")
            return Response(status_code=499)  # 499 = Client Closed Request (nicht offiziell, aber gängig)
        except Exception as e:
            raise e


class WebServer(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = None
        self.boot_time = datetime.now()
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.add_middleware(SuppressConnectionResetMiddleware)
