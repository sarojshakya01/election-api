from fastapi import Depends, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import v1.dependencies.dependencies as dependencies
import json

from core.models.models import Party

router = APIRouter(
    prefix="/api/v1/party",
    tags=["party"],
    #    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {
        "description": "Not found"
    }})


@router.get("/all")
async def get_parties(db: Session = Depends(
    dependencies.get_database_session)):
    try:
        result = db.query(Party).all()
        data = []
        for p in result:
            d = {
                "id": p.party_id,
                "code": p.code,
                "name_np": p.name_np,
                "name_en": p.name_en,
                "short_name_np": p.short_name_np,
                "short_name_en": p.short_name_en,
                "color": p.color,
                "symbol": p.symbol
            }
            data.append(d)
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
    #   with open("data/parties.json") as stream:
    #     parties = json.load(stream)
    #   return {"data": parties, "message": "Data Read Successfully", "status": "OK"}
    # except:
    #   raise HTTPException(status_code=404, detail={"data": [], "message": "Data Read Failed", "status": "FAILED"})
