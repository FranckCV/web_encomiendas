from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'motivo_reclamo'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where id = {id}
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
    sql= f'''
        select 
            mo.id ,
            mo.nombre ,
            mo.descripcion,
            tip.nombre as nom_tip 
        from {table_name} mo
        inner join tipo_reclamo tip on tip.id = mo.tipo_reclamoid
        order by mo.id asc
    '''
    columnas = {
        'id': ['ID' , 0.5 ] , 
        'nombre' : ['Nombre' , 3] , 
        'descripcion' : ['descripcion' , 3] , 
        'nom_tip' : ['Tipo de Reclamo' , 3],
    }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row(id):
    unactive_row_table({table_name}, id)


def insert_row(nombre, descripcion , tipo_reclamoid):
    sql = f'''
        INSERT INTO 
            motivo_reclamo (nombre,descripcion,tipo_reclamoid) 
        VALUES 
            (%s, %s, %s)
    '''
    sql_execute(sql, (nombre, descripcion , tipo_reclamoid))


def update_row(nombre, descripcion, tipo_reclamoid, id):
    sql = f'''
        UPDATE {table_name} SET 
            nombre = %s,
            descripcion =%s,
            tipo_reclamoid = %s
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql, (nombre, descripcion,tipo_reclamoid))


#####_ ADICIONALES _#####

def get_options():
    sql= f'''
        SELECT 
            id,
            nombre
        FROM {table_name}
        ORDER BY nombre asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila[get_primary_key()], fila['nombre']) for fila in filas]

    return lista
