import typing as t
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from piccolo.apps.user.tables import BaseUser

from api.accounts.schema import Token, TokenData, UserModelIn, UserModelOut
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="accounts/login")
router = APIRouter(prefix="/accounts")


def create_access_token(
    data: dict,
    expires_delta: t.Optional[timedelta] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode["exp"] = expire
    return jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = (
        await BaseUser.select()
        .where(BaseUser.username == token_data.username)
        .first()
        .run()
    )
    if user is None:
        raise credentials_exception
    return user


@router.post("/login/", response_model=Token, tags=["Auth"])
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await BaseUser.login(
        username=form_data.username, password=form_data.password
    )
    result: t.Any = await BaseUser.select().where(BaseUser.id == user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": result["username"]}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register/", response_model=UserModelOut, tags=["Auth"])
async def register_user(user: UserModelIn):
    user = BaseUser(**user.__dict__)
    if (
        await BaseUser.exists().where(BaseUser.email == user.email).run()
        or await BaseUser.exists()
        .where(BaseUser.username == user.username)
        .run()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with that email or username already exists.",
        )
    await user.save().run()
    return UserModelOut(**user.__dict__)


@router.get("/profile/", response_model=UserModelOut, tags=["User profile"])
async def user_profile(
    current_user: UserModelOut = Depends(get_current_user),
):
    return current_user
