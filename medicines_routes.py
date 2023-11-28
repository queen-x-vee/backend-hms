from fastapi import APIRouter, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from database import engine, Session
from models import Medicines, User
from schemas import MedicineModel, MedicineQuantityModel
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
    

#update medicine quantity

@medicines_router.patch("/medicine/{id}", status_code=status.HTTP_200_OK)
async def update_medicine_quantity(id: int, medicine: MedicineQuantityModel, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        db__medicine = session.query(Medicines).filter(Medicines.id == id).first()
        db__medicine.quantity = medicine.quantity

        session.commit()

        response = {
            "message": "Medicine quantity updated successfully",
            "data": {
                "id": db__medicine.id,
                "medicine_name": db__medicine.medicine_name,
                "quantity": db__medicine.quantity,
            },
            "status": status.HTTP_200_OK}
        return response, status.HTTP_200_OK
    
    else:
        return{
            "message": "You are not authorized to perform this action",
            "status": status.HTTP_401_UNAUTHORIZED
        }


#update entire medicine
@medicines_router.put("/medicine/{id}", status_code=status.HTTP_200_OK)
async def update_medicine(id: int, medicine: MedicineModel, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        db__medicine = session.query(Medicines).filter(Medicines.id == id).first()

        db__medicine.medicine_name = medicine.medicine_name
        db__medicine.side_effects = medicine.side_effects
        db__medicine.how_to_use = medicine.how_to_use
        db__medicine.quantity = medicine.quantity
        db__medicine.group = medicine.group


        session.commit()

        response={
            "message": "Medicine updated successfully",
            "data": {
                "medicine_name": db__medicine.medicine_name,
                "side_effects": db__medicine.side_effects,
                "how_to_use": db__medicine.how_to_use,
                "quantity": db__medicine.quantity,
                "group": db__medicine.group,
                "id": db__medicine.id
            },
            "status": status.HTTP_200_OK}
        return response, status.HTTP_200_OK
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to update this medicine")




#delete medicine

@medicines_router.delete("/medicine/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicine(id: int, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    medicine_to_delete = session.query(Medicines).filter(Medicines.id == id).first()

    session.delete(medicine_to_delete)

    session.commit()

    return medicine_to_delete


            
    