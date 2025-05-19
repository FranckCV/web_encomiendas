from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'modelo'

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


def get_table():
    sql= f'''
        select 
            mo.id ,
            mo.nombre ,
            mar.nombre as nom_mar,
            tip.nombre as nom_tip ,
            mo.tipo_unidadid ,
            mo.marcaid ,
            mo.activo
        from {table_name} mo
        inner join marca mar on mar.id = mo.marcaid 
        inner join tipo_unidad tip on tip.id = mo.tipo_unidadid


        order by mo.id asc
    '''
    columnas = {
        'id': ['ID' , 0.5 ] , 
        'nombre' : ['Nombre' , 3] , 
        'nom_mar' : ['Marca' , 3 ] , 
        'nom_tip' : ['Tipo de Unidad' , 3] ,
        'activo' : ['Actividad' , 1]
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


# def insert_row( nombre , marcaid , tipo_unidadid ):
#     sql = f'''
#         INSERT INTO 
#             {table_name} 
#             ( nombre , marcaid , tipo_unidadid )
#         VALUES 
#             ( '{nombre}' , '{marcaid}' , '{tipo_unidadid}' )
#     '''
#     sql_execute(sql)


def insert_row( nombre , marcaid , tipo_unidadid ):
    sql = f'''
        INSERT INTO 
            {table_name} ( nombre , marcaid , tipo_unidadid , activo ) 
        VALUES 
            ( %s ,  %s , %s , 1)
    '''
    sql_execute(sql,( nombre , marcaid , tipo_unidadid ))


def update_row( nombre , marcaid , tipo_unidadid , id):
    sql = f'''
        update {table_name} set 
        nombre = %s,
        marcaid = %s ,
        tipo_unidadid = %s
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql,(nombre , marcaid , tipo_unidadid))


#####_ ADICIONALES _#####

def get_options():
    sql= f'''
        select 
            id ,
            nombre
        from {table_name}
        order by nombre asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila["id"], fila["nombre"]) for fila in filas]

    return lista



