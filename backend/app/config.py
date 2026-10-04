import os
from dotenv import load_dotenv

load_dotenv()

# SQLite is used by default so the project runs without XAMPP/MySQL.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB = os.path.join(BASE_DIR, "endpoint_support.db")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB}")

CORS_ORIGINS = [
    item.strip()
    for item in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")
    if item.strip()
]
