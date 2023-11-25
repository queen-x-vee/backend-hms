from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
     id: Optional[int]
     username: str
     email: str
     password: str
     is_staff:Optional[bool]
     is_active: Optional[bool]
     #orders = relationship("Order", back_populates="user")
     #sqlalchemy is the orm in this project

     class Config:
          orm_mode = True
          schema_extra = {
               "example": {
                    "username": "test",
                    "email": "test@email.com",
                    "password": "password",
                    "is_staff": True,
                    "is_active": True,
               }
          }


#class Settings(BaseModel):
   #  authjwt_secret_key: str='a0076b92217c27dd15701b85280212aa99fb52c0c48011a42b7f8081eed92a97' #to generate this toke, open terminal and type python, then import secrets, then secrets.token_hex()


class LoginModel(BaseModel):
     username: str
     password: str


class MedicineModel(BaseModel):
     id: Optional[int]
     medicine_name: str
     quantity: int
     side_effects:str
     how_to_use:str
     order_status: Optional[str]="PENDING"
     group: Optional[str]="OTC"
     user_id: Optional[int]


     class Config:
          orm_mode = True
          schema_extra = {
               "example": {
                    "medicine_name": "paracetamol",
                    "side_effects": "headache",
                    "how_to_use": "take with water",
                    "quantity": 2,
                    "group": "POM",
               }
          }



class OrderStatusModel(BaseModel):
     order_status: Optional[str]="PENDING"

     class Config:
          orm_mode = True
          schema_extra = {
               "example": {
                    "order_status": "PENDING"
               }
          }