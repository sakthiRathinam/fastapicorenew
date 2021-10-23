from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.security import APIKeyCookie
from starlette.responses import Response, HTMLResponse
from starlette import status
from jose import jwt


app = FastAPI()

cookie_sec = APIKeyCookie(name="session")

secret_key = "someactualsecret"

users = {"dmontagu": {"password": "secret1"},
         "tiangolo": {"password": "secret2"}}


def get_current_user(session: str = Depends(cookie_sec)):
    try:
        payload = jwt.decode(session, secret_key)
        user = users[payload["sub"]]
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication"
        )


@app.get("/login")
def login_page():
    return HTMLResponse(
        """
        <form action="/login" method="post">
        Username: <input type="text" name="username" required>
        <br>
        Password: <input type="password" name="password" required>
        <input type="submit" value="Login">
        </form>
        """
    )


@app.post("/login")
def login(response: Response, username: str = Form(...), password: str = Form(...)):
    if username not in users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user or password"
        )
    db_password = users[username]["password"]
    if not password == db_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user or password"
        )
    token = jwt.encode({"sub": username}, secret_key)
    response.set_cookie("session", token)
    return {"ok": True}


@app.get("/private")
def read_private(username: str = Depends(get_current_user)):
    return {"username": username, "private": "get some private data"}
