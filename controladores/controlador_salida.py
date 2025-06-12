#Cuando programo una salida también inserto una escala y un empleado-salida
from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'salida'

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
        SELECT
            s.id, 
            CONCAT(e.nombre, ' ', e.apellidos) AS nom_conductor,
            u.placa,
            ub.departamento AS destino,
            s.fecha,
            s.hora,
            u.capacidad,
            CASE s.estado
                WHEN 'P' THEN 'Pendiente (origen sucursal / domicilio)'
                WHEN 'E' THEN 'En curso (en ruta)'
                WHEN 'C' THEN 'Completada (destino sucursal / domicilio)'
                WHEN 'X' THEN 'Cancelada'
                ELSE 'Estado desconocido'
            END AS estado
        FROM salida s
        LEFT JOIN unidad u ON u.id = s.unidadid
        LEFT JOIN empleado e ON e.id = s.conductor_principal
        LEFT JOIN sucursal su ON su.id = s.destino_final
        LEFT JOIN ubigeo ub ON ub.codigo = su.ubigeocodigo
    '''
    columnas = {
        'id': ['ID' , 0.5 ] , 
        'nom_conductor' : ['Conductor' , 1 ] , 
        'placa' : ['Placa' , 1] , 
        'destino' : ['Destino' , 3.5] , 
        'fecha' : ['Fecha' , 1.2] , 
        'hora' : ['Hora' , 1] , 
        'capacidad' : ['Capacidad' , 1.5] , 
        'estado' : ['Estado' , 3.5] ,

        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CAMBIAR PARAMETROS Y SQL INTERNO _###### 

# def unactive_row( id ):
#     unactive_row_table(table_name , id)


# def insert_row( nombre , descripcion = None ):
#     sql = f'''
#         INSERT INTO 
#             {table_name} ( nombre , descripcion , activo )
#         VALUES 
#             ( %s , %s , 1 )
#     '''
#     sql_execute(sql,( nombre , descripcion ))


# def update_row( id , nombre , descripcion =None ):
#     sql = f'''
#         update {table_name} set 
#         nombre = %s ,
#         descripcion = %s
#         where {get_primary_key()} = {id}
#     '''
#     sql_execute(sql,(nombre , descripcion))


#####_ ADICIONALES _#####






