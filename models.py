from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, func, Date, UUID, TIMESTAMP, \
    LargeBinary
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import Session, relationship

from database import Base, SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# Tietokanta taulut, nämä luodaan automaattisesti postgresql tietokantaan


class Viewing(Base):
    __tablename__ = 'viewings'

    id = Column(Integer, primary_key=True)
    grade = Column(Integer)
    create_date = Column(Date, default=datetime.utcnow())
    what_positive = Column(Text)
    what_negative = Column(Text)
    observations = Column(Text)
    improvement_idea = Column(Text)
    photo = Column(LargeBinary, nullable=True)
    accepted = Column(Boolean, default=False)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False, unique=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(45), nullable=False, unique=True)
    password = Column(MEDIUMTEXT, nullable=False)
    roles_id = Column(ForeignKey('roles.id'), nullable=False, index=True)
    access_token_identifier = Column(String(45), nullable=True)
    refresh_token_identifier = Column(String(45), nullable=True)

    role = relationship('Role')


