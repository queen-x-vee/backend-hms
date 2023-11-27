from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from database import engine, Session
from models import Medicines, User
from schemas import MedicineModel
from models import User


medicines_router = APIRouter(
    prefix='/medicines',
    tags=['Medicines']
)

session = Session(bind=engine)

@medicines_router.post("/medicine", status_code=status.HTTP_201_CREATED)
async def create_medicine(medicine: MedicineModel, Authorize:AuthJWT = Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    #current_user = session.query(User).filter(User.username == medicine.username).first()

    current_user=Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    new_order = Medicines(
        medicine_name = medicine.medicine_name,
        quantity = medicine.quantity,
        side_effects = medicine.side_effects,
        how_to_use = medicine.how_to_use,
        group = medicine.group
    )

    #now attach the order to the user if user is not a staff
    if not user.is_staff:
        new_order.user = user
   

    #save this with session

    session.add(new_order)

    session.commit()

    response={
        "message": "Medicine added successfully",
    }
    

   

    return response, status.HTTP_201_CREATED


@medicines_router.get("/medicine", status_code=status.HTTP_200_OK)
async def get_medicines(Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    medicines = session.query(Medicines).all()

    return {
        "data": medicines,
        "status": status.HTTP_200_OK
    }

@medicines_router.get("/medicine/{id}", status_code=status.HTTP_200_OK)
async def get_medicine(id: int, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    db__medicine = session.query(Medicines).filter(Medicines.id == id).first()

    if db__medicine is None:
        return {
            "message": "Medicine not found",
            "status": status.HTTP_404_NOT_FOUND
        }
    else:
        return {
            "data": db__medicine,
            "status": status.HTTP_200_OK
        }
    

