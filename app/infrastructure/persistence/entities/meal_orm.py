from sqlalchemy import Integer, Column, String, DateTime, UniqueConstraint

from app.infrastructure.persistence.database import Base


class MealEntity(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    glucose_value = Column(Integer)
    desc = Column(String)
    __table_args__ = (
        UniqueConstraint('user_id', 'timestamp', name='uix_meal_timestamp'),  # timestamps must be unique
    )
