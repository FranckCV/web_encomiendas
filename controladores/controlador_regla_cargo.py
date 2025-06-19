from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd


def get_condiciones_tarifa():
    sql = '''
        SELECT tipo_condicion, inferior, superior, porcentaje
        FROM regla_cargo
    '''
    return sql_select_fetchall(sql)


def get_max_valor():
    sql = '''
        SELECT max(superior) as valor_max
        FROM regla_cargo
    '''
    row = sql_select_fetchone(sql)
    
    return row['valor_max'] if row and row.get('valor_max') is not None else 0
def get_regla_cargo_condicion( tipo_condicion , valor ):
    sql = '''
        SELECT `id`, `tipo_condicion`, `inferior`, `superior`, `porcentaje` 
        FROM `regla_cargo` 
        WHERE tipo_condicion = %s and 
        (inferior <= %s and %s <= superior) or 
        (inferior <= %s and superior is NULL) or 
        (inferior is NULL and %s <= superior)
    '''
    return sql_select_fetchone(sql,(tipo_condicion , valor , valor , valor , valor))




def get_rango():

    sql = """
      SELECT inferior, superior
      FROM regla_cargo
      WHERE tipo_condicion = 'V'
    """
    filas = sql_select_fetchall(sql)
    # filas viene como [{ 'inferior': x, 'superior': y }, …]
    return [(f['inferior'], f['superior']) for f in filas]

def get_porcentaje_peso():

    sql = """
      SELECT porcentaje
      FROM regla_cargo
      WHERE tipo_condicion = 'P'
      LIMIT 1
    """
    fila = sql_select_fetchone(sql)
    return fila['porcentaje'] if fila and 'porcentaje' in fila else None
