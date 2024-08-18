import jwt
from src.config import JWT_SECRET
from fastapi import FastAPI, Depends, HTTPException, Request, Cookie
from src import crud


async def get_user_id_from_cookies(usersAuth: str = Cookie(None)) -> int:
    if not usersAuth:
        raise HTTPException(status_code=403, detail="Not authenticated")
    try:
        payload = jwt.decode(usersAuth, JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        return int(user_id)

    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
