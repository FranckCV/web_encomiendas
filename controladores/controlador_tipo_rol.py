from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'tipo_rol'

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

from flask import request
import controladores.controlador_usuario as controlador_usuario
def get_table():
    usuario = controlador_usuario.get_usuario_empleado_user_id(request.cookies.get('user_id'))
    validar_admin = '' if usuario['rolid'] == 1 else ' where tip.id != 1 '

    sql= f'''
        select 
            tip.id ,
            tip.nombre ,
            tip.descripcion ,
            tip.activo 
        from {table_name} tip
        {validar_admin}
    '''
    columnas = {
        'id': ['ID' , 0.5] , 
        'nombre' : ['Nombre' , 4.5] , 
        'descripcion' : ['Descripción' , 4.5] , 
        'activo' : ['Actividad' , 1] 
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( nombre , descripcion=None ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( nombre , descripcion , activo )
        VALUES 
            ( %s , %s , 1 )
    '''
    sql_execute(sql,( nombre , descripcion ))


def update_row( id , nombre , descripcion ):
    sql = f'''
        update {table_name} set 
        nombre = %s ,
        descripcion = %s
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql, (nombre , descripcion ))


#####_ ADICIONALES _#####

def get_options():
    usuario = controlador_usuario.get_usuario_empleado_user_id(request.cookies.get('user_id'))
    validar_admin = '' if usuario['rolid'] == 1 else ' and tip.id != 1 '

    sql= f'''
        select 
            id ,
            nombre
        from {table_name} tip
        where activo = 1 {validar_admin}
        order by nombre asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila['id'], fila["nombre"]) for fila in filas]

    return lista






