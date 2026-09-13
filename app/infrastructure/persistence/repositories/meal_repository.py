from sqlalchemy.exc import IntegrityError

from app.core.exceptions import DatabaseError
from app.infrastructure.interfaces.meal_repository_interface import IMealRepository
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
