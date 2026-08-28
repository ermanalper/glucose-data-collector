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

    '''
    :param user_id: The target user's id. (This is a self-hosted backend, so 
                    it supports only one user unless changed. Try 'default_user')
    :returns:       The last glucose reading
    '''
    def get_latest(self, user_id: str) -> Optional[Glucose]:
        results = self.get_latest_n(user_id, 1)
        if not results:
            return None
        return results[0]

    '''
    :param user_id: The target user's id. (This is a self-hosted backend, so 
                    it supports only one user unless changed. Try 'default_user')
    :param n:       Last n glucose readings. If there are less than n glucose readings,
                    all readings are returned.
    :returns:       The last n glucose readings.
    '''
    def get_latest_n(self, user_id: str, n: int) -> list[Glucose]:
        with SessionLocal() as session:
            entities = session.query(GlucoseEntity) \
                .filter(GlucoseEntity.user_id == user_id) \
                .order_by(GlucoseEntity.timestamp.desc()) \
                .limit(n) \
                .all()
            return [
                Glucose(
                    value=entity.value,
                    timestamp=entity.timestamp,
                    trend=TrendState(entity.trend),
                    source=entity.source
                )
                for entity in entities
            ]