from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ CRUD _#####

table_name = 'tipo_unidad'

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
            tip.id ,
            tip.nombre ,
            tip.descripcion ,
            tip.activo 
        from {table_name} tip

        {bd.include_list_search(True , list_columns=columns_search , value_search = value_search)} 

    '''
    columnas = {
        'id':'ID' , 
        'nombre' : 'Nombre' , 
        'descripcion' : 'Descripción' , 
        'activo' : 'Activo' 
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql)


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( nombre , descripcion=None ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( nombre , descripcion , activo )
        VALUES 
            ( '{nombre}' , '{descripcion}' , 1 )
    '''
    sql_execute(sql)


def update_row( id , nombre , descripcion ):
    sql = f'''
        update {table_name} set 
        nombre = '{nombre}' ,
        descripcion = '{descripcion}'
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
        where activo = 1
        order by nombre asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila[get_primary_key()], fila["nombre"]) for fila in filas]

    return lista






