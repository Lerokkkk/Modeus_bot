from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)

    modeus_data = relationship("ModeusData", back_populates="user")
    calendar_data = relationship("CalendarData", back_populates="user")


class ModeusData(Base):
    __tablename__ = 'modeus_data'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    user_id = Column(String, ForeignKey('users.user_id'))

    user = relationship("User", back_populates="modeus_data")


class CalendarData(Base):
    __tablename__ = 'calendar_data'

    id = Column(Integer, primary_key=True)
    calendar_id = Column(String)
    user_id = Column(String, ForeignKey('users.user_id'))

    user = relationship("User", back_populates="calendar_data")
