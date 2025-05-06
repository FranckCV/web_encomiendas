from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'empleado'

def get_info_columns():
    return show_columns(table_name)

def get_primary_key():
    return show_primary_key(table_name)

def exists_Activo():
    return exists_column_Activo(table_name)

def delete_row(id):
    bd.delete_row_table(table_name, id)

#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql = f'''
        SELECT 
            usuarioid,
            nombre,
            ape_paterno,
            ape_materno,
            cargoid
        FROM {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    return resultados

def get_table():
    sql = f'''
        SELECT 
            emp.usuarioid,
            emp.nombre,
            emp.ape_paterno,
            emp.ape_materno,
            emp.cargoid
        FROM {table_name} emp
    '''
    columnas = {
        'usuarioid': ['Usuario ID', 1],
        'nombre': ['Nombre', 2],
        'ape_paterno': ['Apellido Paterno', 3],
        'ape_materno': ['Apellido Materno', 3],
        'cargoid': ['Cargo ID', 1]
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas

######_ CAMBIAR PARAMETROS Y SQL INTERNO _######

def unactive_row(id):
    unactive_row_table(table_name, id)

def insert_row(nombre, ape_paterno, ape_materno, cargoid, usuarioid):
    sql = f'''
        INSERT INTO 
            {table_name} (usuarioid, nombre, ape_paterno, ape_materno, cargoid)
        VALUES 
            (%s, %s, %s, %s, %s)
    '''
    sql_execute(sql, (usuarioid, nombre, ape_paterno, ape_materno, cargoid))

def update_row(usuarioid, nombre, ape_paterno, ape_materno, cargoid):
    sql = f'''
        UPDATE {table_name} SET 
            nombre = %s,
            ape_paterno = %s,
            ape_materno = %s,
            cargoid = %s
        WHERE {get_primary_key()} = {usuarioid}
    '''
    sql_execute(sql, (nombre, ape_paterno, ape_materno, cargoid))

#####_ ADICIONALES _#####

def get_options_empleado():
    sql = f'''
        SELECT 
            usuarioid,
            CONCAT(nombre, ' ', ape_paterno, ' ', ape_materno) AS nombre_completo
        FROM {table_name}
        ORDER BY nombre ASC
    '''
    filas = sql_select_fetchall(sql)
    lista = [(fila["usuarioid"], fila["nombre_completo"]) for fila in filas]
    return lista