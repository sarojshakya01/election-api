from fastapi import Depends, FastAPI, APIRouter, Depends, Header, HTTPException

# import v1.dependencies.dependencies as dependencies

import json

router = APIRouter(
    prefix="/api/v1/party",
    tags=["central", "province"],
    #    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {
        "description": "Not found"
    }})


@router.get("/all")
async def get_parties():
    try:
        with open('data/parties.json') as stream:
            parties = json.load(stream)
        return {
            'data': parties,
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
