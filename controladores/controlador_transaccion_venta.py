from controladores.bd import (
    sql_execute_lastrowid,
    sql_execute,
    sql_select_fetchone
)


def obtener_transaccion_provisional(clienteid, tipo_comprobanteid=2):
    sql = '''
        SELECT num_serie FROM transaccion_venta
        WHERE clienteid = %s AND tipo_comprobanteid = %s AND estado = 0
        ORDER BY num_serie DESC
        LIMIT 1
    '''
    result = sql_select_fetchone(sql, (clienteid, tipo_comprobanteid))
    
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


def actualizar_monto_total(ventanum_serie, ventatipo_comprobanteid):
    sql = '''
        SELECT SUM(dv.cantidad * a.precio) AS total
        FROM detalle_venta dv
        JOIN articulo a ON dv.articuloid = a.id
        WHERE dv.ventanum_serie = %s AND dv.ventatipo_comprobanteid = %s
    '''
    total = sql_select_fetchone(sql, (ventanum_serie, ventatipo_comprobanteid))
    if total and total.get("total") is not None:
        update_sql = '''
            UPDATE transaccion_venta
            SET monto_total = %s
            WHERE num_serie = %s
        '''
        return sql_execute(update_sql, (total["total"], ventanum_serie))


def registrar_detalle_venta(clienteid, tipo_comprobanteid, articuloid, cantidad):
    # Paso 1: Buscar si ya existe transacción provisional
    transaccion = obtener_transaccion_provisional(clienteid, tipo_comprobanteid)

    if not transaccion:
        # Paso 2: Crear transacción provisional nueva
        num_serie = crear_transaccion_provisional(tipo_comprobanteid, 0, clienteid)
    else:
        num_serie = transaccion["num_serie"]

    # Paso 3: Insertar detalle de venta
    agregar_detalle_venta(articuloid, num_serie, tipo_comprobanteid, cantidad)

    # Paso 4: Actualizar total
    actualizar_monto_total(num_serie, tipo_comprobanteid)

    return num_serie
