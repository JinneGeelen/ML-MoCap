import databases
import logging

from starlette.applications import Starlette
from starlette.datastructures import Secret
from starlette.schemas import SchemaGenerator

from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.cors import CORSMiddleware

from api import cameras, diagnostic_results, diagnostics, participants, recordings, studies
from db import get_db, init_tables
from controllers import camera_controller
from config import DEBUG, DATABASE_URL


# Set up logging level globally
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

# Main application code
db = get_db(DATABASE_URL)
app = Starlette()
app.debug = DEBUG

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

# Mount all the different API's
app.mount('/api/cameras', cameras)
app.mount('/api/diagnostic_results', diagnostic_results)
app.mount('/api/diagnostics', diagnostics)
app.mount('/api/participants', participants)
app.mount('/api/recordings', recordings)
app.mount('/api/studies', studies)


# Set up OpenAPI schema
schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "ML-MoCap Controller API", "version": "1.0"}}
)


@app.route("/schema", methods=["GET"], include_in_schema=False)
def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)

# Set up the connection to database on startup and shutdown of the application


@app.on_event("startup")
async def startup():
    await init_tables('{}'.format(DATABASE_URL))
    await db.connect()
    await camera_controller.reset_status()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
