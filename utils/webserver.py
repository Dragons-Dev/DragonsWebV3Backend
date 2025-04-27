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
            allow_origins=[
                "http://localhost:5173",  # deine lokale Frontend-URL
                "http://26.220.13.21:5173",  # die IP deines Freundes (ersetze mit der echten IP)
                "http://26.47.104.215:5173",  # deine eigene IP (ersetze mit deiner IP)
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
