import pandas as pd
from database.db import DbConnection
from database.conexiones import pfa_dgc_server

conn = DbConnection(pfa_dgc_server)
engine = conn.get_engine()
print(pd.read_sql('select * from hechos limit 10;', engine))