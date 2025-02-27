from app.db.db import prisma
from app.schemas.auth import Signup
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException

auth_router = APIRouter()


@auth_router.post("/signup")
async def signin(data: Signup):

    email = data.email
    password = data.password

    existing_user = await prisma.user.find_first(where={"email": email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    hash_password = pwd_context.hash(password)

    try:
        await prisma.user.create(
            data={
                "email": email,
                "password": hash_password,
            }
        )
        raise HTTPException(status_code=201, detail="User created")
    except Exception as e:
        print(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
