from databases import DatabaseURL
from starlette.config import Config

# Read configuration variables from the environment or .env file
config = Config('.venv')

DEBUG = config('DEBUG', cast=bool, default=False)
PORT = config('PORT', cast=int)
LOCAL_STORAGE_PATH = config('LOCAL_STORAGE_PATH', cast=str)
REMOTE_STORAGE_PATH = config('REMOTE_STORAGE_PATH', cast=str)
DATABASE_URL = config('DATABASE_URL', cast=DatabaseURL)
