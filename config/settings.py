import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve values from .env
ASTRA_DEVOPS_API_TOKEN = os.getenv("ASTRA_DEVOPS_API_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
