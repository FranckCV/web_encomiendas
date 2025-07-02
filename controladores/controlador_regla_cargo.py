from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd

table_name = 'regla_cargo'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( id ):
    bd.delete_row_table(table_name , id)


#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql= f'''
        select 
            *
        from {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    
    return resultados


def get_table():
    sql= f'''
        SELECT 
            id, 
            tipo_condicion, 
            inferior, 
            superior, 
            porcentaje 
        FROM regla_cargo
    '''
    columnas = {
        'id': ['ID' , 0.5 ] , 
        'tipo_condicion' : ['Tipo de condición' , 3 ] , 
        'inferior' : ['Inferior' , 3.5] , 
        'superior' : ['Superior' , 3.5] , 
        'porcentaje' : ['Porcentaje' , 3.5] , 
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas









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
        SELECT id, tipo_condicion, inferior, superior, porcentaje 
        FROM regla_cargo 
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
