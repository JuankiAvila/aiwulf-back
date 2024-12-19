# app/schemas/user.py
# Versión: 1.0.0

from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    email: str
    password: str
