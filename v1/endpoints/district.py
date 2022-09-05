from fastapi import Depends, FastAPI, APIRouter, Depends, Header, HTTPException

# import v1.dependencies.dependencies as dependencies

import json


router = APIRouter(prefix="/api/v1/district",
                   tags=["central", "province"],
                #    dependencies=[Depends(dependencies.get_token_header)],
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/")
async def get_regions(type: str):
    try:
        with open('data/districts.json') as stream:
            districts = json.load(stream)
        return {
            'data': districts,
            'message': "Data Read Successfully",
            'status': 'OK'
        }
    except:

        raise HTTPException(status_code=404,
                            detail={
                                'data': [],
                                'message': "Data Read Failed",
                                'status': 'FAILED'
                            })
