from datetime import timedelta

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from orjson import loads

from models import BaseCookie, ValuedCookie, TimedCookie, FullCookie, ResponseCookie

router = APIRouter(prefix="/api/v1", tags=["cookies"])

@router.get("/get_cookies", response_model=ResponseCookie)
async def get_cookies(request: Request):
    """
    Get all cookies from the request.
    """
    cookies = request.cookies
    print(cookies)
    return JSONResponse(status_code=200, content={"message": "Get Cookies", "data": cookies})

@router.post("/set_cookie")
async def set_cookie(request: Request, data: FullCookie):
    """
    Set a cookie in the response.
    """
    response = JSONResponse(status_code=200, content={"message": "Set Cookie", "data": loads(data.model_dump_json())})

    response.set_cookie(
        key=data.name,            # Name
        value=data.value,         # Payload
        httponly=True,            # kein JS-Zugriff
        secure=True,             # in Prod: True (nur HTTPS)
        samesite="none",           # oder "strict"/"none"
        expires=data.expires + timedelta(days=30),     # Lebensdauer in Sekunden
    )
    return response

@router.post("/edit_cookie")
async def edit_cookie(request: Request, data: ValuedCookie | TimedCookie):
    """
    Edits a cookie in the response.
    """
    response = JSONResponse(status_code=200, content={"message": "Edit Cookie", "data": loads(data.model_dump_json())})
    cookie = request.cookies[data.name]
    if type(cookie) is TimedCookie:
        response.set_cookie(
            key=data.name,  # Name
            value=cookie,  # Payload
            httponly=True,  # kein JS-Zugriff
            secure=True,  # in Prod: True (nur HTTPS)
            samesite="none",  # oder "strict"/"none"
            expires=(data.expires + timedelta(days=30)),  # Lebensdauer in Sekunden
        )
    else:
        response.set_cookie(
            key=data.name,  # Name
            value=data.value,  # Payload
            httponly=True,  # kein JS-Zugriff
            secure=True,  # in Prod: True (nur HTTPS)
            samesite="none",  # oder "strict"/"none"
        )
    return response

@router.delete("/delete_cookie")
async def delete_cookie(data: BaseCookie):
    """
    Deletes a cookie in the response.
    """
    response = JSONResponse(status_code=200, content={"message": "Delete Cookie", "data": loads(data.model_dump_json())})
    response.delete_cookie(
        key=data.name,            # Name
        httponly=True,            # kein JS-Zugriff
        secure=True,             # in Prod: True (nur HTTPS)
        samesite="none",           # oder "strict"/"none"
    )
    return response
