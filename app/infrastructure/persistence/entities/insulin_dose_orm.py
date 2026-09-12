from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, UniqueConstraint, Float
from sqlalchemy.orm import relationship

from app.infrastructure.persistence.database import Base


class InsulinDoseEntity(Base):
    __tablename__ = 'insulin_doses'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    insulin_type_id = Column(Integer, ForeignKey('insulin_types.id'), nullable=False)
    dose = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    insulin_type = relationship("InsulinEntity", lazy="joined")
    __table_args__ = (
        UniqueConstraint('user_id', 'timestamp', name='uix_insulin_doses_user_timestamp'),  # timestamps must be unique
    )