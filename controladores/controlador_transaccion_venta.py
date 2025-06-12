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


def agregar_detalle_venta(articuloid, ventanum_serie, ventatipo_comprobanteid, cantidad):
    sql = '''
        INSERT INTO detalle_venta (articuloid, ventanum_serie, ventatipo_comprobanteid, cantidad)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE cantidad = VALUES(cantidad)
    '''
    return sql_execute(sql, (articuloid, ventanum_serie, ventatipo_comprobanteid, cantidad))

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
    agregar_detalle_venta(articuloid, num_serie, tipo_comprobanteid, cantidad)

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
