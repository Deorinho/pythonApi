from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy_utils import EmailType
from database import Base

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primaryKey = True, index = True)
    email = Column(EmailType)
    passwd = Column(String)
    signup_ts = Column(DateTime)

    