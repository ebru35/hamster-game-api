from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PayloadSchema(BaseModel):
    """Event payload with game metrics."""
    
    click_power: Optional[int] = None
    coins: Optional[int] = None
    total_clicks: Optional[int] = None


class EventRequest(BaseModel):
    """Request schema for incoming events."""
    
    user_email: str = Field(..., description="User email address")
    event_name: str = Field(..., description="Type of event")
    timestamp: datetime = Field(..., description="Event timestamp")
    payload: PayloadSchema = Field(..., description="Event payload")


class EventResponse(BaseModel):
    """Response schema for API responses."""
    
    status: str
    event_id: int


class EventSchema(BaseModel):
    """Full event schema from database."""
    
    id: int
    user_email: str
    event_name: str
    timestamp: Optional[datetime] = None
    click_power: Optional[int] = None
    coins: Optional[int] = None
    total_clicks: Optional[int] = None
    payload: Optional[dict] = None
    processed: bool
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
