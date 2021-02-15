from tinydb import TinyDB, Query
from globals import CWD

db = TinyDB(CWD / "scripts" / "database" / "db.json")
