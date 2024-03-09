import yaml

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DBConfig(object):
    def __init__(self, file):
        self._load(file)
        self.url = self.config.get('url', 'sqlite:///:memory:')
        self.kwargs = {key: value for key, value in self.config.items() if key != "url"}
        self.session = None
        
    def _load(self, file_name):
        with open(file_name) as file:
            data = yaml.safe_load(file)
        if not data['database']:
            ValueError(f"Database Configuration not found on file {file_name}")
        self.config = data['database']

class SQLAlchemy(object):
    def __init__(self, file='config.yml'):
        self.config = DBConfig(file)
        self.engine = create_engine(self.config.url,
                                    **self.config.kwargs)
        self.base = declarative_base()
    
    def create_all(self):
        self.base.metadata.create_all(self.engine)
    
    def init_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def init(self, create_all=True):
        if create_all:
            self.create_all()
        self.init_session()
    
    def close(self):
        self.session.close()

class BaseRepository(object):
    def __init__(self, db: SQLAlchemy, model_class):
        self.session = db.session
        self.model_class = model_class

    def all(self):
        return self.session.query(self.model_class).all()

    def find_by_id(self, id):
        return self.session.query(self.model_class).get(id)

    def save(self, instance):
        if instance.id and self.session.get(instance.__class__, instance.id) is None:
            self.session.add(instance)
        else:
            self.session.merge(instance)

    def save_and_flush(self, instance):
        self.save(instance)
        self.commit()
        return instance.id

    def delete(self, instance):
        self.session.delete(instance)
        self.commit()

    def commit(self):
        self.session.commit()
        self.session.flush()
