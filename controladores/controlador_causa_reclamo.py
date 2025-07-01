from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'causa_reclamo'

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
            ca.id ,
            ca.nombre ,
            ca.descripcion,
            mot.nombre as nom_mot 
        from {table_name} ca
        inner join motivo_reclamo mot on mot.id = ca.motivo_reclamoid
        order by ca.id asc
    '''
    columnas = {
        'id': ['ID' , 0.5 ] , 
        'nombre' : ['Nombre' , 3] , 
        'descripcion' : ['descripcion' , 3] , 
        'nom_mot' : ['Motivo de reclamo' , 3],
    }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row(id):
    unactive_row_table({table_name}, id)


def insert_row(nombre, descripcion , motivo_reclamoid):
    sql = f'''
        INSERT INTO 
            causa_reclamo (nombre,descripcion,motivo_reclamoid) 
        VALUES 
            (%s, %s, %s)
    '''
    sql_execute(sql, (nombre, descripcion , motivo_reclamoid))


def update_row(nombre, descripcion, motivo_reclamoid, id):
    sql = f'''
        UPDATE {table_name} SET 
            nombre = %s,
            descripcion =%s,
            motivo_reclamoid = %s
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql, (nombre, descripcion,motivo_reclamoid))


#####_ ADICIONALES _#####


def get_options():
    try:
        sql = f'''
            SELECT 
                {get_primary_key()},
                nombre
            FROM {table_name}
            ORDER BY nombre ASC
        '''
        filas = sql_select_fetchall(sql)
        return [(fila[get_primary_key()], fila["nombre"]) for fila in filas]
    except Exception as e:
        print("❌ Error en get_options causa_reclamo:", e)
        return []
