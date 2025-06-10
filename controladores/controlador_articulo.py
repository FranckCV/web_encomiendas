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
            art.img ,
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
        # 'img': ['Imagen', 3],  # si quieres mostrar imagen
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
            ( nombre, precio, stock, img, dimensiones, tamaño_cajaid , activo)
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
        tamaño_cajaid = %s
        where id = {id}
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
    sql = '''
        SELECT 
            art.id AS articuloid,
            art.nombre AS nom_articulo,
            art.precio,
            art.stock,
            art.dimensiones,
            tam.nombre AS tam_nombre,
            art.tamaño_cajaid,
            art.img,
            des.nombre AS nom_descuento,
            REGEXP_SUBSTR(des.nombre, '[0-9]+') AS volumen,
            des_art.cantidad_descuento,
            art.activo
        FROM articulo art
        LEFT JOIN tamanio_caja tam ON tam.id = art.tamaño_cajaid
        LEFT JOIN descuento_articulo des_art ON des_art.articuloid = art.id
        LEFT JOIN descuento des ON des.id = des_art.descuentoid
        WHERE UPPER(art.nombre) NOT LIKE UPPER('%caja%')
    '''
    return sql_select_fetchall(sql)



def get_table_cajas():
    sql= f'''
        select 
            art.id as articuloid,
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
        LEFT join descuento des on des.id = des_art.DESCUENTOid
        where UPPER(art.nombre) like UPPER('%caja%')
        ;

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
            # Asumo formato 'YYYY-MM-DD' y validación simple de longitud
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

def get_report_reposicion(stock_minimo=10):
    """
    Obtiene un reporte de artículos que necesitan reposición
    basado en un stock mínimo definido
    """
    try:
        sql = '''
            SELECT 
                a.id,
                a.nombre,
                a.precio,
                a.stock,
                a.dimensiones,
                tam.nombre as tam_nombre,
                CASE 
                    WHEN a.stock = 0 THEN 'Sin Stock'
                    WHEN a.stock <= %s THEN 'Stock Bajo'
                    ELSE 'Stock Normal'
                END as estado_stock,
                COALESCE(SUM(dv.cantidad), 0) AS total_vendido
            FROM articulo a
            LEFT JOIN tamanio_caja tam ON tam.id = a.tamaño_cajaid
            LEFT JOIN detalle_venta dv ON a.id = dv.articuloid
            WHERE a.activo = 1 
                AND a.stock <= %s
            GROUP BY a.id, a.nombre, a.precio, a.stock, a.dimensiones, tam.nombre
            ORDER BY a.stock ASC, total_vendido DESC
        '''
        
        columnas = {
            'id': ['ID', 0.5],
            'nombre': ['Artículo', 3],
            'precio': ['Precio', 1],
            'stock': ['Stock Actual', 1],
            'dimensiones': ['Dimensiones', 2],
            'tam_nombre': ['Tamaño Caja', 2],
            'estado_stock': ['Estado', 1.5],
            'total_vendido': ['Total Vendido', 1.5],
        }
        
        filas = sql_select_fetchall(sql, (stock_minimo, stock_minimo))
        
        return columnas, filas
        
    except Exception as e:
        print(f"Error en get_report_reposicion: {e}")
        return {}, []

def get_stock_minimo_options():
    """Retorna opciones predefinidas para el stock mínimo"""
    return [
        (5, "5 unidades"),
        (10, "10 unidades"), 
        (15, "15 unidades"),
        (20, "20 unidades"),
        (25, "25 unidades"),
        (50, "50 unidades")
    ]


################## TRANSACCION VENTA ############
def obtener_precio_articulo(articulo_id):
    sql = "SELECT precio FROM articulo WHERE id = %s"
    resultado = sql_select_fetchone(sql, (articulo_id,))
    return resultado[0] if resultado else None
