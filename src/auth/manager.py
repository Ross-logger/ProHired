import os
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from src.auth.models import User
from src.auth.utils import get_user_db

MANAGER_SECRET = os.getenv("MANAGER_SECRET")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = MANAGER_SECRET
    verification_token_secret = MANAGER_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")



async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
