from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import null, text


class Message(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=True, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)