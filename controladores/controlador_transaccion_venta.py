from controladores.bd import (
    sql_execute_lastrowid,
    sql_execute,
    sql_select_fetchone,
    sql_select_fetchall
)


def obtener_transaccion_provisional(clienteid):
    sql = '''
        SELECT num_serie FROM transaccion_venta
        WHERE clienteid = %s AND estado = 0
        ORDER BY num_serie DESC
        LIMIT 1
    '''
    result = sql_select_fetchone(sql, (clienteid,))
    
    # 🔒 Validación de error
    if isinstance(result, Exception):
        raise result

    return result

def crear_transaccion_provisional(tipo_comprobanteid, monto_total, clienteid):
    sql = '''
        INSERT INTO transaccion_venta (tipo_comprobanteid, monto_total, fecha, hora, clienteid, estado)
        VALUES (%s, %s, CURDATE(), CURTIME(), %s, 0)
    '''
    return sql_execute_lastrowid(sql, (tipo_comprobanteid, monto_total, clienteid))


def agregar_detalle_venta(articuloid, ventanum_serie, cantidad):
    sql = '''
        INSERT INTO detalle_venta (articuloid, ventanum_serie, cantidad)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE cantidad = VALUES(cantidad)
    '''
    return sql_execute(sql, (articuloid, ventanum_serie, cantidad))

def actualizar_monto_total(ventanum_serie):
    sql = '''
        SELECT SUM(dv.cantidad * 
            COALESCE(
                (
                    SELECT da.cantidad_descuento
                    FROM descuento_articulo da
                    JOIN descuento d ON d.id = da.descuentoid
                    WHERE da.articuloid = dv.articuloid
                        AND CAST(REGEXP_SUBSTR(d.nombre, '[0-9]+') AS UNSIGNED) <= dv.cantidad
                    ORDER BY CAST(REGEXP_SUBSTR(d.nombre, '[0-9]+') AS UNSIGNED) DESC
                    LIMIT 1
                ),
                a.precio
            )
        ) AS total
        FROM detalle_venta dv
        JOIN articulo a ON dv.articuloid = a.id
        WHERE dv.ventanum_serie = %s
    '''

    total = sql_select_fetchone(sql, (ventanum_serie,))
    if total and total.get("total") is not None:
        update_sql = '''
            UPDATE transaccion_venta
            SET monto_total = %s
            WHERE num_serie = %s
        '''
        return sql_execute(update_sql, (total["total"], ventanum_serie))


# def actualizar_monto_total(ventanum_serie):
#     sql = '''
#         SELECT SUM(dv.cantidad * a.precio) AS total
#         FROM detalle_venta dv
#         JOIN articulo a ON dv.articuloid = a.id
#         WHERE dv.ventanum_serie = %s 
#     '''
#     total = sql_select_fetchone(sql, (ventanum_serie,))
#     if total and total.get("total") is not None:
#         update_sql = '''
#             UPDATE transaccion_venta
#             SET monto_total = %s
#             WHERE num_serie = %s
#         '''
#         return sql_execute(update_sql, (total["total"], ventanum_serie))


def registrar_detalle_venta(clienteid, tipo_comprobanteid, articuloid, cantidad):
    # Paso 1: Buscar si ya existe transacción provisional
    transaccion = obtener_transaccion_provisional(clienteid)

    if not transaccion:
        # Paso 2: Crear transacción provisional nueva
        num_serie = crear_transaccion_provisional(tipo_comprobanteid, 0, clienteid)
    else:
        num_serie = transaccion["num_serie"]

    # Paso 3: Insertar detalle de venta
    agregar_detalle_venta(articuloid, num_serie, cantidad)

    # Paso 4: Actualizar total
    actualizar_monto_total(num_serie)

    return num_serie

def obtener_carrito_cliente(clienteid: int):
    transaccion = obtener_transaccion_provisional(clienteid)
    if not transaccion:
        return []

    num_serie = transaccion.get("num_serie")

    sql = '''
        SELECT 
            dv.articuloid AS id,
            a.nombre AS name,
            CAST(a.precio AS DECIMAL(10,2)) AS originalPrice,
            dv.cantidad AS quantity,
            a.img as image,

            -- Descuentos
            MAX(CASE 
                WHEN REGEXP_SUBSTR(des.nombre, '[0-9]+') IS NOT NULL AND 
                     CAST(REGEXP_SUBSTR(des.nombre, '[0-9]+') AS UNSIGNED) = vol.min_vol THEN des_art.cantidad_descuento
                ELSE NULL END) AS precio_unitario_2,

            MAX(CASE 
                WHEN REGEXP_SUBSTR(des.nombre, '[0-9]+') IS NOT NULL AND 
                     CAST(REGEXP_SUBSTR(des.nombre, '[0-9]+') AS UNSIGNED) = vol.max_vol THEN des_art.cantidad_descuento
                ELSE NULL END) AS precio_unitario_3,

            vol.min_vol AS cantidad_precio_unitario_2,
            vol.max_vol AS cantidad_precio_unitario_3

        FROM detalle_venta dv
        JOIN articulo a ON dv.articuloid = a.id
        LEFT JOIN descuento_articulo des_art ON des_art.articuloid = a.id
        LEFT JOIN descuento des ON des.id = des_art.descuentoid

        LEFT JOIN (
            SELECT 
                da.articuloid,
                MIN(CAST(REGEXP_SUBSTR(d.nombre, '[0-9]+') AS UNSIGNED)) AS min_vol,
                MAX(CAST(REGEXP_SUBSTR(d.nombre, '[0-9]+') AS UNSIGNED)) AS max_vol
            FROM descuento_articulo da
            JOIN descuento d ON d.id = da.descuentoid
            GROUP BY da.articuloid
        ) AS vol ON vol.articuloid = a.id

        WHERE dv.ventanum_serie = %s
        GROUP BY dv.articuloid, a.nombre, a.precio, dv.cantidad, a.img, vol.min_vol, vol.max_vol
    '''

    return sql_select_fetchall(sql, (num_serie,))

def eliminar_detalle_venta(articuloid, ventanum_serie):
    sql = '''
        DELETE FROM detalle_venta
        WHERE articuloid = %s AND ventanum_serie = %s
    '''
    return sql_execute(sql, (articuloid, ventanum_serie))


def eliminar_todo_detalle_venta(ventanum_serie):
    sql = '''
        DELETE FROM detalle_venta
        WHERE ventanum_serie = %s
    '''
    return sql_execute(sql, (ventanum_serie,))

def obtener_monto_total(num_serie):
    sql = "SELECT monto_total FROM transaccion_venta WHERE num_serie = %s"
    resultado = sql_select_fetchone(sql, (num_serie,))
    if resultado and "monto_total" in resultado:
        return resultado["monto_total"]
    return 0


# def obtener_carrito_cliente_contipocomprobante(clienteid: int, tipo_comprobanteid: int = 2):
#     transaccion = obtener_transaccion_provisional(clienteid, tipo_comprobanteid)
#     if not transaccion:
#         return []

#     num_serie = transaccion.get("num_serie")

#     sql = '''
#         SELECT 
#             dv.articuloid AS id,
#             a.nombre AS name,
#             CAST(a.precio AS DECIMAL(10,2)) AS originalPrice,
#             dv.cantidad AS quantity,
#             a.img as image,

#             -- Descuentos
#             MAX(CASE 
#                 WHEN REGEXP_SUBSTR(des.nombre, '[0-9]+') IS NOT NULL AND 
#                      CAST(REGEXP_SUBSTR(des.nombre, '[0-9]+') AS UNSIGNED) = vol.min_vol THEN des_art.cantidad_descuento
#                 ELSE NULL END) AS precio_unitario_2,

#             MAX(CASE 
#                 WHEN REGEXP_SUBSTR(des.nombre, '[0-9]+') IS NOT NULL AND 
#                      CAST(REGEXP_SUBSTR(des.nombre, '[0-9]+') AS UNSIGNED) = vol.max_vol THEN des_art.cantidad_descuento
#                 ELSE NULL END) AS precio_unitario_3,

#             vol.min_vol AS cantidad_precio_unitario_2,
#             vol.max_vol AS cantidad_precio_unitario_3

#         FROM detalle_venta dv
#         JOIN articulo a ON dv.articuloid = a.id
#         LEFT JOIN descuento_articulo des_art ON des_art.articuloid = a.id
#         LEFT JOIN descuento des ON des.id = des_art.descuentoid

#         LEFT JOIN (
#             SELECT 
#                 da.articuloid,
#                 MIN(CAST(REGEXP_SUBSTR(d.nombre, '[0-9]+') AS UNSIGNED)) AS min_vol,
#                 MAX(CAST(REGEXP_SUBSTR(d.nombre, '[0-9]+') AS UNSIGNED)) AS max_vol
#             FROM descuento_articulo da
#             JOIN descuento d ON d.id = da.descuentoid
#             GROUP BY da.articuloid
#         ) AS vol ON vol.articuloid = a.id

#         WHERE dv.ventanum_serie = %s AND dv.ventatipo_comprobanteid = %s
#         GROUP BY dv.articuloid, a.nombre, a.precio, dv.cantidad, a.img, vol.min_vol, vol.max_vol
#     '''

#     return sql_select_fetchall(sql, (num_serie, tipo_comprobanteid))

def obtener_detalle_venta(num_serie):
    """
    Obtiene los artículos vendidos en una transacción
    """
    try:
        sql = '''
            SELECT 
                dv.articuloid,
                dv.cantidad,
                a.nombre as articulo_nombre,
                a.precio as precio_unitario,
                (dv.cantidad * a.precio) as subtotal,
                a.dimensiones,
                tc.nombre as tamaño_caja
            FROM detalle_venta dv
            INNER JOIN articulo a ON dv.articuloid = a.id
            LEFT JOIN tamanio_caja tc ON a.tamaño_cajaid = tc.id
            WHERE dv.ventanum_serie = %s
            AND a.activo = 1
        '''
        
        # Usar fetchall en lugar de fetchone para obtener todos los registros
        result = sql_select_fetchall(sql, (num_serie,))
        
        print(f"Debug - Resultado de la consulta: {result}")
        print(f"Debug - Tipo de resultado: {type(result)}")
        
        # Verificar que result sea una lista
        if not isinstance(result, list):
            print(f"Error: La consulta devolvió {type(result)} en lugar de lista: {result}")
            return []
        
        if not result:
            print(f"No se encontraron artículos para la venta {num_serie}")
            return []
        
        items = []
        for row in result:
            # Verificar que row sea un diccionario
            if not isinstance(row, dict):
                print(f"Error: La fila no es un diccionario: {row} (tipo: {type(row)})")
                continue
                
            try:
                item = {
                    'codigo': str(row.get('articuloid', '')),
                    'descripcion': str(row.get('articulo_nombre', '')),
                    'cantidad': float(row.get('cantidad', 1)),
                    'precio_unitario': float(row.get('precio_unitario', 0)),
                    'subtotal': float(row.get('subtotal', 0)),
                    'dimensiones': str(row.get('dimensiones', '') or ''),
                    'tamaño': str(row.get('tamaño_caja', '') or '')
                }
                items.append(item)
                print(f"Debug - Item agregado: {item}")
                
            except Exception as item_error:
                print(f"Error al procesar item: {item_error}, row: {row}")
                continue
        
        print(f"Debug - Total items procesados: {len(items)}")
        return items
        
    except Exception as e:
        print(f"Error al obtener detalle de venta: {e}")
        print(f"Debug - num_serie: {num_serie}, tipo: {type(num_serie)}")
        return []


# Función alternativa si la anterior no funciona
def obtener_detalle_venta_alternativa(num_serie):
    """
    Versión alternativa usando una consulta más simple
    """
    try:
        # Consulta más simple para debugging
        sql = '''
            SELECT 
                dv.articuloid,
                dv.cantidad,
                a.nombre,
                a.precio
            FROM detalle_venta dv
            INNER JOIN articulo a ON dv.articuloid = a.id
            WHERE dv.ventanum_serie = %s
        '''
        
        result = sql_select_fetchall(sql, (num_serie,))
        
        print(f"Debug alternativa - Resultado: {result}")
        print(f"Debug alternativa - Tipo: {type(result)}")
        
        if not isinstance(result, list):
            return []
        
        items = []
        for row in result:
            if isinstance(row, dict):
                item = {
                    'codigo': str(row.get('articuloid', '')),
                    'descripcion': str(row.get('nombre', '')),
                    'cantidad': float(row.get('cantidad', 1)),
                    'precio_unitario': float(row.get('precio', 0)),
                    'subtotal': float(row.get('cantidad', 1)) * float(row.get('precio', 0)),
                    'dimensiones': '',
                    'tamaño': ''
                }
                items.append(item)
            elif isinstance(row, (list, tuple)) and len(row) >= 4:
                # Si viene como tupla/lista
                item = {
                    'codigo': str(row[0]),
                    'descripcion': str(row[2]),
                    'cantidad': float(row[1]),
                    'precio_unitario': float(row[3]),
                    'subtotal': float(row[1]) * float(row[3]),
                    'dimensiones': '',
                    'tamaño': ''
                }
                items.append(item)
        
        return items
        
    except Exception as e:
        print(f"Error en consulta alternativa: {e}")
        return []


# Función de debugging para verificar la estructura de datos
def debug_detalle_venta(num_serie):
    """
    Función para hacer debugging de la consulta
    """
    print(f"=== DEBUG DETALLE VENTA ===")
    print(f"num_serie: {num_serie} (tipo: {type(num_serie)})")
    
    try:
        # Verificar que existe la venta
        sql_venta = "SELECT * FROM transaccion_venta WHERE num_serie = %s"
        venta = sql_select_fetchone(sql_venta, (num_serie,))
        print(f"Venta encontrada: {venta}")
        
        # Verificar detalle_venta
        sql_detalle = "SELECT * FROM detalle_venta WHERE ventanum_serie = %s"
        detalle = sql_select_fetchall(sql_detalle, (num_serie,))
        print(f"Detalle encontrado: {detalle}")
        print(f"Tipo de detalle: {type(detalle)}")
        
        # Verificar artículos
        if isinstance(detalle, list) and detalle:
            for item in detalle:
                if isinstance(item, dict):
                    articulo_id = item.get('articuloid')
                    sql_articulo = "SELECT * FROM articulo WHERE id = %s"
                    articulo = sql_select_fetchone(sql_articulo, (articulo_id,))
                    print(f"Artículo {articulo_id}: {articulo}")
        
    except Exception as e:
        print(f"Error en debug: {e}")
    
    print(f"=== FIN DEBUG ===")
    
    # Intentar obtener el detalle normal
    return obtener_detalle_venta(num_serie)


# Agregar a controlador_transaccion_venta.py
def obtener_transaccion_por_num_serie(num_serie):
    """
    Obtiene una transacción de venta por su número de serie
    """
    try:
        sql = '''
            SELECT 
                tv.num_serie,
                tv.tipo_comprobanteid,
                tv.estado,
                tv.monto_total,
                tv.fecha,
                tv.hora,
                tv.clienteid,
                tc.nombre as tipo_comprobante_nombre
            FROM transaccion_venta tv
            LEFT JOIN tipo_comprobante tc ON tv.tipo_comprobanteid = tc.id
            WHERE tv.num_serie = %s
        '''
        
        result = sql_select_fetchone(sql, (num_serie,))
        return result
        
    except Exception as e:
        print(f"Error al obtener transacción: {e}")
# Agregar a controlador_cliente.py
def obtener_cliente_por_id(cliente_id):
    """
    Obtiene los datos completos de un cliente por su ID
    """
    try:
        sql = '''
            SELECT 
                c.id,
                c.correo,
                c.telefono,
                c.num_documento,
                c.nombre_siglas,
                c.apellidos_razon,
                td.siglas as tipo_documento,
                tc.nombre as tipo_cliente
            FROM cliente c
            LEFT JOIN tipo_documento td ON c.tipo_documentoid = td.id
            LEFT JOIN tipo_cliente tc ON c.tipo_clienteid = tc.id
            WHERE c.id = %s
        '''
        
        result = sql_select_fetchone(sql, (cliente_id,))
        return result
        
    except Exception as e:
        print(f"Error al obtener cliente por ID: {e}")
        return None
