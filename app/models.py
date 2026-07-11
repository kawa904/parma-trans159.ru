from pydantic import BaseModel, Field
from datetime import datetime

class OrderRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., pattern=r'^\+?[0-9]{10,15}$')
    message: str = Field(..., min_length=5, max_length=1000)
    consent: bool = Field(..., description="Согласие на обработку ПД")
    consent_ads: bool = Field(False, description="Согласие на рекламные звонки")
    timestamp: datetime = Field(default_factory=datetime.now)

class OrderDB(OrderRequest):
    ip: str
    user_agent: str