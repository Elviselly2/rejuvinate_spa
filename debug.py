from sqlalchemy.orm import Session
from lib.config import SessionLocal
from lib.models.service import Service
from lib.models.appointment import Appointment
from lib.models.payment import Payment
from lib.models.inventory import Inventory
from datetime import datetime
import sys
sys.path.append(".")

from lib.models.customer import Customer


# Initialize database session
db = SessionLocal()

# Function to test customer queries
def test_customers():
    print("\n🔍 Testing Customer Queries")
    customer = db.query(Customer).first()
    print("First Customer:", customer.name if customer else "No customers found.")

# Function to test service queries
def test_services():
    print("\n🔍 Testing Service Queries")
    services = db.query(Service).all()
    for service in services:
        print(f"- {service.name}: ${service.price}")

# Function to test appointments
def test_appointments():
    print("\n🔍 Testing Appointments")
    upcoming = db.query(Appointment).filter(Appointment.scheduled_time > datetime.now()).all()
    print(f"Upcoming Appointments: {len(upcoming)}")

# Function to test payments
def test_payments():
    print("\n🔍 Testing Payments")
    payments = db.query(Payment).all()
    for payment in payments:
        print(f"- Payment ID {payment.id}: ${payment.amount}")

# Function to test inventory stock
def test_inventory():
    print("\n🔍 Testing Inventory Stock")
    inventory_items = db.query(Inventory).all()
    for item in inventory_items:
        print(f"- {item.product_name}: {item.quantity} in stock")

# Run all debug functions
if __name__ == "__main__":
    test_customers()
    test_services()
    test_appointments()
    test_payments()
    test_inventory()

    print("\n✅ Debugging complete!")
