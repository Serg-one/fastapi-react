import os
import jwt
import dotenv

import fastapi
import fastapi.security as security
import sqlalchemy.orm as orm
import passlib.hash as hash

import database
import models
import schemas


dotenv.load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")


def create_database():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_db_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def create_user(user: schemas.UserCreate, db: orm.Session):
    user_obj = models.User(
        email=user.email,
        hashed_password=hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_db_user_by_email(email=email, db=db)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_tocken=token, token_type="bearer")


async def get_current_user(
        db: orm.Session, token: str = fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = db.query(models.User).get(payload['id'])
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
    return schemas.User.from_orm(user)
