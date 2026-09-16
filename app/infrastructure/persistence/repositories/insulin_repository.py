from datetime import timezone
from typing import List

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import DatabaseError, ResourceNotFoundException
from app.infrastructure.interfaces.insulin.insulin_repository_interface import IInsulinRepository
from app.infrastructure.persistence.entities.insulin_dose_orm import InsulinDoseEntity
from app.infrastructure.persistence.entities.insulin_orm import InsulinEntity
from app.models.insulin import Insulin
from app.infrastructure.persistence.database import SessionLocal
from app.models.insulin_dose import InsulinDose


class SqlAlchemyInsulinRepository(IInsulinRepository):
    def get_insulin_types(self):
        with SessionLocal() as session:
            entities = session.query(InsulinEntity) \
                .order_by(InsulinEntity.id) \
                .all()
        return [
            Insulin(id=entity.id, name=entity.type)
            for entity in entities
        ]


    def get_insulin_history_by_time_interval(self, start_time, end_time, user_id) -> List[InsulinDose]:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        with SessionLocal() as session:
            entities = session.query(InsulinDoseEntity) \
                .filter(InsulinDoseEntity.user_id == user_id) \
                .filter(InsulinDoseEntity.timestamp >= start_time) \
                .filter(InsulinDoseEntity.timestamp <= end_time) \
                .order_by(InsulinDoseEntity.timestamp.desc()) \
                .all()
        return [
            InsulinDose(
                user_id=entity.user_id,
                insulin_type=Insulin(
                    id=entity.insulin_type.id,
                    name=entity.insulin_type.type
                ),
                dose=entity.dose,
                timestamp=entity.timestamp,
                glucose_value=entity.glucose_val
            )
            for entity in entities
        ]

    def add_insulin(self, insulin: Insulin) -> None:
        with SessionLocal() as session:
            try:
                db_entity = InsulinEntity(
                    type=insulin.name
                )

                session.add(db_entity)
                session.commit()

                print(f"[DB] Written to SQL: Insulin Type '{insulin.name}'")
            except Exception as e:
                # Rollback in case of error
                session.rollback()
                print(f"[DB ERROR] SQL error: {e}")

    def enter_insulin_dose(self, insulin_dose: InsulinDose):
        with SessionLocal() as session:
            try:
                db_entity = InsulinDoseEntity(
                    user_id=insulin_dose.user_id,
                    insulin_type_id=insulin_dose.insulin_type.id,
                    dose=insulin_dose.dose,
                    timestamp=insulin_dose.timestamp,
                    glucose_val=insulin_dose.glucose_value
                )
                session.add(db_entity)
                session.commit()
                return "Insulin dose successfully entered. User: '{insulin_dose.user_id} Insulin type ID: '{insulin_dose.insulin_type.id} Dose: '{insulin_dose.dose}'"
            except IntegrityError as e:
                session.rollback()
                error_str = str(e.orig)

                if "ForeignKeyViolation" in error_str:
                    raise ResourceNotFoundException("No insulin found with given ID")

                elif "UniqueViolation" in error_str:
                    raise DatabaseError(message="There already is a dose entry at the given time.")

                else:
                    raise DatabaseError(message="Database integrity error")

            except Exception as e:
                session.rollback()
                raise DatabaseError(message=f"Unknown database error: {str(e)}")
