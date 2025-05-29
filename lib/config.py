from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Import all models
from lib.models.customer import Customer
from lib.models.service import Service
from lib.models.appointment import Appointment
from lib.models.payment import Payment
from lib.models.inventory import Inventory
from lib.models.staff import Staff
from lib.models.service_inventory import ServiceInventory
from lib.models.appointment_inventory import AppointmentInventory

engine = create_engine('sqlite:///rejuvenate_spa.db', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


Base.metadata.create_all(bind=engine)
