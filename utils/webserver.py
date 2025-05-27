from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
