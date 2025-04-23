from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid


def get_table_colores():
    sql= '''
        select 
            id , 
            nombre , 
            valor 
        from color
    '''
    columnas = [ 'ID' , 'Nombre' , 'Valor Hexadecimal' ]
    resultados = sql_select_fetchall(sql)
    return columnas , resultados






