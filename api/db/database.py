from databases import Database
from sqlalchemy import create_engine, MetaData


metadata = MetaData()

_db = None

def get_db(url = None):
  global _db
  if url:
    if _db:
      _db.disconnect()
    _db = Database(url)

  return _db

async def init_tables(url):
  engine = create_engine(url)
  # metadata.drop_all(bind=engine)
  metadata.create_all(bind=engine, checkfirst=True)
