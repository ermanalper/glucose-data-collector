from app.infrastructure.interfaces.glucose_repository_interface import IGlucoseRepository
from app.models.glucose import Glucose
from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.entities.glucose_orm import GlucoseEntity


class  SqlAlchemyGlucoseRepository(IGlucoseRepository):
    def save(self, glucose: Glucose) -> None:
         with SessionLocal() as session:
            try:
                db_entity = GlucoseEntity(
                    user_id="default_user",
                    value=glucose.value,
                    timestamp=glucose.timestamp,
                    trend=glucose.trend.value, #get enum's string value
                    source=glucose.source
                )

                session.add(db_entity)
                session.commit()

                print(f"[DB] Written to SQL: {glucose.value} mg/dL | Direction: {glucose.trend.value}")
            except Exception as e:
                # Rollback in case of error
                session.rollback()
                print(f"[DB ERROR] SQL error: {e}")