from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.database import Base


class Event(Base):
    """Model for storing game events from webhook."""
    
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False, index=True)
    event_name = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=True)
    click_power = Column(Integer, nullable=True)
    coins = Column(Integer, nullable=True)
    total_clicks = Column(Integer, nullable=True)
    payload = Column(JSON, nullable=True)
    
    # Processing status
    processed = Column(Boolean, default=False, index=True)
    processing = Column(Boolean, default=False, index=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Event(id={self.id}, user_email={self.user_email}, event_name={self.event_name}, processed={self.processed})>"
