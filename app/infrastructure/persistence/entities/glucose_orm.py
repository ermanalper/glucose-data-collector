from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from app.infrastructure.persistence.database import Base


class GlucoseEntity(Base):
    __tablename__ = "glucose_readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False, default="default_user")

    value = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    trend = Column(String, nullable=False)
    source = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'timestamp', name='uix_user_timestamp'), #timestamps must be unique
    )