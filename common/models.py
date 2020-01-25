"""
This file contains the database models that are used
to generate and access the database
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    mac_address = Column(String, unique=True)
    label = Column(String)

    heartbeats = relationship("Heartbeat", back_populates="device")
    services = relationship("Service", back_populates="device")
    fingerprints = relationship("Fingerprint", back_populates="device")
    vulnerabilities = relationship("Vulnerability", back_populates="device")
    ip_address = Column(String, index=True)
    hostname = Column(String)


class Heartbeat(Base):
    __tablename__ = 'heartbeats'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    device = relationship("Device", back_populates="heartbeats")


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    device = relationship("Device", back_populates="services")
    
    type = Column(String, index=True)
    address = Column(String, index=True)
    description = Column(String)

class Fingerprint(Base):
    __tablename__ = 'fingerprints'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    device = relationship("Device", back_populates="fingerprints")

    type = Column(String, index=True)
    value = Column(String, index=True)

class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    device = relationship("Device", back_populates="vulnerabilities")

    type = Column(String, index=True)
    description = Column(String, index=True)
