from connection import async_engine

import uuid
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, select,ForeignKey, UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy.orm import relationship, sessionmaker, declarative_base, DeclarativeBase, Mapped, mapped_column

from typing import Optional

# Base = declarative_base()
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    # id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True, index=True)
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = 'profiles'
    # id = Column(Integer, primary_key=True, index=True)
    id = Column(String, primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name:Mapped[Optional[str]]
    # Foreign Key relationship with users table
    user_id = Column(String, ForeignKey('users.id'), unique=True) 
    user = relationship("User", back_populates="profile", uselist=False)

# Create the table in the database (if it doesn't exist)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)
async def get_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()



# Create User
# user1 = User(username="jannny", email="jannny@example.com")
# user2 = User(username="smith", email="smith@example.com")

# db.add(user1)
# db.add(user2)


# # # Commit the changes to the database
# db.commit()

# # # Close the session
# db.close()

