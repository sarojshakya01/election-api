from fastapi import Depends, FastAPI, APIRouter, Depends, Header, HTTPException

# import v1.dependencies.dependencies as dependencies

import json

router = APIRouter(
    prefix="/api/v1/region",
    tags=["central", "province"],
    #    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {
        "description": "Not found"
    }})


@router.get("/all")
async def get_regions():
  try:
    with open('data/regions.json') as stream:
      regions = json.load(stream)
    return {'data': regions, 'message': "Data Read Successfully", 'status': 'OK'}
  except:

    raise HTTPException(status_code=404, detail={'data': [], 'message': "Data Read Failed", 'status': 'FAILED'})
