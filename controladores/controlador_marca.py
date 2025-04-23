from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ CRUD _#####

table_name = 'marca'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def table_fetchall():
    sql= f'''
        select 
            id ,
            nombre
        from {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    
    return resultados


def get_table():
    sql= f'''
        select 
            id ,
            nombre
        from {table_name}
        order by id desc
    '''
    columnas = [ 'ID' , 'Nombre' ]
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql)


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( nombre ):
    sql = f'''
        INSERT INTO 
            {table_name} ( nombre )
        VALUES 
            ( '{nombre}' )
    '''
    sql_execute(sql)


def update_row( id , nombre ):
    sql = f'''
        Update {table_name} set 
        nombre = '{nombre}'
        where id = {id}
    '''
    sql_execute(sql)


#####_ ADICIONALES _#####

def get_options_marca():
    sql= f'''
        select 
            id ,
            nombre
        from {table_name}
        order by id asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila["id"], fila["nombre"]) for fila in filas]

    return lista

