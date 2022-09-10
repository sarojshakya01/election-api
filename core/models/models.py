import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, Integer, Float, Boolean, JSON, Enum, DateTime
from .database import Base


class View(Table):
    is_view = True


class ElectionFResult(Base):
    __tablename__ = "ds_election_fresults"
    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, nullable=False)
    district_id = Column(String(50), nullable=False)
    type = Column(Enum('federal', 'provincial'),
                  default='federal',
                  nullable=False)
    region_id = Column(Float, nullable=False)
    declared = Column(Boolean, default=False)
    result = Column(JSON)
    elected = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)


class ElectionPResult(Base):
    __tablename__ = "ds_election_presults"
    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, nullable=False)
    district_id = Column(String(50), nullable=False)
    type = Column(Enum('federal', 'provincial'),
                  default='federal',
                  nullable=False)
    region_id = Column(Float, nullable=False)
    declared = Column(Boolean, default=False)
    result = Column(JSON)
    elected = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)


class District(Base):
    __tablename__ = "ds_election_districts"
    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(
        Integer,
        ForeignKey("provinces.province_id"),
        nullable=False,
    )
    district_id = Column(String(50), nullable=False)

    name_np = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)


class Province(Base):
    __tablename__ = "ds_election_provinces"
    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, nullable=False)
    name_np = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)


class FederalResult(View):
    is_view = True
    __tablename__ = "ds_v_federal_results"
    provinces = Column(JSON)


class FederalResult(View):
    is_view = True
    __tablename__ = "ds_v_provincial_results"
    provinces = Column(JSON)