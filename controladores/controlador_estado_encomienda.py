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

def get_options():
    sql= f'''
        select 
            {get_primary_key()} ,
            nombre
        from {table_name}
        where activo = 1
        order by nombre asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila[get_primary_key()], fila["nombre"]) for fila in filas]

    return lista



def get_states():
    sql = '''
        select id, nombre from estado_encomienda where tipoEstado = 'N'
    '''
    filas = sql_select_fetchall(sql)
    return filas

from datetime import datetime

def get_last_states(tracking):
    sql = '''
        SELECT de.nombre, s.fecha, s.hora
        FROM seguimiento s
        INNER JOIN detalle_estado de ON de.id = s.detalle_estadoid
        WHERE s.paquetetracking = %s
        ORDER BY s.fecha DESC, s.hora DESC
        LIMIT 1
    '''
    fila = sql_select_fetchone(sql, (tracking,))

    if fila:
        fecha = datetime.strptime(str(fila['fecha']), "%Y-%m-%d").strftime("%d/%m/%Y")
        hora = datetime.strptime(str(fila['hora']), "%H:%M:%S").strftime("%H:%M")

        fila['fecha'] = fecha
        fila['hora'] = hora

    return fila
