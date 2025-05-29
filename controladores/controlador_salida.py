#Cuando programo una salida también inserto una escala y un empleado-salida
from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'estado_encomienda'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( id ):
    bd.delete_row_table(table_name , id)


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
            est.id ,
            est.nombre,
            est.descripcion,
            est.activo 
        from {table_name} est
    '''
    columnas = {
        'id': ['ID' , 0.5 ] , 
        'nombre' : ['Nombre' , 1 ] , 
        'descripcion' : ['Descripcion' , 5.5] , 
        'activo' : ['Actividad' , 3.5] , 
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CAMBIAR PARAMETROS Y SQL INTERNO _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( nombre , descripcion = None ):
    sql = f'''
        INSERT INTO 
            {table_name} ( nombre , descripcion , activo )
        VALUES 
            ( %s , %s , 1 )
    '''
    sql_execute(sql,( nombre , descripcion ))


def update_row( id , nombre , descripcion =None ):
    sql = f'''
        update {table_name} set 
        nombre = %s ,
        descripcion = %s
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql,(nombre , descripcion))


#####_ ADICIONALES _#####






