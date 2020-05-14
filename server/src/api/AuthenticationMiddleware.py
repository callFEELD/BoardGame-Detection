import re

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse


class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, auth_token: str):
        """
        Create a new auth middleware

        :param app: A fastapi app
        :param auth_token: The auth token which should be used for authentication
        """

        super().__init__(app)

        self.auth_token = auth_token

        # Get the api doc urls
        self.openapi_url = app.openapi_url
        self.docs_url = app.docs_url
        self.redoc_url = app.redoc_url

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        if self._matches_docs_url(request.url.path):
            return await call_next(request)

        header_token = ''
        if 'X-authentication-token' in request.headers:
            header_token = request.headers['X-authentication-token']

        if header_token != self.auth_token:
            exception: dict = {'error': 'Wrong X-authentication-token'}
            return JSONResponse({'detail': exception}, status_code=401)

        return await call_next(request)

    def _matches_docs_url(self, url: str) -> bool:
        redoc = re.match(f'^{self.redoc_url}(#.*)?$', url)
        doc = re.match(f'^{self.docs_url}(#/.*)?$', url)
        openapi = re.match(f'^{self.openapi_url}$', url)

        return bool(redoc or doc or openapi)
