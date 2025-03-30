from sqlalchemy import Table,Column, Integer, String, ForeignKey
from app.db import Base
from sqlalchemy.orm import relationship

favorites_table = Table(
    "favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("shanyrak_id", Integer, ForeignKey("shanyraks.id"))
)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    favorites = relationship(
        "Shanyrak",
        secondary=favorites_table,
        backref="favorited_by"
    )

