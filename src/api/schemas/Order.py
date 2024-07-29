from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class Order(BaseModel):
    order_number: int

    model_config = SettingsConfigDict(extra='allow')
