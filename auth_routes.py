from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from database import engine, Session
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


auth_router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

session = Session(bind=engine)

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(user: SignUpModel):
    #check if email exists
    db_email= session.query(User).filter(User.email == user.email).first()
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    #create a new user
    new_user = User(username=user.username,
                    email=user.email, 
                    password=generate_password_hash(user.password),
                    is_staff=user.is_staff,
                    is_active=user.is_active
    )

    session.add(new_user)
    session.commit()
    return new_user

    
    
