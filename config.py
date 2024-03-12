from dotenv import load_dotenv
import os

load_dotenv(".env")

db_name: str = os.getenv("db_name")
print(db_name)