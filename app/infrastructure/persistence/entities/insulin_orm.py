from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.persistence.database import Base


class InsulinEntity(Base):
    __tablename__ = 'insulin_types'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, nullable=False)
