from pydantic import BaseModel, EmailStr, PositiveInt


class User(BaseModel):
    name: str
    id: int
    age: int
    is_adult: bool = False


class UserInfo(BaseModel):
    username: str
    user_info: str


class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt
    is_subscribed: bool = False
