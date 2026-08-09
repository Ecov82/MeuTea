from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    familia_id: int


class UsuarioPublic(BaseModel):
    id: int
    nome: str
    email: EmailStr
    familia_id: int

    class Config:
        from_attributes = True