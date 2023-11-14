import models


class BaseService:
    def __init__(self, db: models.db_dependency):
        self.db = db

    def commit(self):
        self.db.commit()

    def add(self, entity):
        self.db.add(entity)
