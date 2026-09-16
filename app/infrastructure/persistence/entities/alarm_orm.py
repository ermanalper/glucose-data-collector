import uuid

from sqlalchemy import String, Column, Integer, DateTime, UniqueConstraint, UUID, Boolean

from app.infrastructure.persistence.database import Base


class AlarmEntity(Base):
    __tablename__ = "alarms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, index=True, nullable=False, default="default_user")
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    message = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'timestamp', name='uix_alarm_timestamp'), #timestamps must be unique
    )

