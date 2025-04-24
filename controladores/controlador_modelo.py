from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ CRUD _#####

table_name = 'modelo'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def table_fetchall():
    sql= f'''
        select 
            *
        from {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    
    return resultados


def get_table(columns_search=[],value_search=None):
    sql= f'''
        select 
            mo.id ,
            mo.nombre as nom_mod,
            mar.nombre as nom_mar,
            tip.nombre as nom_tip 
        from {table_name} mo
        inner join marca mar on mar.id = mo.marcaid 
        inner join tipo_unidad tip on tip.id = mo.tipo_unidadid

        {bd.include_list_search(True , list_columns=columns_search , value_search = value_search)} 

    '''
    columnas = {
        'id':'ID' , 
        'nom_mod' : 'Nombre' , 
        'nom_mar' : 'Marca' , 
        'nom_tip' : 'Tipo de Unidad' 
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where id = {id}
    '''
    sql_execute(sql)


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( nombre , marcaid , tipo_unidadid ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( nombre , marcaid , tipo_unidadid )
        VALUES 
            ( '{nombre}' , '{marcaid}' , '{tipo_unidadid}' )
    '''
    sql_execute(sql)


def update_row( id , nombre , marcaid , tipo_unidadid):
    sql = f'''
        update {table_name} set 
        nombre = '{nombre}',
        marcaid = {marcaid} ,
        tipo_unidadid = {tipo_unidadid}
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql)


#####_ ADICIONALES _#####

def get_options():
    sql= f'''
        select 
            {get_primary_key()} ,
            nombre
        from {table_name}
        order by id asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila[get_primary_key()], fila["nombre"]) for fila in filas]

    return lista



