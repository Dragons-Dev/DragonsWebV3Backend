from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/v1/authentication", tags=["authentication"])


@router.post("/register")
async def register(request: Request):
    """
    Register endpoint.
    """
    return JSONResponse(status_code=200, content={"status": 200, "message": "OK"})

@router.post("/login")
async def login(request: Request, name: str = Form(...), password: str = Form(...), stay_logged_in: bool = Form(False)):
    """
    Login endpoint.
    """
    print(name)
    print(password)
    print(stay_logged_in)
    return JSONResponse(status_code=200, content={"status": 200, "message": "OK"})
