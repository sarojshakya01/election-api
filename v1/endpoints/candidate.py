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
async def get_candidates(db: Session = Depends(
    dependencies.get_database_session)):
    try:
        result = db.query(Candidate).all()
        data = []
        for c in result:
            data.append(c)
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
