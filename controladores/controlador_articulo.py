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
            des.id,
            des.nombre as nom_descuento,
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

### REPORTES ###
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

def get_report_reposicion():
    """
    Obtiene un reporte de todos los artículos con clasificación automática de estado de stock
    """
    try:
        sql = '''
           SELECT 
                a.id,
                a.nombre,
                a.precio,
                a.stock,
                a.dimensiones,
                COALESCE(tam.nombre, 'Sin tamaño') as tam_nombre,
                    CASE 
                        WHEN a.stock = 0 THEN 'Sin Stock'
                        WHEN a.stock <= 5 THEN 'Stock Crítico'
                        WHEN a.stock <= 10 THEN 'Stock Bajo'
                        ELSE 'Stock Normal'
                    END as estado_stock
            FROM articulo a
            LEFT JOIN tamanio_caja tam ON tam.id = a.tamaño_cajaid
            WHERE a.activo = 1
            ORDER BY id
        '''
        
        columnas = {
            'id': ['ID', 0.5],
            'nombre': ['Artículo', 0.5],
            'precio': ['Precio S/.', 0.5],
            'stock': ['Stock Actual', 0.5],
            'estado_stock': ['Estado', 0.5],
        }
        
        filas = sql_select_fetchall(sql)
        
        return columnas, filas
        
    except Exception as e:
        print(f"Error en get_report_reposicion: {e}")
        return {}, []

def get_reporte_ventas(fecha_inicio=None, fecha_fin=None):
    """
    Obtiene un reporte de ventas por periodo con detalles de transacciones
    """
    try:
        # Construir la consulta base
        sql = '''
            SELECT 
                tv.num_serie,
                tv.fecha,
                tv.hora,
                CONCAT(c.nombre_siglas, ' ', c.apellidos_razon) as cliente,
                c.num_documento,
                td.siglas as tipo_documento,
                tc.nombre as tipo_comprobante,
                tv.monto_total,
                tv.estado,
                CASE 
                    WHEN tv.estado = 0 THEN 'Pendiente'
                    WHEN tv.estado = 1 THEN 'Completado'
                    ELSE 'Cancelado'
                END as estado_descripcion,
                COUNT(dv.articuloid) as cantidad_articulos,
                SUM(dv.cantidad) as total_unidades,
                ROUND(tv.monto_total / 1.18, 2) as subtotal,
                ROUND(tv.monto_total - (tv.monto_total / 1.18), 2) as igv
            FROM transaccion_venta tv
            INNER JOIN cliente c ON tv.clienteid = c.id
            INNER JOIN tipo_documento td ON c.tipo_documentoid = td.id
            INNER JOIN tipo_comprobante tc ON tv.tipo_comprobanteid = tc.id
            LEFT JOIN detalle_venta dv ON tv.num_serie = dv.ventanum_serie
            WHERE 1=1
        '''
        
        params = []
        
        # Aplicar filtros de fecha si se proporcionan
        if fecha_inicio and fecha_fin:
            # Validar formato de fecha
            if len(fecha_inicio) == 10 and len(fecha_fin) == 10:
                sql += " AND tv.fecha BETWEEN %s AND %s "
                params.extend([fecha_inicio, fecha_fin])
            else:
                print("Formato de fecha incorrecto, filtro ignorado.")
        
        sql += '''
            GROUP BY tv.num_serie, tv.fecha, tv.hora, c.id, td.siglas, tc.nombre, tv.monto_total, tv.estado
            ORDER BY tv.fecha DESC, tv.hora DESC
        '''
        
        columnas = {
            'num_serie': ['N° Serie', 1],
            'fecha': ['Fecha', 1.2],
            'hora': ['Hora', 1],
            'cliente': ['Cliente', 3],
            'num_documento': ['Documento', 1.5],
            'tipo_documento': ['Tipo Doc.', 1],
            'tipo_comprobante': ['Comprobante', 1.5],
            'cantidad_articulos': ['Artículos', 1],
            'total_unidades': ['Unidades', 1],
            'subtotal': ['Subtotal S/.', 1.5],
            'igv': ['IGV S/.', 1.2],
            'monto_total': ['Total S/.', 1.5],
            'estado_descripcion': ['Estado', 1.2],
        }
        
        filas = sql_select_fetchall(sql, tuple(params))
        
        return columnas, filas
        
    except Exception as e:
        print(f"Error en get_reporte_ventas: {e}")
        return {}, []
    
################## TRANSACCION VENTA ############
def obtener_precio_articulo(articulo_id):
    sql = "SELECT precio FROM articulo WHERE id = %s"
    resultado = sql_select_fetchone(sql, (articulo_id,))
    return resultado[0] if resultado else None
