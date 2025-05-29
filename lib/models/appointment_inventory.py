from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship
from datetime import datetime
from lib.base import Base
from lib.models.inventory import Inventory

class AppointmentInventory(Base):
    __tablename__ = "appointment_inventory"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    quantity_used = Column(Integer, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Store timestamp when entry is created
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Update timestamp when modified

    appointment = relationship("Appointment")
    inventory = relationship("Inventory")

    @classmethod
    def record_inventory_usage(cls, db: Session, appointment_id: int, inventory_id: int, quantity_used: int):
        """Records inventory usage in an appointment with timestamps."""
        appointment_inventory = cls(
            appointment_id=appointment_id,
            inventory_id=inventory_id,
            quantity_used=quantity_used,
            created_at=datetime.utcnow
        )
        db.add(appointment_inventory)
        db.commit()
        db.refresh(appointment_inventory)
        return appointment_inventory

    @classmethod
    def deduct_inventory(cls, db: Session, inventory_id: int, quantity_used: int):
        """Deducts inventory stock from the Inventory table."""
        inventory_item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
        
        if not inventory_item:
            raise ValueError("Inventory item not found!")
        
        if inventory_item.quantity < quantity_used:
            raise ValueError("Not enough stock available!")

        inventory_item.quantity -= quantity_used  # Deduct from inventory stock
        inventory_item.updated_at = datetime.utcnow  #  Update timestamp
        db.commit()
        db.refresh(inventory_item)
        return inventory_item
