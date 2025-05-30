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
        SELECT 
            art.id,
            art.nombre,
            art.precio,
            art.stock,
            art.dimensiones,
            tam.nombre as tam_nombre,
            art.tamaño_cajaid,
            art.activo
        FROM {table_name} art
        LEFT JOIN tamanio_caja tam ON tam.id = art.tamaño_cajaid
    '''
    columnas = {
        'id': ['ID', 0.5], 
        'nombre': ['Nombre', 5], 
        'precio': ['Precio', 1], 
        'stock': ['Stock', 1], 
        'dimensiones': ['Dimensiones', 2], 
        'tam_nombre': ['Tamaño de caja', 3], 
        'img': ['Imagen', 3],  # si quieres mostrar imagen
        'activo': ['Actividad', 1] 
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas



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


def my_sql_select_fetchall(sql, params=None):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados or []
    except Exception as e:
        print(f"Error en consulta SQL: {e}")
        return []

def get_report_mas_vendidos(fecha_inicio=None, fecha_fin=None):
    try:
        sql = '''
            SELECT 
                a.id,
                a.nombre,
                COALESCE(SUM(dv.cantidad), 0) AS total_vendido,
                a.stock
            FROM articulo a
            LEFT JOIN detalle_venta dv 
                ON a.id = dv.articuloid
            LEFT JOIN transaccion_venta tv 
                ON dv.ventanum_serie = tv.num_serie 
                AND dv.ventatipo_comprobanteid = tv.tipo_comprobanteid
            WHERE 1=1
        '''
        params = []

        if fecha_inicio and fecha_fin:
            if len(fecha_inicio) == 10 and len(fecha_fin) == 10:
                sql += " AND tv.fecha BETWEEN %s AND %s "
                params.extend([fecha_inicio, fecha_fin])
            else:
                print("Formato de fecha incorrecto, filtro ignorado.")

        sql += '''
            GROUP BY a.id, a.nombre, a.stock
            ORDER BY total_vendido DESC
        '''

        columnas = {
            'id': ['ID', 0.5],
            'nombre': ['Nombre', 3],
            'total_vendido': ['Total Vendido', 1.5],
            'stock': ['Stock', 1],
        }

        filas = sql_select_fetchall(sql, tuple(params))
        return columnas, filas

    except Exception as e:
        print(f"Error en get_report_mas_vendidos: {e}")
        return {}, []


def get_report_articulos_reposicion(stock_min=10):
    try:
        if not isinstance(stock_min, int) or stock_min < 0:
            stock_min = 10

        sql = '''
            SELECT
                id,
                nombre,
                stock,
                precio
            FROM articulo
            WHERE stock < %s AND activo = 1
            ORDER BY stock ASC
        '''

        columnas = {
            'id': ['ID', 0.5],
            'nombre': ['Nombre', 3],
            'stock': ['Stock', 1],
            'precio': ['Precio', 1],
        }

        filas = sql_select_fetchall(sql, (stock_min,))
        return columnas, filas

    except Exception as e:
        print(f"Error en get_report_articulos_reposicion: {e}")
        return {}, []

