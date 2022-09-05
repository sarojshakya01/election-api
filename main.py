from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import v1.dependencies.dependencies as dependencies

from v1.endpoints import result, district, admin

# app = FastAPI(dependencies=[Depends(dependencies.get_query_token)])
app = FastAPI()

origins = [
    "http://localhost:3001",
    "http://localhost:3333",
    "https://saroj.el369.javra.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(result.router)
app.include_router(district.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(dependencies.get_token_header)],
    responses={
        418: {
            "description": "You are not authorized to see this page"
        }
    },
)


@app.get("/")
async def root():
    return {"response": "API is running"}