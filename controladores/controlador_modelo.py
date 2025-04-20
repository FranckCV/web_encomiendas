from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns
#####_ NECESARIAS _#####

table_name = 'modelo'

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
            mo.id ,
            mo.nombre ,
            mar.nombre ,
            tip.nombre 
        from {table_name} mo
        inner join marca mar on mar.id = mo.marcaid 
        inner join tipo_unidad tip on tip.id = mo.tipo_unidadid 
        order by mo.id desc
    '''
    columnas = [ 'ID' , 'Nombre' , 'Marca' , 'Tipo de Unidad' ]
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


def insert_row( nombre , marcaid , tipo_unidadid ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( nombre , marcaid , tipo_unidadid )
        VALUES 
            ( '{nombre}' , '{marcaid}' , '{tipo_unidadid}' )
    '''
    sql_execute(sql)


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where id = {id}
    '''
    sql_execute(sql)


#####_ ADICIONALES _#####


