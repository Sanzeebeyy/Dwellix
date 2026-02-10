from .database import Base
from sqlalchemy import Column, Integer, String ,ForeignKey, Enum, Boolean, DateTime,  UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    bio = Column(String)
    gender = Column(String)
    role = Column(Enum('seeker', 'owner', 'both', name = "user_role"))
    profile_picture_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    rooms = relationship("Room", back_populates="owner")
    applications = relationship("Application", back_populates="applicant")





class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    area = Column(String, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)
    rent = Column(Integer, nullable=False)
    deposit = Column(Integer, nullable=False)
    room_type = Column(Enum('single','shared','flat', name = 'room_type'))
    is_furnished = Column(Boolean, default=False)
    min_stay_months = Column(Integer)
    status = Column(Enum('available','occupied','hidden', name = 'room_status'), nullable=False, default='available')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    owner = relationship("User",back_populates="rooms")

    images = relationship("RoomImage", back_populates="room", cascade="all, delete")
    applications = relationship("Application", back_populates="room")





class RoomImage(Base):
    __tablename__ = "room_images"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", back_populates="images")





class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
    UniqueConstraint('room_id', 'applicant_id', name='unique_room_application'),)

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    applicant_id = Column(Integer, ForeignKey("users.id"))
    bargain_amount = Column(Integer)
    status = Column(Enum('pending','accepted','rejected', name = 'application_status'), default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    room = relationship("Room", back_populates="applications")
    applicant = relationship("User",back_populates="applications")





class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
    UniqueConstraint('user_id', 'room_id', name='unique_favorite'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())





class RoomView(Base):
    __tablename__ = "room_views"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
