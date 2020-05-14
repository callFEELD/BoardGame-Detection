import os

from fastapi import FastAPI

from src.api.AuthenticationMiddleware import AuthenticationMiddleware
from src.api.endpoints import gameboarddetection as gbd

app = FastAPI()
app.include_router(gbd.router)

auth_token = os.environ.get('auth_token', '123456789')
app = AuthenticationMiddleware(app, auth_token)
