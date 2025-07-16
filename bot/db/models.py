from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, Float, ForeignKey, text, BigInteger, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    user_tg_id = Column(BigInteger, index=True, nullable=False, unique=True)
    user_tg_login = Column(String(255), nullable=False)


class Application(Base):
    __tablename__ = 'applications'

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)  
    username_app = Column(String(255), nullable=False)
    house_chosen = Column(String(255), nullable=False)
    house_square = Column(String(255), nullable=False)
    plot = Column(String(255), nullable=False)
    budget = Column(String(255), nullable=False)
    temp = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=False)
    status = Column(Enum("new", "accepted", "completed", name = "application_status"), nullable=False)
    registration_time = Column(DateTime,default=text("CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow'"), nullable=False)  
