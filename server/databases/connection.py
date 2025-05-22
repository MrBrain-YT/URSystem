import sqlalchemy as db

engine = db.create_engine("sqlite:///databases/Users.sqlite")
conn = engine.connect() 
metadata = db.MetaData()
users_table = db.Table("users",metadata, autoload_with=engine)