from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    first_name: str
