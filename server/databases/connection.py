import sys

import sqlalchemy as db

print("pytest" in sys.modules)
if "pytest" in sys.modules:
    engine = db.create_engine("sqlite:///databases/auto_test/users.sqlite")
else:
    engine = db.create_engine("sqlite:///databases/users.sqlite")
conn = engine.connect() 
metadata = db.MetaData()
users_table = db.Table("users",metadata, autoload_with=engine)