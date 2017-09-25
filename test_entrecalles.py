from random import choice
import pandas as pd
from database.db import DbConnection
from database.conexiones import pfa_dgc_local

conn = DbConnection(pfa_dgc_local)
engine = conn.get_engine()
conn_alchemy = engine.connect()

q_cruces = '''
WITH calle AS (
    SELECT
      union_geom('{0}') AS geom
)
SELECT
  array_agg(nombre) AS puntos
FROM calles_geocod cg, calle c
WHERE
  (
    st_intersects(c.geom, cg.geom)
    OR
    st_touches(c.geom, cg.geom)
  )
AND
nombre != '{0}';
'''


def interseccion_random(calle):
    cruces = pd.read_sql(q_cruces.format(calle), engine)
    return choice(cruces.puntos[0])


def crear_entrecalles(calle):
    calle_principal = calle
    for _ in range(10):
        cruce1 = interseccion_random(calle)
        cruce2 = interseccion_random(calle)
        tabla = 'test_entrecalles.{}_{}_{}'.format(calle.replace(' ', '').replace(',', '').replace('.', ''),
                                                   cruce1.replace(' ', '').replace(',', '').replace('.', ''),
                                                   cruce2.replace(' ', '').replace(',', '').replace('.', ''))
        res = conn_alchemy.execute('''
            CREATE TABLE {} AS (
            SELECT 1 AS id, entrecalles('{}', '{}', '{}') AS geom);
        '''.format(tabla, calle_principal, cruce1, cruce2))
        print(res)



crear_entrecalles('ladines')
