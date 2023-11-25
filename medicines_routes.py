from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from database import engine, Session
from schemas import SignUpModel, LoginModel
from models import User


medicines_router = APIRouter(
    prefix='/medicines',
    tags=['Medicines']
)