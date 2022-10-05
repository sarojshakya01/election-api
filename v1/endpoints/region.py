from fastapi import Depends, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import v1.dependencies.dependencies as dependencies

from core.models.models import Province, District, Region
import json

router = APIRouter(
    prefix="/api/v1/region",
    tags=["region", "district", "province"],
    #    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {
        "description": "Not found"
    }})


@router.get("/all")
async def get_regions(db: Session = Depends(
    dependencies.get_database_session)):
    try:
        result = db.execute(
            'SELECT JSON_OBJECT("id", pdr.province_id, "name_np", pdr.name_np, "name_en", pdr.name_en, "color", pdr.color, "districts", pdr.districts) from ds_v_province_district_regions pdr;'
        )
        data = []
        for p in (result):
            data.append(json.loads(p[0]))
        return {
            "data": data,
            "message": "Data Read Successfully",
            "status": "OK"
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,
                            detail={
                                "data": [],
                                "message": "Data Read Failed",
                                "status": "FAILED"
                            })
    # try:
    #   with open("data/regions.json") as stream:
    #     regions = json.load(stream)
    #   return {"data": regions, "message": "Data Read Successfully", "status": "OK"}
    # except:
    #   raise HTTPException(status_code=404, detail={"data": [], "message": "Data Read Failed", "status": "FAILED"})
