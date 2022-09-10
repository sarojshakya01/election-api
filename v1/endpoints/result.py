from unittest import result
from fastapi import Request, Depends, APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

# import v1.dependencies.dependencies as dependencies
from core.models.models import ElectionFResult, ElectionPResult
from core.models import models

import json

router = APIRouter(
    prefix="/api/v1/result",
    tags=["central", "province"],
    #    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {
        "description": "Not found"
    }})

from core.models.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# @router.get("/{type}")
# async def get_result(type: str):
#     if type == "federal":
#         with open("data/federal.json") as stream:
#             federal = json.load(stream)
#         return {
#             "data": federal,
#             "message": "Data Read Successfully",
#             "status": "OK"
#         }
#     elif type == "provincial":
#         with open("data/provincial.json") as stream:
#             provincial = json.load(stream)
#         return {
#             "data": provincial,
#             "message": "Data Read Successfully",
#             "status": "OK"
#         }
#     elif type == "all":
#         federal = []
#         provincial = []
#         with open("data/federal.json") as stream:
#             federal = json.load(stream)
#         with open("data/provincial.json") as stream:
#             provincial = json.load(stream)
#         return {
#             "data": [{
#                 "federal": federal,
#                 "provincial": provincial
#             }],
#             "message": "Data Read Successfully",
#             "status": "OK"
#         }
#     else:
#         raise HTTPException(status_code=404,
#                             detail={
#                                 "data": [],
#                                 "message": "Data Read Failed",
#                                 "status": "FAILED"
#                             })


@router.get("/{type}")
async def fetch_results(request: Request,
                        db: Session = Depends(get_database_session)):
    fprovinces = db.execute("select provinces from ds_v_federal_results")
    pprovinces = db.execute("select provinces from ds_v_provincial_results")
    federal = {"provinces": []}
    provincial = {"provinces": []}
    count = 1
    for row in fprovinces:
        prov = {"id": count, "districts": json.loads(row[0])}
        federal["provinces"].append(prov)
        count = count + 1
    for row in pprovinces:
        prov = {"id": count, "districts": json.loads(row[0])}
        count = count + 1
        provincial["provinces"].append(prov)
    return {
        "data": [{
            "federal": federal,
            "provincial": provincial
        }],
        "message": "Data Read Successfully",
        "status": "OK"
    }
