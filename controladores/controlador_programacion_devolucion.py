from controladores.bd import sql_execute, sql_select_fetchone, sql_select_fetchall
from datetime import datetime

# Función para buscar paquetes por tracking
def buscar_paquete(tracking):
    """
    Busca un paquete por número de tracking
    """
    sql = """
    SELECT 
        p.tracking,
        p.nombres_contacto_destinatario,
        p.apellidos_razon_destinatario,
        CONCAT(p.nombres_contacto_destinatario, ' ', p.apellidos_razon_destinatario) as destinatario_completo,
        p.telefono_destinatario,
        p.peso,
        CONCAT(p.largo, 'x', p.ancho, 'x', p.alto, ' cm') as dimensiones,
        p.valor,
        so.direccion as sucursal_origen,
        so.abreviatura as sucursal_origen_abrev,
        sd.direccion as sucursal_destino,
        sd.abreviatura as sucursal_destino_abrev,
        te.num_serie,
        u_actual.placa as unidad_actual_placa,
        mo.nombre as unidad_actual_modelo,
        CONCAT(u_actual.placa, ' (', mo.nombre, ')') as unidad_actual,
        de.nombre as estado_actual
    FROM paquete p
    INNER JOIN transaccion_encomienda te ON p.transaccion_encomienda_num_serie = te.num_serie
    INNER JOIN sucursal so ON te.id_sucursal_origen = so.id
    INNER JOIN sucursal sd ON p.sucursal_destino_id = sd.id
    LEFT JOIN salida s ON p.salidaid = s.id
    LEFT JOIN unidad u_actual ON s.unidadid = u_actual.id
    LEFT JOIN modelo mo ON u_actual.modeloid = mo.id
    LEFT JOIN seguimiento seg ON p.tracking = seg.paquetetracking
    LEFT JOIN detalle_estado de ON seg.detalle_estadoid = de.id
    WHERE p.tracking = %s
    AND p.estado_pago != 'E'
    ORDER BY seg.fecha DESC, seg.hora DESC
    LIMIT 1
    """
    result = sql_select_fetchone(sql, (tracking,))
    # print("Tracking:", tracking)
    # print("Resultado:", result)
    return result

# Función para obtener unidades disponibles para devolución
def obtener_unidades_disponibles(tracking_paquete):
    """
    Obtiene las unidades disponibles para asignar devoluciones
    que tengan una salida programada (estado 'P') con origen en la sucursal destino del paquete
    y destino en la sucursal origen del paquete
    """
    # Primero obtenemos las sucursales del paquete
    sql_paquete = """
    SELECT 
        te.id_sucursal_origen,
        p.sucursal_destino_id
    FROM paquete p
    INNER JOIN transaccion_encomienda te ON p.transaccion_encomienda_num_serie = te.num_serie
    WHERE p.tracking = %s
    """
    
    paquete_info = sql_select_fetchone(sql_paquete, (tracking_paquete,))
    
    if not paquete_info:
        return []
    
    sucursal_origen_paquete = paquete_info['id_sucursal_origen']
    sucursal_destino_paquete = paquete_info['sucursal_destino_id']
    
    # Ahora buscamos unidades con salidas programadas que vayan en dirección contraria
    sql = """
    SELECT 
        u.id,
        u.placa,
        mo.nombre as modelo,
        u.capacidad,
        u.volumen,
        u.estado,
        s.id as salida_id,
        so_origen.direccion as origen_salida,
        so_destino.direccion as destino_salida,
        COALESCE(ocupacion.peso_ocupado, 0) as peso_ocupado,
        ROUND((COALESCE(ocupacion.peso_ocupado, 0) / u.capacidad) * 100, 0) as porcentaje_ocupacion,
        CASE 
            WHEN u.estado = 'A' THEN 'Activo/Disponible'
            WHEN u.estado = 'M' THEN 'En Mantenimiento' 
            WHEN u.estado = 'I' THEN 'Inactivo'
            ELSE 'Desconocido'
        END as estado_texto
    FROM unidad u
    INNER JOIN modelo mo ON u.modeloid = mo.id
    INNER JOIN salida s ON u.id = s.unidadid
    INNER JOIN sucursal so_origen ON s.origen_inicio_id = so_origen.id
    INNER JOIN sucursal so_destino ON s.destino_final_id = so_destino.id
    LEFT JOIN (
        SELECT 
            s_sub.unidadid,
            SUM(p_sub.peso) as peso_ocupado
        FROM salida s_sub
        INNER JOIN paquete p_sub ON s_sub.id = p_sub.salidaid
        WHERE s_sub.estado IN ('P', 'T')  -- Programada o en tránsito
        GROUP BY s_sub.unidadid
    ) ocupacion ON u.id = ocupacion.unidadid
    WHERE s.estado = 'P'  -- Salida programada (pendiente)
    AND s.origen_inicio_id = %s  -- Origen de la salida = destino del paquete
    AND s.destino_final_id = %s  -- Destino de la salida = origen del paquete
    AND u.estado = 'A'  -- Unidad activa
    ORDER BY porcentaje_ocupacion ASC, s.fecha ASC, s.hora ASC
    """
    # print(sql_select_fetchall(sql, (sucursal_destino_paquete, sucursal_origen_paquete)))
    return sql_select_fetchall(sql, (sucursal_destino_paquete, sucursal_origen_paquete))


def programar_devolucion(tracking, unidad_id):
    """
    Programa la devolución de un paquete asignándolo a una unidad específica
    """
    try:
        # Obtener el ID de la salida de la unidad seleccionada
        salida_info = sql_select_fetchone("""
            SELECT id 
            FROM salida 
            WHERE unidadid = %s AND estado = 'P'
            ORDER BY fecha ASC, hora ASC
            LIMIT 1
        """, (unidad_id,))
        
        if not salida_info:
            raise Exception("No se encontró una salida programada para la unidad seleccionada")
        
        salida_id = salida_info['id']
        
        # Actualizar el paquete para asignarlo a esta salida
        sql_update_paquete = """
        UPDATE paquete 
        SET salidaid = %s
        WHERE tracking = %s
        """
        
        sql_execute(sql_update_paquete, (salida_id, tracking))
        
        # Cambiar el seguimiento de estado 17 a estado 22
        ahora = datetime.now()
        fecha_actual = ahora.date()
        hora_actual = ahora.time()
        
        sql_seguimiento = """
        INSERT INTO seguimiento (paquetetracking, detalle_estadoid, fecha, hora)
        VALUES (%s, %s, %s, %s)
        """
        sql_execute(sql_seguimiento, (tracking, 22, fecha_actual, hora_actual))
        
        return {
            'success': True,
            'message': 'Devolución programada exitosamente',
            'salida_id': salida_id
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error al programar devolución: {str(e)}'
        }

# Función para obtener estados de paquete disponibles
def obtener_estados_devolucion():
    """
    Obtiene los estados relacionados con devoluciones
    """
    sql = """
    SELECT id, nombre, descripcion
    FROM detalle_estado de
    INNER JOIN estado_encomienda ee ON de.estado_encomiendaid = ee.id
    WHERE de.nombre LIKE '%devoluc%' OR de.nombre LIKE '%retorn%' OR de.nombre LIKE '%devolu%'
    ORDER BY de.nombre
    """
    
    return sql_execute(sql)

# Función para validar si un paquete puede ser devuelto
def validar_paquete_para_devolucion(tracking):
    """
    Valida si un paquete puede ser programado para devolución
    """
    sql = """
    SELECT 
        p.tracking,
        p.estado_pago,
        COUNT(s.paquetetracking) as seguimientos
    FROM paquete p
    LEFT JOIN seguimiento s ON p.tracking = s.paquetetracking
    LEFT JOIN detalle_estado de ON s.detalle_estadoid = de.id
    WHERE p.tracking = %s
    AND p.estado_pago NOT IN ('E', 'D')  -- No entregado ni en devolución
    GROUP BY p.tracking, p.estado_pago
    """
    
    result = sql_select_fetchall(sql, (tracking,))
    return len(result) > 0 and result[0]['seguimientos'] > 0

# Función para obtener historial de devoluciones
def obtener_historial_devoluciones(limit=50):
    """
    Obtiene el historial de devoluciones programadas
    """
    sql = """
    SELECT 
        p.tracking,
        CONCAT(p.nombres_contacto_destinatario, ' ', p.apellidos_razon_destinatario) as destinatario,
        u.placa,
        mo.nombre as modelo_unidad,
        s.fecha as fecha_devolucion,
        s.hora as hora_devolucion,
        s.estado as estado_salida,
        so.direccion as origen_devolucion,
        sd.direccion as destino_devolucion
    FROM paquete p
    INNER JOIN salida s ON p.salidaid = s.id
    INNER JOIN unidad u ON s.unidadid = u.id
    INNER JOIN modelo mo ON u.modeloid = mo.id
    INNER JOIN sucursal so ON s.origen_inicio_id = so.id
    INNER JOIN sucursal sd ON s.destino_final_id = sd.id
    WHERE p.estado_pago = 'D'  -- Estado de devolución
    ORDER BY s.fecha DESC, s.hora DESC
    LIMIT %s
    """
    
    return sql_execute(sql, (limit,))

def obtener_paquetes_estado_17():
    """
    Obtiene los paquetes que tienen seguimiento con detalle_estado_id = 17
    """
    sql = """
    SELECT DISTINCT
        p.tracking,
        CONCAT(p.nombres_contacto_destinatario, ' ', p.apellidos_razon_destinatario) as destinatario,
        p.telefono_destinatario as telefono,
        so.direccion as sucursal_origen,
        so.abreviatura as origen_abrev,
        sd.direccion as sucursal_destino,
        sd.abreviatura as destino_abrev,
        DATE_FORMAT(s.fecha, '%d/%m/%Y') as fecha_estado,
        TIME_FORMAT(s.hora, '%H:%i') as hora_estado,
        p.peso,
        p.valor
    FROM paquete p
    INNER JOIN transaccion_encomienda te ON p.transaccion_encomienda_num_serie = te.num_serie
    INNER JOIN sucursal so ON te.id_sucursal_origen = so.id
    INNER JOIN sucursal sd ON p.sucursal_destino_id = sd.id
    INNER JOIN seguimiento s ON p.tracking = s.paquetetracking
    WHERE s.detalle_estadoid = 17
    AND p.estado_pago NOT IN ('E', 'D')  -- No entregado ni en devolución
    ORDER BY s.fecha DESC, s.hora DESC
    """
    print(sql_select_fetchall(sql))
    return sql_select_fetchall(sql)