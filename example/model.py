from .database import db
from sqlalchemy import Column, Integer, String

class User(db.base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', age={self.age})>"
