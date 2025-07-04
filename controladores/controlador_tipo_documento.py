from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'tipo_documento'

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
            tip.id ,
            tip.siglas,
            tip.nombre ,
            tip.activo 
        from {table_name} tip
    '''
    columnas = {
        'id': ['ID' , 0.5] , 
        'siglas' : ['Siglas' , 1.5] , 
        'nombre' : ['Nombre' , 6] , 
        'activo' : ['Actividad' , 1] 
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( siglas, nombre ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( siglas , nombre , activo )
        VALUES 
            ( %s , %s , 1 )
    '''
    sql_execute(sql,( siglas , nombre ))


def update_row( id , siglas , nombre ):
    sql = f'''
        update {table_name} set 
        siglas = %s ,
        nombre = %s 
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql, (siglas , nombre ))


#####_ ADICIONALES _#####

def get_options():
    try:
        sql = f'''
            SELECT 
                {get_primary_key()},
                nombre
            FROM {table_name}
            WHERE activo = 1
            ORDER BY nombre ASC
        '''
        filas = sql_select_fetchall(sql)
        return [(fila[get_primary_key()], fila["nombre"]) for fila in filas]
    except Exception as e:
        print(f"❌ Error en get_options de {table_name}:", e)
        return []


def get_options_dict():
    sql= f'''
        select 
            id ,
            CONCAT(siglas ,' - ', nombre) as nombre ,
            siglas
        from tipo_documento
        where activo = 1
        order by nombre asc
    '''
    filas = sql_select_fetchall(sql)

    return filas





