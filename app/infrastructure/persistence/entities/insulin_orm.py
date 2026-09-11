from sqlalchemy import Column, Integer, String

from app.infrastructure.persistence.database import Base


class InsulinEntity(Base):
    __tablename__ = 'insulin_types'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False, default="default_user")
    type = Column(String, nullable=False)

