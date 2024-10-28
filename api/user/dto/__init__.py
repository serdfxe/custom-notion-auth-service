from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    
class UserCreateDTO(UserBase):
    password_hash: str
    
class UserResponseDTO(UserBase):
    user_id: int
