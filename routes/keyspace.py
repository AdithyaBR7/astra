from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.keyspace_service import create_keyspace_if_not_exists, get_keyspaces

router = APIRouter()

class KeyspaceRequest(BaseModel):
    org: str

@router.get("/v1/orgs")
async def list_keyspaces():
    keyspaces = get_keyspaces()
    if keyspaces:
        return {"org_list": keyspaces}
    raise HTTPException(status_code=500, detail="Failed to retrieve org.")

@router.post("/v1/register")
async def create_keyspace(keyspace_request: KeyspaceRequest):
    result = create_keyspace_if_not_exists(keyspace_request.org)
    if result:
        return result
    raise HTTPException(status_code=500, detail="Error creating org.")
