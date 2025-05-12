from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'rol'

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

def table_fetchall():
    sql = f'''
        SELECT 
            r.*, tr.nombre AS nom_tiporol
        FROM {table_name} r
        LEFT JOIN tipo_rol tr ON r.tipo_rolid = tr.id
    '''
    return sql_select_fetchall(sql)

def get_table():
    sql = f'''
        SELECT 
            r.id,
            r.nombre,
            r.descripcion,
            r.activo,
            r.tipo_rolid,
            tr.nombre AS nom_tiporol
        FROM {table_name} r
        INNER JOIN tipo_rol tr ON r.tipo_rolid = tr.id
    '''
    columnas = {
        'id': ['ID', 0.5],
        'nombre': ['Nombre del Rol', 1.5],
        'descripcion': ['Descripción', 2],
        'nom_tiporol': ['Tipo de Rol', 1.5],
        'activo': ['Activo', 0.5]
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas

def unactive_row(id):
    unactive_row_table(table_name, id)

def insert_row(nombre, descripcion, tipo_rolid):
    sql = f'''
        INSERT INTO {table_name} (nombre, descripcion, activo, tipo_rolid)
        VALUES (%s, %s, 1, %s)
    '''
    sql_execute(sql, (nombre, descripcion, tipo_rolid))

def update_row(id, nombre, descripcion, tipo_rolid):
    sql = f'''
        UPDATE {table_name}
        SET nombre = %s,
            descripcion = %s,
            tipo_rolid = %s
        WHERE id = {id}
    '''
    sql_execute(sql, (nombre, descripcion, tipo_rolid))



def get_options():
    sql= f'''
        select 
            {get_primary_key()} ,
            nombre
        from {table_name}
        where activo = 1
        order by nombre asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila[get_primary_key()], fila["nombre"]) for fila in filas]

    return lista