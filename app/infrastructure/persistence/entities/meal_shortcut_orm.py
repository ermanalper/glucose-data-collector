from sqlalchemy import Column, Integer, String

from app.infrastructure.persistence.database import Base

class MealShortcutEntity(Base):
    __tablename__ ='meal_shortcuts'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    title = Column(String)
    desc = Column(String)
