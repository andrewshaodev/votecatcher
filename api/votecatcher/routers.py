from fastapi import APIRouter, Depends
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper

from api.accounts.routers import oauth2_scheme
from api.votecatcher.tables import APIKey

votecatcher_router = APIRouter()

FastAPIWrapper(
    root_url="/apikeys/",
    fastapi_app=votecatcher_router,
    piccolo_crud=PiccoloCRUD(
        table=APIKey,
        read_only=False,
    ),
    fastapi_kwargs=FastAPIKwargs(
        all_routes={"tags": ["ApiKey"]},
        post={"dependencies": [Depends(oauth2_scheme)]},
        put={"dependencies": [Depends(oauth2_scheme)]},
        patch={"dependencies": [Depends(oauth2_scheme)]},
        delete_single={"dependencies": [Depends(oauth2_scheme)]},
    ),
)
