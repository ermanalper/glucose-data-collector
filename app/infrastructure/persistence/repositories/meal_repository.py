import datetime
from typing import List

from sqlalchemy.exc import IntegrityError

from app.core.exceptions import DatabaseError
from app.infrastructure.interfaces.meals.meal_repository_interface import IMealRepository
from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.entities.meal_orm import MealEntity
from app.infrastructure.persistence.entities.meal_shortcut_orm import MealShortcutEntity
from app.models.meal import Meal
from app.models.meal_shortcut import MealShortcut


class MealRepositoryImpl(IMealRepository):
    def save_meal(self, meal: Meal):
        with SessionLocal() as session:
            try:
                db_entity = MealEntity(
                    user_id=meal.user_id,
                    timestamp=meal.timestamp,
                    glucose_value=meal.glucose_value,
                    desc=meal.desc
                )
                session.add(db_entity)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                error_str = str(e.orig)

                if "UniqueViolation" in error_str:
                    raise DatabaseError(message="There already is a meal entry at the given time.")

                else:
                    raise DatabaseError(message="Database integrity error")

            except Exception as e:
                session.rollback()
                raise DatabaseError(message=f"Unknown database error: {str(e)}")

    def save_meal_shortcut(self, meal_shortcut: MealShortcut):
        with SessionLocal() as session:
            try:
                db_entity = MealShortcutEntity(
                    user_id=meal_shortcut.user_id,
                    title=meal_shortcut.title,
                    desc=meal_shortcut.desc
                )
                session.add(db_entity)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise DatabaseError(message="Database integrity error")

            except Exception as e:
                session.rollback()
                raise DatabaseError(message=f"Unknown database error: {str(e)}")

    def get_meal_shortcuts(self, user_id: str) -> List[MealShortcut]:
        with SessionLocal() as session:
            entities = session.query(MealShortcutEntity) \
                .filter(MealShortcutEntity.user_id == user_id) \
                .all()

            return [
                MealShortcut(
                    user_id=entity.user_id,
                    title=entity.title,
                    desc=entity.desc
                )
                for entity in entities
            ]

    def get_meal_history_by_time_interval(self, start_time: datetime, end_time: datetime, user_id: str) -> List[Meal]:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=datetime.timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=datetime.timezone.utc)

        with SessionLocal() as session:
            entities = session.query(MealEntity) \
                .filter(MealEntity.user_id == user_id) \
                .filter(MealEntity.timestamp >= start_time) \
                .filter(MealEntity.timestamp <= end_time) \
                .order_by(MealEntity.timestamp.desc()) \
                .all()
        return [
            Meal(
                user_id=entity.user_id,
                timestamp=entity.timestamp,
                desc=entity.desc,
                glucose_value=entity.glucose_value
            )
            for entity in entities
        ]



