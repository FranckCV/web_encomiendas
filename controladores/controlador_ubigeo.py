from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd

table_name =  'ubigeo'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( id ):
    bd.delete_row_table(table_name , id)
    
#####_ CAMBIAR SQL y DICT INTERNO _#####
def table_fetch_all():
    sql = f'select * from {table_name}'
    resultados = sql_select_fetchall(sql)
    return resultados

def get_table():
    sql = f'select LPAD(codigo, 6, "0") as codigo, distrito, provincia,departamento, activo from {table_name} order by distrito asc'
    columnas = {
        'codigo': ['Código' , 0.5] , 
        'departamento' : ['Departamento' , 2.5] , 
        'provincia' : ['Provincia' , 2.5] , 
        'distrito' : ['Distrito' , 2.5],
        'activo' : ['Activo',0.5]
        }
    filas = sql_select_fetchall(sql)
    return columnas,filas

#####_ ADICIONALES _#####

def get_options():
    sql= f'''
        SELECT 
            codigo,
            CONCAT(departamento, " / ", provincia, " / ", distrito) AS ubigeo
        FROM {table_name}
        order by ubigeo
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila['codigo'], fila["ubigeo"]) for fila in filas]
    return lista

def get_options_departamento():
    sql= f'''
        SELECT DISTINCT 
            ub.departamento 
        FROM ubigeo ub
        inner join sucursal su on ub.codigo = su.ubigeocodigo
        where ub.activo = 1
        order by ub.departamento
    '''
    filas = sql_select_fetchall(sql)
    
    # lista = [(fila["departamento"]) for fila in filas]
    lista = filas
    return lista


def get_options_provincia():
    sql= f'''
        SELECT DISTINCT 
            ub.departamento ,
            ub.provincia
        FROM ubigeo ub
        inner join sucursal su on ub.codigo = su.ubigeocodigo
        where ub.activo = 1
        order by ub.departamento , ub.provincia
    '''
    filas = sql_select_fetchall(sql)
    
    # lista = [( fila["departamento"] , fila["provincia"]) for fila in filas]
    lista = filas
    return lista


def get_options_distrito():
    sql= f'''
        SELECT DISTINCT
            ub.codigo , 
            ub.departamento ,
            ub.provincia ,
            ub.distrito 
        FROM ubigeo ub
        inner join sucursal su on ub.codigo = su.ubigeocodigo
        where ub.activo = 1
        order by ub.departamento , ub.provincia , ub.distrito
    '''
    filas = sql_select_fetchall(sql)
    
    # lista = [( fila["codigo"] , fila["departamento"] , fila["provincia"] , fila["distrito"] ) for fila in filas]
    lista = filas
    return lista


