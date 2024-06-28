from fastapi import FastAPI
from routes.resource import resource

app = FastAPI()

app.include_router(resource)
