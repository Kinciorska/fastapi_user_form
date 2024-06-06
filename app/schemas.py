from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone: str
    email: str


class UserInfoCreate(UserInfoBase):
    password: str


class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True
