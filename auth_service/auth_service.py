# auth_service/auth_service.py

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from dotenv import load_dotenv
import os
import hashlib

# Load environment variables
load_dotenv()

# Fetch credentials securely
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Validate environment variables
if not all([DB_USERNAME, DB_PASSWORD, DB_NAME]):
    raise EnvironmentError("❌ Missing one or more required environment variables: DB_USERNAME, DB_PASSWORD, DB_NAME")

# Encode special characters in password
encoded_password = DB_PASSWORD.replace("@", "%40")

# Construct database URL
DATABASE_URL = f"mysql+mysqlconnector://{DB_USERNAME}:{encoded_password}@localhost/{DB_NAME}"

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(200))
    interest = Column(String(100))
    user_type = Column(String(50), default="free")

# Password hashing utilities
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(raw_password: str, hashed: str) -> bool:
    return hash_password(raw_password) == hashed

# Create tables if they don't exist
def init_db():
    Base.metadata.create_all(engine)

# User management functions
def sign_up(name: str, email: str, password: str, interest: str, user_type: str = 'free') -> str:
    session = Session()
    try:
        if session.query(User).filter_by(email=email).first():
            return "❌ Email already registered."
        user = User(
            name=name,
            email=email,
            password=hash_password(password),
            interest=interest,
            user_type=user_type
        )
        session.add(user)
        session.commit()
        return "✅ User registered successfully."
    finally:
        session.close()

def sign_in(email: str, password: str):
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user and check_password(password, user.password):
            return user
        return None
    finally:
        session.close()
