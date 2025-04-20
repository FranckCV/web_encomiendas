from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid ,show_columns
#####_ NECESARIAS _#####

table_name = 'tipo_unidad'

def get_info_columns():
    return show_columns(table_name)


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
            tip.nombre ,
            tip.descripcion ,
            tip.activo 
        from {table_name} tip
        order by tip.id desc
    '''
    columnas = [ 'ID' , 'Nombre' , 'Descripcion' , 'Activo' ]
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


def insert_row( nombre , descripcion , activo ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( nombre , descripcion , activo )
        VALUES 
            ( '{nombre}' , '{descripcion}' , {activo} )
    '''
    sql_execute(sql)


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where id = {id}
    '''
    sql_execute(sql)


#####_ ADICIONALES _#####

def get_options():
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