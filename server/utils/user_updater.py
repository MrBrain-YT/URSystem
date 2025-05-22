import os
import secrets

import sqlalchemy as db

from databases.connection import users_table
from databases.database_manager import DBWorker

def update_user_info() -> dict:
    from API.accounts_manager import AccountManager
    users = {}
    query = users_table.select()
    rows = DBWorker().send_select_query(query).fetchall()
    for i in rows:
        users[i[0]] = {"password": i[1],
                "role": i[2],
                "token": i[3]
                }
    AccountManager().set_users(users)
    return users

def update_token() -> dict:
    users = update_user_info()
    tokens = []
    for i in [i for i in users]:
        tokens.append(users.get(i)["token"])
        
    while True:
        token = secrets.token_hex(32)
        if token not in tokens:
            break
    
    query = users_table.update().where(db.and_(users_table.columns.role == "System",
                users_table.columns.name == "",
                users_table.columns.password == "" 
                )).values(token=token)
    DBWorker.send_query(query)

    os.environ["SYSTEM_API_TOKEN"] = token
    return update_user_info()