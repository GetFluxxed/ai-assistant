import os 
from dotenv import load_dotenv  

# Configuration variables for the rest of project

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")

EMBEDDING_MODEL = "text-embedding-3-small"

EMBEDDING_DIMENSIONS = 1536