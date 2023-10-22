from pydantic import BaseModel, EmailStr

class UserRegistrationRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str
    profile_picture: str

class UserResponse(BaseModel):
    user_id: str
    full_name: str
    email: str
    phone: str
    profile_picture: str