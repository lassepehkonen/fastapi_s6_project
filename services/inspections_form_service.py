from typing import Annotated

from fastapi import Depends

from models import db_dependency
import models
from services.base_service import BaseService


def init_form_service(db: db_dependency):
    return InspectionFormService(db)


class InspectionFormService(BaseService):
    def __init__(self, db: db_dependency):
        super(InspectionFormService, self).__init__(db)

    def get_by_id(self, _id: int):
        return self.db.query(models.Inspectionform).filter(models.Inspectionform.id == _id).first()


FormServ = Annotated[InspectionFormService, Depends(init_form_service)]

