from sqlalchemy import Column, String, Integer, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from backend.app.core.db import Base

def generate_uuid():
    return str(uuid.uuid4())

class Site(Base):
    __tablename__ = "sites"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    domain_url = Column(String(255), nullable=False, unique=True)
    brand_keywords = Column(String(1000), nullable=True) # Comma-separated brand names
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    charts = relationship("GSCDailyChart", back_populates="site", cascade="all, delete-orphan")
    queries = relationship("GSCQuery", back_populates="site", cascade="all, delete-orphan")
    pages = relationship("GSCPage", back_populates="site", cascade="all, delete-orphan")
    ga4_pages = relationship("GA4Page", back_populates="site", cascade="all, delete-orphan")

class GSCDailyChart(Base):
    __tablename__ = "gsc_daily_charts"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False)
    sync_date = Column(Date, nullable=False)
    clicks = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    avg_position = Column(Float, default=0.0)
    
    site = relationship("Site", back_populates="charts")
    
    __table_args__ = (
        UniqueConstraint("site_id", "sync_date", name="uq_site_date_chart"),
    )

class GSCQuery(Base):
    __tablename__ = "gsc_queries"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False)
    sync_date = Column(Date, nullable=False)
    query_text = Column(String(1000), nullable=False)
    clicks = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    avg_position = Column(Float, default=0.0)
    is_brand = Column(Boolean, default=False)
    
    site = relationship("Site", back_populates="queries")
    
    __table_args__ = (
        UniqueConstraint("site_id", "sync_date", "query_text", name="uq_site_date_query"),
    )

class GSCPage(Base):
    __tablename__ = "gsc_pages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False)
    sync_date = Column(Date, nullable=False)
    page_url = Column(String(2048), nullable=False)
    clicks = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    avg_position = Column(Float, default=0.0)
    
    site = relationship("Site", back_populates="pages")
    
    __table_args__ = (
        UniqueConstraint("site_id", "sync_date", "page_url", name="uq_site_date_page"),
    )

class GA4Page(Base):
    __tablename__ = "ga4_pages"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    site_id = Column(String(36), ForeignKey("sites.id", ondelete="CASCADE"), nullable=False)
    sync_date = Column(Date, nullable=False)
    page_url = Column(String(2048), nullable=False)
    pageviews = Column(Integer, default=0)
    sessions = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    bounce_rate = Column(Float, default=0.0)
    
    site = relationship("Site", back_populates="ga4_pages")
    
    __table_args__ = (
        UniqueConstraint("site_id", "sync_date", "page_url", name="uq_site_date_ga4_page"),
    )
