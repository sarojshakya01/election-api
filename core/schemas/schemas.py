from datetime import datetime
from pydantic import BaseModel


class ElectionResults(BaseModel):
    id = int
    province_id = int
    district_id = str
    type = str
    region_id = float
    declared = bool
    result = object
    elected = object
    created_at = datetime
    updated_at = datetime

    class Config:
        orm_mode = True


class Districts(BaseModel):
    id = int
    province_id = int
    district_id = str
    name_np = str
    name_en = str
    created_at = datetime
    updated_at = datetime

    class Config:
        orm_mode = True


class Provinces(BaseModel):
    id = int
    province_id = int
    name_np = str
    name_en = str
    created_at = datetime
    updated_at = datetime

    class Config:
        orm_mode = True
