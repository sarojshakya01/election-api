from fastapi import Depends, APIRouter, Depends, Header, HTTPException

# import v1.dependencies.dependencies as dependencies

import json

router = APIRouter(
    prefix="/api/v1/result",
    tags=["central", "province"],
    #    dependencies=[Depends(dependencies.get_token_header)],
    responses={404: {
        "description": "Not found"
    }})


@router.get("/{type}")
async def get_result(type: str):
    if type == "federal":
        with open('data/federal.json') as stream:
            federal = json.load(stream)
        return {
            'data': {
                'provinces': federal
            },
            'message': "Data Read Successfully",
            'status': 'OK'
        }
    elif type == "provincial":
        with open('data/provincial.json') as stream:
            provincial = json.load(stream)
        return {
            'data': {
                'provinces': provincial
            },
            'message': "Data Read Successfully",
            'status': 'OK'
        }
    elif type == "all":
        federal = []
        provincial = []
        with open('data/federal.json') as stream:
            federal = json.load(stream)
        with open('data/provincial.json') as stream:
            provincial = json.load(stream)
        return {
            'data': [{
                'federal': {
                    'provinces': federal
                },
                'provincial': {
                    'provinces': provincial
                }
            }],
            'message':
            "Data Read Successfully",
            'status':
            'OK'
        }
    else:
        raise HTTPException(status_code=404,
                            detail={
                                'data': [],
                                'message': "Data Read Failed",
                                'status': 'FAILED'
                            })
