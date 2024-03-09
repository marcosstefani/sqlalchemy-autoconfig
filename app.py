from example.database import db
from example.model import User
from example.repository import UserRepository

db.init()

new_user = User(name='John', age=30)

user_repo = UserRepository()

user_repo.save_and_flush(new_user)

users = user_repo.all()
print('1', users)
print('2', id, user_repo.find_by_id(1))

db.close()
