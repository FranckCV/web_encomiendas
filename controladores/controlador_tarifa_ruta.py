from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'tarifa_ruta'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( sucursal_origen_id , sucursal_destino_id ):
    sql = f'''
        delete from tarifa_ruta
        where sucursal_origen_id = {sucursal_origen_id} and sucursal_destino_id = {sucursal_destino_id}
    '''
    sql_execute(sql)


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
    sql = '''
        SELECT 
            tr.sucursal_origen_id,
            tr.sucursal_destino_id,
            so.abreviatura AS sucursal_origen,
            sd.abreviatura AS sucursal_destino,
            tr.tarifa
        FROM 
            tarifa_ruta tr
        INNER JOIN sucursal so ON so.id = tr.sucursal_origen_id
        INNER JOIN sucursal sd ON sd.id = tr.sucursal_destino_id;
    '''

    columnas = {
        'sucursal_origen': ['Sucursal Origen', 2],
        'sucursal_destino': ['Sucursal Destino', 2],
        'tarifa': ['Tarifa (S/)', 1.5]
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas



######_ CRUD ESPECIFICAS _###### 

def unactive_row(id):
    unactive_row_table("sucursal", id)


def insert_row(sucursal_origen_id, sucursal_destino_id, tarifa):
    sql = '''
        INSERT INTO tarifa_ruta (sucursal_origen_id, sucursal_destino_id, tarifa)
        VALUES (%s, %s, %s)
    '''
    sql_execute(sql, (sucursal_origen_id, sucursal_destino_id, tarifa))


def update_row(sucursal_origen_id, sucursal_destino_id, tarifa):
    sql = '''
        UPDATE tarifa_ruta
        SET tarifa = %s
        WHERE sucursal_origen_id = %s AND sucursal_destino_id = %s
    '''
    sql_execute(sql, (tarifa, sucursal_origen_id, sucursal_destino_id))


#####_ ADICIONALES _#####


