import pymysql
from pymysql.cursors import DictCursor

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                port=3306,
                                # port=3307,
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
    # lista = []

    # for col in columnas:
    #     lista.append( [ col[0] ] )
    
    return columnas

