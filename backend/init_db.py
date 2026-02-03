from database import engine, Base
from models import User, Wallet

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")

if __name__ == "__main__":
    create_tables()
