from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'metodo_pago'

def get_info_columns():
    return show_columns(table_name)

def get_primary_key():
    return show_primary_key(table_name)

def exists_Activo():
    return exists_column_Activo(table_name)

def delete_row(id):
    sql = f'''
        DELETE FROM {table_name}
        WHERE id = {id}
    '''
    sql_execute(sql)

#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql = f'''
        SELECT 
            *
        FROM {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    return resultados

def get_table():
    sql = f'''
        SELECT 
            mp.id,
            mp.nombre,
            mp.activo
        FROM {table_name} mp
    '''
    columnas = {
        'id': ['ID', 1],
        'nombre': ['Nombre', 5],
        'activo': ['Activo', 1]
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas

######_ CRUD ESPECIFICAS _###### 

def unactive_row(id):
    unactive_row_table(table_name, id)

def insert_row(nombre):
    sql = f'''
        INSERT INTO 
            {table_name} 
            (nombre, activo)
        VALUES 
            (%s, 1)
    '''
    sql_execute(sql, (nombre,))

def update_row(id, nombre):
    sql = f'''
        UPDATE {table_name} SET 
            nombre = %s
        WHERE {get_primary_key()} = {id}
    '''
    sql_execute(sql, (nombre,))

#####_ ADICIONALES _#####

def get_options():
    sql = f'''
        SELECT 
            {get_primary_key()},
            nombre
        FROM {table_name}
        WHERE activo = 1
        ORDER BY nombre ASC
    '''
    filas = sql_select_fetchall(sql)
    # lista = [(fila['id'], fila["nombre"]) for fila in filas]
    return filas




def get_metodo_pago_online():
    sql = '''
        select id,nombre from metodo_pago where id != 1
    '''
    filas = sql_select_fetchall(sql)
    return filas