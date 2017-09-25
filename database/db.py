from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


class DbConnection:
    def __init__(self, conn_str: str):
        self._connection_string = conn_str

    def get_engine(self):
        engine = None
        try:
            engine = create_engine(self._connection_string)
            engine.connect()
        except OperationalError as e:
            print(e.args)
        return engine
