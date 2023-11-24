from typing import Annotated

from fastapi import Depends

import models
from dtos.location import AddNewLocationReq
from services.base_service import BaseService


class LocationService(BaseService):
    def __init__(self, db: models.db_dependency):
        super(LocationService, self).__init__(db)

    def get_all_locations(self):
        return self.db.query(models.Location).all()

    def add_new_location(self, req: AddNewLocationReq) -> models.Location:
        location = models.Location(**req.model_dump())

        self.add(location)
        self.commit()

        return location


def init_location_service(db: models.db_dependency):
    return LocationService(db)


LocationServ = Annotated[LocationService, Depends(init_location_service)]