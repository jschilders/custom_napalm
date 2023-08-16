import os
import dotenv

# Load extra environment variables from .env file
dotenv.load_dotenv()

# Get variables from environment
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

