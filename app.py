from fastapi import FastAPI
from routes.keyspace import router as keyspace_router

app = FastAPI()

# Include keyspace-related routes
app.include_router(keyspace_router)

#@app.get("/")
#async def root():
 #   return {"message": "AstraDB FastAPI Service Running"}
