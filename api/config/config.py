from databases import DatabaseURL
from starlette.config import Config

# Read configuration variables from the environment or .env file
config = Config('.venv')

DEBUG = config('DEBUG', cast=bool, default=False)
STORAGE_PATH = config('STORAGE_PATH', cast=str)
DATABASE_URL = config('DATABASE_URL', cast=DatabaseURL)
