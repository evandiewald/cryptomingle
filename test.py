import database
import config
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

db = create_engine(config.DB_STRING)
conn = db.connect()

session = Session(db)
table = database.users_table(db)

print(database.get_next_id(session, table))