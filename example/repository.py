from autoconfig import BaseRepository

from .database import db
from .model import User

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(db, User)
