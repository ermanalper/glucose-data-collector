from sqlalchemy.exc import IntegrityError

from app.api.schemas.insulin_dose_schema import InsulinDoseResponse
from app.core.exceptions import DuplicateEntiresException, DatabaseError, ResourceNotFoundException
from app.infrastructure.interfaces.insulin_repository_interface import IInsulinRepository
from app.infrastructure.persistence.entities.insulin_dose_orm import InsulinDoseEntity
from app.infrastructure.persistence.entities.insulin_orm import InsulinEntity
from app.models.insulin import Insulin
from app.infrastructure.persistence.database import SessionLocal
from app.models.insulin_dose import InsulinDose


class SqlAlchemyInsulinRepository(IInsulinRepository):
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
                    timestamp=insulin_dose.timestamp
                )
                session.add(db_entity)
                session.commit()
                return InsulinDoseResponse(message=f"Insuline dose successfully entered. User: '{insulin_dose.user_id} Insulin type ID: '{insulin_dose.insulin_type.id} Dose: '{insulin_dose.dose}'")
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
