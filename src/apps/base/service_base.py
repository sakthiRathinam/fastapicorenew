from pydantic import BaseModel, conint
from fastapi_pagination import Params
from typing import TypeVar, Generic, Sequence
from fastapi_pagination.bases import AbstractPage, AbstractParams
from typing import TypeVar, Type, Optional, Union
from fastapi import Request, Response
from fastapi import HTTPException
from pydantic import BaseModel
from tortoise.models import Model

from tortoise import models
from fastapi_pagination.ext.tortoise import paginate
from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from tortoise.queryset import QuerySet



ModelType = TypeVar("ModelType", bound=models.Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)
QuerySchemaType = TypeVar("QuerySchemaType", bound=BaseModel)


class BaseService:
    model: Type[ModelType]
    create_schema: CreateSchemaType
    update_schema: UpdateSchemaType
    query_schema: QuerySchemaType
    get_schema: GetSchemaType
    async def create(self, schema, *args, **kwargs) -> Optional[CreateSchemaType]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)
    async def update(self, schema, **kwargs) -> Optional[UpdateSchemaType]:
        await self.model.filter(**kwargs).update(**schema.dict(exclude_unset=True))
        return await self.get_schema.from_queryset_single(self.model.get(**kwargs))
    async def update_extra(self, id,schema, **kwargs) -> Optional[UpdateSchemaType]:
        obj = await self.model.get(id=id).update(**schema.dict(exclude_unset=True),**kwargs)
        return obj
    async def delete(self, **kwargs):
        obj = await self.model.filter(**kwargs).delete()
        if not obj:
            raise HTTPException(status_code=404, detail='Object does not exist')
    async def all(self) -> Optional[GetSchemaType]:
        return await self.get_schema.from_queryset(self.model.all())
    async def filter(self, **kwargs) -> Optional[GetSchemaType]:
        return await self.get_schema.from_queryset(self.model.filter(**kwargs))
    async def get(self, **kwargs) -> Optional[GetSchemaType]:
        return await self.get_schema.from_queryset_single(self.model.get(**kwargs))
    async def get_obj(self, **kwargs) -> Optional[ModelType]:
        return await self.model.get_or_none(**kwargs)
    async def get_or_create(self, **kwargs) -> Optional[ModelType]:
        return await self.model.get_or_create(**kwargs)
    async def paginate_data(query:QuerySet):
        if not isinstance(query, QuerySet):
            query = await query.all()
        paginated_data =  await paginate(query)
        print(request.query_params)
        extra = {'previous': False, "next": True}
        if request.query_params['page'] != str(1):
            extra['previous'] = True
        if (int(request.query_params['page']) * int(request.query_params['size']))+1 > paginated_data.total:
            extra['next'] = False
        data = {**paginated_data.dict(), **extra}
        return data
    async def limited_data(self, offset,limit,**kwargs) -> Optional[ModelType]:
        toReturn = {
            'total':None,
            'prev':False,
            'next':True,
            'data':None,
        }
        print(kwargs)
        toReturn['total'] = await self.model.filter(**kwargs).count()
        if offset+limit+1 > toReturn['total']:
            toReturn['next'] = False
        if offset != 0:
            toReturn['prev'] = True
        toReturn['data'] =  await self.model.filter(**kwargs).offset(offset).limit(limit)
        return toReturn
    

######################Base Functions###############################
# @clinto_router.post('/addMedicines')
# async def add_medicines(data: Create_Medicine = Body(...)):
#     add_medicine = await medicine_view.create(data)
#     return {"medicine": "medicine created successfully", "medicine_obj": add_medicine}


# @clinto_router.delete('/deleteMedicines')
# async def delete_medicines(id: int):
#     await medicine_view.delete(id=1)
#     return {"success": "deleted"}


# @clinto_router.put('/updateMedicines')
# async def update_medicines(id: int, data: Create_Medicine = Body(...)):
#     await medicine_view.update(data, id=id)
#     return {"success": "updated"}


# @clinto_router.put('/filtermedicines')
# async def filter_medicines(data: GET_Medicine = Body(...)):
#     await medicine_view.filter(**data.dict(exclude_unset=True))
#     return {"success": "updated"}
T = TypeVar("T")

class CustomPage(AbstractPage[T], Generic[T]):
    results: Sequence[T]
    total : int
    page: conint(ge=1)  # type: ignore
    size: conint(ge=1)     
    previous: Optional[bool] = False
    next: Optional[bool] = False
    __params_type__ = Params  # Set params related to Page
    @classmethod
    def create(
            cls,
            items: Sequence[T],
            total: int,
            params: AbstractParams,
            previous: Optional[bool]= False,
            next: Optional[bool]=False,
    ) -> Page[T]:
        return cls(results=items, total=total,page=params.page,size=params.size)
    
from math import radians,cos,sin,tan,atan2,sqrt
async def nearest(lon1, lat1, lon2, lat2, clinic_obj):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    distance = round(distance, 2)
    if distance < 5:
        return distance
    return None


async def find_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    print("Result:", distance)
    print("Should be:", distance, "km")
    return distance


