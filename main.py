from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import v1.dependencies.dependencies as dependencies
from v1.endpoints import region, result, party, candidate, admin
from core.models.database import engine
from core.models import models
from core.settings import ALLOWED_ORIGINS

# app = FastAPI(dependencies=[Depends(dependencies.get_query_token)])
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(result.router)
app.include_router(region.router)
app.include_router(party.router)
app.include_router(candidate.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {
        "description": "You are not authorized to see this page"
    }},
)


@app.get("/")
async def root():
  return {"response": "API is running"}
