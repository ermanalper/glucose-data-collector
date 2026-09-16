from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import DatabaseError, AlarmAlreadyActiveException, MissingArgumentException
from app.infrastructure.interfaces.alarm_repository_interface import IAlarmRepository
from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.entities.alarm_orm import AlarmEntity
from app.models.alarm import Alarm


class AlarmRepositoryImpl(IAlarmRepository):
    def reset_alarm(self, alarm_id: UUID):
        if not alarm_id:
            raise MissingArgumentException("Alarm ID is missing")
        with SessionLocal() as session:
            try:
                db_entity = session.query(AlarmEntity).filter(
                    AlarmEntity.id == alarm_id
                ).first()

                if db_entity is None:
                    raise DatabaseError(message="Alarm not found.")

                if not db_entity.is_active:
                    raise AlarmAlreadyActiveException(message="Alarm is already acknowledged")

                db_entity.is_active = False
                session.commit()

            except DatabaseError:
                session.rollback()
                raise

            except Exception as e:
                session.rollback()
                raise DatabaseError(
                    message=f"Unknown database error: {str(e)}"
                )

    def set_alarm(self, alarm: Alarm):
        print("Saving alarm to db")
        with SessionLocal() as session:
            try:
                db_entity = AlarmEntity(
                    user_id=alarm.user_id,
                    timestamp=alarm.timestamp,
                    message=alarm.message,
                    is_active=True,
                    level=alarm.level
                )
                session.add(db_entity)
                session.commit()
            except IntegrityError as e:
                # --- GERÇEK HATAYI BURADA YAZDIRALIM ---
                print(f"--- DATABASE INTEGRITY ERROR DETAYI ---")
                print(f"Original Exception: {e.orig}")
                print(f"Statement: {e.statement}")
                print(f"Parameters: {e.params}")
                print(f"--------------------------------------")
                session.rollback()
                error_str = str(e.orig)

                if "UniqueViolation" in error_str:
                    raise DatabaseError(message="There already is an alarm set at the given timestamp.")

                else:
                    raise DatabaseError(message="Database integrity error")

            except Exception as e:
                session.rollback()
                raise DatabaseError(message=f"Unknown database error: {str(e)}")

    def get_active_alarms(self, user_id: str):
        with SessionLocal() as session:
            entities = session.query(AlarmEntity) \
                .filter(AlarmEntity.user_id == user_id,
                         AlarmEntity.is_active) \
                .all()
            return [
                Alarm(
                    id=entity.id,
                    level=entity.level,
                    message=entity.message,
                    timestamp=entity.timestamp
                )
                for entity in entities
            ]