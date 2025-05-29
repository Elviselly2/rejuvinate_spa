from sqlalchemy.orm import Session
from lib.config import SessionLocal, engine
from lib.base import Base
from lib.models.customer import Customer
from lib.models.service import Service
from lib.models.staff import Staff
from lib.models.appointment import Appointment
from lib.models.payment import Payment
from lib.models.inventory import Inventory
from lib.models.service_inventory import ServiceInventory
from lib.models.appointment_inventory import AppointmentInventory
from datetime import datetime

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

# Function to seed the database
def seed_data():
    db = SessionLocal()  # Initialize the database session

    # Clears existing data before seeding
    db.query(Customer).delete()
    db.query(Service).delete()
    db.query(Staff).delete()
    db.query(Appointment).delete()
    db.query(Payment).delete()
    db.query(Inventory).delete()
    db.query(ServiceInventory).delete()
    db.query(AppointmentInventory).delete()
    db.commit()

    # 1️⃣ Add Customers
    customers = [
        Customer(name="Alice Johnson", email="alice@gmail.com", phone="1234567890"),
        Customer(name="Bob Smith", email="bob@gmail.com", phone="0987654321"),
        Customer(name="Charlie Brown", email="charlie@gmail.com", phone="1122334455"),
        Customer(name="Diana Prince", email="diana@gmail.com", phone="2233445566")
    ]

    # 2️⃣ Add Services
    services = [
        Service(name="Swedish Massage", description="Relaxing full-body massage", price=50.0),
        Service(name="Facial Treatment", description="Deep skin cleansing and hydration", price=75.0),
        Service(name="Hot Stone Therapy", description="Therapeutic heat therapy for muscle relief", price=90.0),
        Service(name="Aromatherapy", description="Essential oil-based massage for relaxation", price=60.0)
    ]

    # 3️⃣ Add Staff
    staff_members = [
        Staff(name="Emma Davis", role="Therapist"),
        Staff(name="John Doe", role="Receptionist"),
        Staff(name="Sophie Turner", role="Therapist"),
        Staff(name="Chris Evans", role="Manager")
    ]

    # 4️⃣ Add Inventory
    inventory_items = [
        Inventory(product_name="Lavender Massage Oil", quantity=20),
        Inventory(product_name="Facial Cleanser", quantity=15),
        Inventory(product_name="Hot Stones", quantity=10),
        Inventory(product_name="Essential Oils Set", quantity=25)
    ]

    # 5️⃣ Add Sample Appointments
    appointments = [
        Appointment(customer_id=1, service_id=1, staff_id=1, scheduled_time=datetime(2025, 5, 28, 10, 0)),
        Appointment(customer_id=2, service_id=2, staff_id=2, scheduled_time=datetime(2025, 5, 29, 14, 0)),
        Appointment(customer_id=3, service_id=3, staff_id=3, scheduled_time=datetime(2025, 5, 30, 12, 0)),
        Appointment(customer_id=4, service_id=4, staff_id=4, scheduled_time=datetime(2025, 5, 31, 9, 0))
    ]

    # 6️⃣ Add Payments
    payments = [
        Payment(customer_id=1, appointment_id=1, amount=50.0, payment_date=datetime.now()),
        Payment(customer_id=2, appointment_id=2, amount=75.0, payment_date=datetime.now()),
        Payment(customer_id=3, appointment_id=3, amount=90.0, payment_date=datetime.now()),
        Payment(customer_id=4, appointment_id=4, amount=60.0, payment_date=datetime.now())
    ]

    # 7️⃣ Associate Services with Inventory
    service_inventory_links = [
        ServiceInventory(service_id=1, inventory_id=1, quantity_used=2),
        ServiceInventory(service_id=2, inventory_id=2, quantity_used=1),
        ServiceInventory(service_id=3, inventory_id=3, quantity_used=4),
        ServiceInventory(service_id=4, inventory_id=4, quantity_used=3)
    ]

    # 8️⃣ Track Inventory Usage in Appointments
    appointment_inventory_links = [
        AppointmentInventory(appointment_id=1, inventory_id=1, quantity_used=2),
        AppointmentInventory(appointment_id=2, inventory_id=2, quantity_used=1),
        AppointmentInventory(appointment_id=3, inventory_id=3, quantity_used=4),
        AppointmentInventory(appointment_id=4, inventory_id=4, quantity_used=3)
    ]

    # Add all data to session and commit
    db.add_all(customers + services + staff_members + inventory_items + appointments + payments + service_inventory_links + appointment_inventory_links)
    db.commit()
    db.close()

    print("✅ Database seeded successfully!")

# Run the seed function
if __name__ == "__main__":
    seed_data()
