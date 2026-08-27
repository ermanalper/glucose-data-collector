from typing import Optional

from app.infrastructure.interfaces.glucose_repository_interface import IGlucoseRepository
from app.models.glucose import Glucose, TrendState
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

    def get_latest(self, user_id: str) -> Optional[Glucose]:
        with SessionLocal() as session:
            entity = session.query(GlucoseEntity) \
                .filter(GlucoseEntity.user_id == user_id) \
                .order_by(GlucoseEntity.timestamp.desc()) \
                .first()

            if not entity:
                return None

            return Glucose(
                value=entity.value,
                timestamp=entity.timestamp,
                trend=TrendState(entity.trend),
                source=entity.source
            )