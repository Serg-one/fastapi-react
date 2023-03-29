import fastapi
import fastapi.security as security

import sqlalchemy.orm as orm

import services
import schemas


app = fastapi.FastAPI()


@app.post("/api/users")
async def create_user(user: schemas.UserCreate, 
                      db: orm.Session = fastapi.Depends(services.get_db)):
    if await services.get_db_user_by_email(user.email, db):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Email already use!"
        )
    return await services.create_user(user, db)


@app.post("/api/token")
async def generate_token(
        form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
        db: orm.Session = fastapi.Depends(services.get_db)
        ):
    user = await services.authenticate_user(
                        form_data.username,
                        form_data.password,
                        db
                 )
    if not user:
        raise fastapi.HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    return await services.create_token(user)


@app.get("/api/users/me", response_model=schemas.User)
async def get_user(
        user: schemas.User = fastapi.Depends(services.get_current_user)
        ):
    return user
