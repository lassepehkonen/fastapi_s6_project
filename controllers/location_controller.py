from fastapi import APIRouter

import models
from dtos.location import AddNewLocationReq, AddNewLocationRes
from services.location_service import LocationServ

router = APIRouter(
    prefix='/api/v1/locations',
    tags=['locations']
)

"""

name: "sdlkjfsdlkdsfjsdfl",
"address": "ldskjfdlsdfkjfsdlkfsd",
"zip_code": "sdlkfdjsdlfkfjdsl"

"""


@router.get('/')
async def get_all_locations(service: LocationServ):
    locations = service.get_all_locations()
    return {'locations': locations}


@router.post('/', response_model=AddNewLocationRes)
async def add_new_location(req: AddNewLocationReq, service: LocationServ):
    location = service.add_new_location(req)
    return location

