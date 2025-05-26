from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'articulo'

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
            art.id ,
            art.nombre ,
            art.precio ,
            art.stock ,
            art.dimensiones ,
            tam.nombre as tam_nombre,
            art.tamaño_cajaid ,
            art.img,
            art.activo 
        from {table_name} art
        left join tamanio_caja tam on tam.id = art.tamaño_cajaid 

    '''
    columnas = {
        'id': ['ID' , 0.5] , 
        'nombre' : ['Nombre' , 5] , 
        'precio' : ['Precio' , 1] , 
        'stock' : ['Stock' , 1] , 
        'dimensiones' : ['Dimensiones' , 2] , 
        'tam_nombre' : ['Tamaño de caja' , 3] , 
        'activo' : ['Actividad' , 1] 
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( nombre, precio, stock, img, dimensiones,tamaño_cajaid ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( nombre, precio, stock, img, dimensiones,tamaño_cajaid , activo)
        VALUES 
            ( %s ,%s ,%s ,%s ,%s ,%s , 1)
    '''
    sql_execute(sql,( nombre, precio, stock, img, dimensiones,tamaño_cajaid ))


def update_row( id ,nombre, precio, stock, img, dimensiones,tamaño_cajaid ):
    sql = f'''
        update {table_name} set 
        nombre = %s,
        precio = %s,
        stock = %s,
        img= %s,
        dimensiones = %s,
        tamaño_cajaid= %s
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql, (nombre, precio, stock, img, dimensiones,tamaño_cajaid ))


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


def get_table_with_discount():
    sql= f'''
        select 
            art.id ,
            art.nombre as nom_articulo,
            art.precio ,
            art.stock ,
            art.dimensiones ,
            tam.nombre as tam_nombre,
            art.tamaño_cajaid ,
            art.img,
            des.nombre as nom_descuento,
            des_art.cantidad_descuento,
            art.activo 
        from articulo art
        left join tamanio_caja tam on tam.id = art.tamaño_cajaid 
        left join descuento_articulo des_art on des_art.articuloid = art.id
        LEFT join descuento des on des.id = des_art.DESCUENTOid;

    '''
    
    filas = sql_select_fetchall(sql)
    
    return filas



