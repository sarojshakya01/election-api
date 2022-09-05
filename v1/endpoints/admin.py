from fastapi import Depends, FastAPI, APIRouter, Depends, Header, HTTPException

# import v1.dependencies.dependencies as dependencies

import json


router = APIRouter(prefix="/api/v1",
                   tags=["central", "province"],
                #    dependencies=[Depends(dependencies.get_token_header)],
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/results/{type}")
async def get_result(type: str):
    print(123, type)
    if type == "central":
        with open('data/central.json') as stream:
            districts = json.load(stream)
        return {
            'data': districts,
            'message': "Data Read Successfully",
            'status': 'OK'
        }
    elif type == "province":
        with open('data/province.json') as stream:
            provinces = json.load(stream)
        return {
            'data': provinces,
            'message': "Data Read Successfully",
            'status': 'OK'
        }
    else:

        raise HTTPException(status_code=404,
                            detail={
                                'data': [],
                                'message': "Data Read Failed",
                                'status': 'FAILED'
                            })
