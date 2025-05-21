from typing import TypeVar
from typing import Any

import sqlalchemy as db

from databases.connection import conn

class DBWorker:
    
    @staticmethod
    def send_query(query) -> None:
        conn.execute(query)
        conn.commit()
    
    @staticmethod
    def send_select_query(query) -> db.CursorResult[TypeVar("_T", bound=Any)]:
        return conn.execute(query)