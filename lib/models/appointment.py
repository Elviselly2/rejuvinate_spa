from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from lib.base import Base
from lib.models.customer import Customer
from lib.models.service import Service
from lib.models.staff import Staff

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Store appointment creation timestamp
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Track modifications

    customer = relationship("Customer")
    service = relationship("Service")
    staff = relationship("Staff")

    @classmethod
    def book_appointment(cls, db: Session, customer_id: int, service_id: int, staff_id: int, scheduled_time: datetime):
        """Schedules a new appointment."""
        if scheduled_time < datetime.utcnow():
            raise ValueError("Scheduled time must be in the future!")

        appointment = cls(
            customer_id=customer_id, 
            service_id=service_id, 
            staff_id=staff_id, 
            scheduled_time=scheduled_time,
            created_at=datetime.utcnow
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    @classmethod
    def cancel_appointment(cls, db: Session, appointment_id: int):
        """Cancels an appointment by removing it from the database."""
        appointment = db.query(cls).filter(cls.id == appointment_id).first()
        if not appointment:
            raise ValueError("Appointment not found!")
        
        db.delete(appointment)
        db.commit()
        return {"message": "Appointment successfully canceled."}

    @classmethod
    def get_upcoming_appointments(cls, db: Session, customer_id: int):
        """Retrieves all upcoming appointments for a customer."""
        return db.query(cls).filter(cls.customer_id == customer_id, cls.scheduled_time > datetime.utcnow()).all()
