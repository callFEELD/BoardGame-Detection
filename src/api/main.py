import re

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.api.endpoints import gameboarddetection as gbd

app = FastAPI()
token = '123456789'


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Prevent calling the api if the token is not provided
    """

    def matches_docs_url(s_str: str) -> bool:
        return bool(re.match('^/redoc.*', s_str) or re.match('^/docs.*$', s_str) or re.match('^/openapi.json$', s_str))

    url: str = request.url.path

    header_token = ''
    if 'X-authentication-token' in request.headers:
        header_token = request.headers['X-authentication-token']

    if header_token != token and not matches_docs_url(url):
        exception: dict = {'error': 'Wrong X-authentication-token'}
        return JSONResponse({'detail': exception}, status_code=401)

    return await call_next(request)


app.include_router(gbd.router)
