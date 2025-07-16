import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMINS = os.getenv("ADMINS")
ADMIN_LIST = [int(admin_id.strip()) for admin_id in ADMINS.split(",")]