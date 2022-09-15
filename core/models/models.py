import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Float, Boolean, JSON, Enum, DateTime
from .database import Base


class View(Table):
    is_view = True

class ElectionFResult(Base):
    __tablename__ = "ds_election_fresults"
    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, nullable=False)
    district_id = Column(String(50), nullable=False)
    region_id = Column(Float, nullable=False)
    rtype = Column(
        Enum('federal', 'provincial'),
        default='federal',
        nullable=False
    )
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
    region_id = Column(Float, nullable=False)
    rtype = Column(
        Enum('federal', 'provincial'),
        default='federal',
        nullable=False
    )
    declared = Column(Boolean, default=False)
    result = Column(JSON)
    elected = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)


class Region(Base):
    __tablename__ = "ds_election_regions"
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(
        Integer,
        index=True,
        nullable=False,
    )
    district_id = Column(
        String(50),
        ForeignKey("districts.district_id"),
        nullable=False)
    province_id = Column(
        Integer,
        ForeignKey("provinces.province_id"),
        nullable=False,
    )
    rtype = Column(
        Enum('federal', 'provincial'),
        default='federal',
        nullable=False
    )

    name_np = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

class District(Base):
    __tablename__ = "ds_election_districts"
    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(String(50), nullable=False)
    province_id = Column(
        Integer,
        ForeignKey("provinces.province_id"),
        nullable=False,
    )
    name_np = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    total_fregions = Column(Integer, nullable=False)
    total_pregions = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)


class Province(Base):
    __tablename__ = "ds_election_provinces"
    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, nullable=False)
    name_np = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    color = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

class Party(Base):
    __tablename__ = "ds_election_parties"
    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, nullable=False)
    code = Column(String(20), nullable=False)
    name_np = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    short_name_np = Column(String(100))
    short_name_en = Column(String(100))
    color = Column(String(10))
    symbol = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, onupdate=datetime.datetime.utcnow)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class FederalResult(View):
    is_view = True
    __tablename__ = "ds_v_federal_results"
    provinces = Column(JSON)


class FederalResult(View):
    is_view = True
    __tablename__ = "ds_v_provincial_results"
    provinces = Column(JSON)


class PDRegions(View):
    is_view = True
    __tablename__ = "ds_v_province_district_regions"
    district = Column(JSON)