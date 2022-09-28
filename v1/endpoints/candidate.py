from fastapi import Depends, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import v1.dependencies.dependencies as dependencies
import json

from core.models.models import Candidate

router = APIRouter(
    prefix="/api/v1/candidate",
    tags=["party"],
    #    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {
        "description": "Not found"
    }})


@router.get("/all")
async def get_parties(db: Session = Depends(dependencies.get_database_session)):
  try:
    result = db.query(Candidate).all()
    data = []
    for c in result:
      d = {
        "id": c.id,
        "rtype" : c.rtype,
        "region_id": c.region_id,
        "district_id": c.district_id,
        "province_id": c.province_id,
        "party_code": c.party_code,
        "name_np": c.name_np,
        "name_en": c.name_en,
        "vote": c.vote,
        "elected": c.elected,
        "descriptions": c.descriptions,
      }
      data.append(d)
    return {"data": {"candidates": data}, "message": "Data Read Successfully", "status": "OK"}
  except Exception as e:
    print(e)
    raise HTTPException(status_code=404, detail={"data": [], "message": "Data Read Failed", "status": "FAILED"})
  
  # try:
  #   with open("data/parties.json") as stream:
  #     parties = json.load(stream)
  #   return {"data": parties, "message": "Data Read Successfully", "status": "OK"}
  # except:
  #   raise HTTPException(status_code=404, detail={"data": [], "message": "Data Read Failed", "status": "FAILED"})
