from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from lib.base import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Track when staff is registered
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Track modifications

    @classmethod
    def register_staff(cls, db: Session, name: str, role: str):
        """Registers a new staff member."""
        if not name or not role:
            raise ValueError("Name and role must be provided!")

        staff = cls(name=name, role=role, created_at=datetime.utcnow)
        db.add(staff)
        db.commit()
        db.refresh(staff)  # ✅ Ensure latest data is retrieved
        return {"message": "Staff registered successfully!", "staff": staff}

    @classmethod
    def get_staff_by_role(cls, db: Session, role: str):
        """Retrieves all staff members with a specific role."""
        staff_members = db.query(cls).filter(cls.role == role).all()
        if not staff_members:
            raise ValueError(f"No staff found with role: {role}")
        return staff_members

    @classmethod
    def update_role(cls, db: Session, staff_id: int, role: str):
        """Updates the role of a staff member."""
        if not role:
            raise ValueError("Role must be provided!")

        staff = db.query(cls).filter(cls.id == staff_id).first()
        if not staff:
            raise ValueError("Staff member not found.")

        staff.role = role
        staff.updated_at = datetime.utcnow  # ✅ Apply timestamp update
        db.commit()
        db.refresh(staff)  # ✅ Ensure updated timestamp is applied
        return {"message": "Staff role updated successfully!", "staff": staff}
