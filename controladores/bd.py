import pymysql
from pymysql.cursors import DictCursor
#Establecemos la conexión
def obtener_conexion():
    return pymysql.connect(host='localhost',
<<<<<<< HEAD
                                # port=3306,
                                port=3307,
=======
                               port=3306,
                                #  port=3307,
>>>>>>> 4bd7800e92863aef8e465ae926fe1a103e45e152
                                user='root',
                                password='',
                                db='bd_encomiendas' ,
                                cursorclass=DictCursor
                                )


def sql_select_fetchall(sql , args = None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql , args)
            resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except Exception as e:
        return e


def sql_select_fetchone(sql , args = None):
    conexion = obtener_conexion()
    try: 
        with conexion.cursor() as cursor:
            cursor.execute(sql, args)
            resultados = cursor.fetchone()
        conexion.close()
        return resultados
    except Exception as e:
        return e


def sql_execute(sql , args = None):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute( sql , args)
    conexion.commit()
    conexion.close()


def sql_execute_lastrowid(sql , args = None):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute( sql , args )
        last_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return last_id


def show_columns(table_name):
    sql= f'''
        SHOW COLUMNS FROM 
        {table_name}
    '''
    columnas = sql_select_fetchall(sql)
    
    return columnas


def show_primary_key(tabla):
    keys = []
    for row in show_columns(tabla):
        if row['Key'] == 'PRI':
            keys.append(row['Field'])

    if len(keys) == 1:
        return keys[0]
    else:
        return keys


def find_column_table(column_name, tabla):
    for row in show_columns(tabla):
        # print(row)
        if row['Field'] == column_name:
            return row
    return None


def delete_row_table( table_name , id ):
    sql = f'''
        delete from {table_name}
        where {show_primary_key(table_name)} = {id}
    '''
    sql_execute(sql)


def exists_column_Activo(tabla):
    row = find_column_table('activo' , tabla)
    # print(row)
    return row is not None


def unactive_row_table(table , pk):
    sql = f'''
        update {table} set 
        activo = NOT activo
        where {show_primary_key(table)} = {pk}
    '''
    sql_execute(sql)
    # return 0


def include_data_search(where = None, column_search = None , value_search = None):
    strSQL = ' '
    if where is not None and column_search is not None and value_search is not None:
        if where is True:
            strSQL += 'where'
        strSQL += f'''
            UPPER({column_search}) LIKE UPPER ('%{str(value_search)}%')
        '''
    return strSQL


def include_list_search(where = None, list_columns = [] , value_search = None):
    strSQL = ' '
    if where is not None and list_columns is not [] and value_search is not None:
        for column in list_columns:
            if list_columns[0] == column:
                strSQL += f'''{include_data_search(where,column,value_search)}'''
            else:
                strSQL += f''' or {include_data_search(False,column,value_search)}'''
    return strSQL

