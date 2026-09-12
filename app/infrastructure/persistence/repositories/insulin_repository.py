from app.infrastructure.interfaces.insulin_repository_interface import IInsulinRepository
from app.models.insulin import Insulin
from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.entities.insulin_orm import InsulinEntity
class SqlAlchemyInsulinRepository(IInsulinRepository):
    def add_insulin(self, insulin: Insulin) -> None:
        with SessionLocal() as session:
            try:
                db_entity = InsulinEntity(
                    user_id=insulin.user_id,
                    type=insulin.name
                )

                session.add(db_entity)
                session.commit()

                print(f"[DB] Written to SQL: Insulin Type '{insulin.name}' for user '{insulin.user_id}'")
            except Exception as e:
                # Rollback in case of error
                session.rollback()
                print(f"[DB ERROR] SQL error: {e}")