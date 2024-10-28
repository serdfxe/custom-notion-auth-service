from pydantic import BaseModel, EmailStr

        
class TokenRequestDTO(BaseModel):
    email: EmailStr
    password_hash: str

class TokenResponseDTO(BaseModel):
    access_token: str   
    token_type: str = "baerer"
