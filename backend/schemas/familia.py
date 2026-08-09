from pydantic import BaseModel


class FamiliaCreate(BaseModel):
    nome_familia: str


class FamiliaPublic(BaseModel):
    id: int
    nome_familia: str

    class Config:
        from_attributes = True