from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'tipo_comprobante'

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
            *
        from {table_name} 

    '''
    columnas = {
        'id': ['ID' , 0.5] , 
        'inicial' : ['Inicial' , 0.5],
        'nombre' : ['Nombre' , 4.5] , 
        'descripcion' : ['Descripción' , 4.5] , 
        'activo' : ['Actividad' , 1] 
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( nombre , inicial,descripcion=None ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( nombre ,inicial, descripcion , activo )
        VALUES 
            ( %s , %s , %s , 1 )
    '''
    sql_execute(sql,( nombre, inicial , descripcion ))


def update_row( id , nombre , inicial ,descripcion ):
    sql = f'''
        update {table_name} set 
        nombre = %s ,
        inicial = %s,
        descripcion = %s
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql, (nombre, inicial , descripcion ))


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

def get_options_nombre():
    sql= f'''
        select 
            id,
            descripcion
        from {table_name}
        where activo = 1 and (id=2 or id=1)
        order by descripcion asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila[get_primary_key()], fila["descripcion"]) for fila in filas]

    return lista


def get_tipo_comprobante_by_tipo():
    sql = '''
        select id, nombre from tipo_comprobante where tipo_uso = 'V'
    '''
    filas = sql_select_fetchall(sql)
    return filas

def get_data_comprobante(id):
    sql = '''
        select id, nombre,inicial from tipo_comprobante where id = %s;   
        '''
    filas = sql_select_fetchone(sql,(id,))
    return filas