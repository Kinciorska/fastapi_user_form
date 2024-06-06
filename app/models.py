from sqlalchemy import Column, Integer, String

from .database import Base


class UserInfo(Base):
    __tablename__ = "userinfos"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
