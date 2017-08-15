import pandas as pd
from database.db import DbConnection
from database.conexiones import pfa_dgc_local

conn = DbConnection(pfa_dgc_local)
engine = conn.get_engine()
print(pd.read_sql('select * from hechos limit 10;', engine))