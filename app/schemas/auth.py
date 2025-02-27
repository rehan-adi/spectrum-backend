from typing import Annotated
from pydantic import BaseModel, EmailStr, constr


class Signup(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=6, max_length=10)]


class Signin(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=6, max_length=10)]
