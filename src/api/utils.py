from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Annotated
import requests

security = HTTPBasic()


async def get_token(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    session = requests.Session()
    session.auth = (credentials.username, credentials.password)
    token_request = session.post('https://api.moysklad.ru/api/remap/1.2/security/token')
    try:
        return token_request.json()['access_token']

    except KeyError:
        return token_request.json()
