from fastapi import Header, HTTPException
from core.models.database import SessionLocal

async def get_token_header(x_token: str = Header(default=None)):
    if x_token != "token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "election":
        raise HTTPException(status_code=400,
                            detail="No token provided")

def get_database_session():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()