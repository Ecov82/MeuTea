from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # O campo 'sub' (subject) é padrão em JWT para identificar o usuário.
    email: Optional[str] = None