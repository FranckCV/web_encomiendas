from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns
#####_ NECESARIAS _#####

table_name = 'marca'

def get_info_columns():
    return show_columns(table_name)


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


def delete_row( id ):
    sql = f'''
        delete from {table_name}
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

