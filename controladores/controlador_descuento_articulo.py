from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'descuento_articulo'

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
    sql = f'''
        SELECT 
            tr.descuentoid,
            tr.articuloid,
            ar.nombre AS nom_articulo,
            des.nombre AS nom_descuento,
            tr.cantidad_descuento AS precio
        FROM 
            DESCUENTO_articulo tr
        INNER JOIN articulo ar ON ar.id = tr.articuloid
        INNER JOIN descuento des ON des.id = tr.descuentoid;
    '''

    columnas = {
        'nom_articulo': ['Artículo', 3],
        'nom_descuento': ['Descuento', 3],
        'precio': ['Cantidad Descuento', 2]
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas



######_ CRUD ESPECIFICAS _###### 

def unactive_row(id):
    unactive_row_table("sucursal", id)


def insert_row(descuentoid, articuloid, cantidad_descuento):
    cantidad = float(cantidad_descuento) /100
    sql = '''
        INSERT INTO descuento_articulo (descuentoid, articuloid, cantidad_descuento)
        VALUES (%s, %s, %s)
    '''
    sql_execute(sql, (descuentoid, articuloid, cantidad))


def update_row(descuentoid, articuloid, cantidad_descuento):
    sql = '''
        UPDATE DESCUENTO_articulo
        SET cantidad_descuento = %s
        WHERE descuentoid = %s AND articuloid = %s
    '''
    sql_execute(sql, (cantidad_descuento, descuentoid, articuloid))



#####_ ADICIONALES _#####


