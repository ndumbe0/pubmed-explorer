from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base

class PubmedPaper(Base):
    __tablename__ = "pubmed_papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    doi = Column(String, index=True)
    abstract = Column(Text)
    journal = Column(String, index=True)
    date = Column(String)
    published_date = Column(String)
    authors = Column(Text)  # stored as JSON string or text
    year = Column(Integer, index=True)
    keyword = Column(Text)
    source_file = Column(String)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())
    content_hash = Column(String, index=True)
