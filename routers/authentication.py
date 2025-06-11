from uuid import uuid4
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
import bcrypt

from database import DBCookie, Authentication
from utils import WebServer

router = APIRouter(prefix="/api/v1/authentication", tags=["authentication"])


def gen_salt():
    return bcrypt.gensalt().decode("utf-8")


def hash_password(password: str, salt: str):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt.encode("utf-8"))
    return hashed_password.decode("utf-8")


async def async_hash_password(password: str, salt: str | None = None):
    if salt is None:
        salt = await run_in_threadpool(gen_salt)
    hashed_password = await run_in_threadpool(hash_password, password, salt)
    return hashed_password, salt


@router.post("/register")
async def register(request: Request, mail: str = Form(...), name: str = Form(...), password: str = Form(...)):
    """
    Register endpoint.
    """
    app: WebServer = request.app
    mail_auth = await app.db.get_authentication(mail)
    name_auth = await app.db.get_authentication(name)
    if name_auth is not None:
        return JSONResponse(status_code=409, content={"status": 409, "message": "User already exists."})
    if mail_auth is not None:
        return JSONResponse(status_code=409, content={"status": 409, "message": "Email already registered."})
    hashed_password, salt = await async_hash_password(password)
    auth = Authentication(
        name = name,
        mail = mail,
        salt = salt,
        password = hashed_password
    )
    await app.db.insert_authentication(auth)
    res = JSONResponse(status_code=200, content={"status": 200, "message": "OK"})
    cookie_value = uuid4().__str__()
    res.set_cookie(
        key="session",
        value=cookie_value,
        httponly=True,
        expires=datetime.now(tz=timezone.utc) + timedelta(days=1),
    )
    await app.db.insert_cookie(
        DBCookie(
            name="session",
            value=cookie_value,
            expires=datetime.now(tz=timezone.utc) + timedelta(days=1)
        )
    )
    return res

@router.post("/login")
async def login(request: Request, name: str = Form(...), password: str = Form(...), stay_logged_in: bool = Form(False)):
    """
    Login endpoint.
    """
    app: WebServer = request.app
    auth = await app.db.get_authentication(name)
    pw, _ = await async_hash_password(password, auth.salt)
    if auth is None or (pw != auth.password):
        return JSONResponse(status_code=404, content={"status": 404, "message": "Invalid login details."})
    res = JSONResponse(status_code=200, content={"status": 200, "message": "OK"})
    cookie_value = uuid4().__str__()
    if stay_logged_in:
        await app.db.insert_cookie(
            DBCookie(
                name="session",
                value=cookie_value,
                expires=datetime.now(tz=timezone.utc) + timedelta(days=30)
            )
        )
        res.set_cookie(
            key="session",
            value=cookie_value,
            httponly=True,
            expires=datetime.now(tz=timezone.utc) + timedelta(days=30),
        )
    else:
        await app.db.insert_cookie(
            DBCookie(
                name="session",
                value=cookie_value,
                expires=datetime.now(tz=timezone.utc) + timedelta(hours=24)
            )
        )
        res.set_cookie(
            key="session",
            value=cookie_value,
            httponly=True
        )
    return res

@router.post("/logout")
async def logout(request: Request):
    """
    Logout endpoint.
    """
    app: WebServer = request.app
    session_cookie = request.cookies.get("session")
    if session_cookie:
        await app.db.delete_cookie("session", session_cookie)
        res = JSONResponse(status_code=200, content={"status": 200, "message": "OK"})
        res.delete_cookie("session")
        return res
    return JSONResponse(status_code=404, content={"status": 404, "message": "No active session found."})
