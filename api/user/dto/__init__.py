from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserCreateDTO(UserBase):
    password_hash: str
    
class UserResponseDTO(UserBase):
    user_id: int
