from controladores.bd import sql_select_fetchall, sql_select_fetchone, sql_execute
from datetime import datetime, timedelta

def get_paquetes_pendientes_devolucion(sucursal_origen=None, dias_limite=7, estado_actual=None):
    """
    Obtiene paquetes que están pendientes de devolución
    """
    where_conditions = []
    params = []
    
    # Paquetes que han pasado el tiempo límite sin ser entregados
    fecha_limite = datetime.now() - timedelta(days=dias_limite)
    where_conditions.append("te.fecha <= %s")
    params.append(fecha_limite.date())
    
    # Estados que indican que el paquete no fue entregado
    estados_no_entregados = ['En ruta de entrega', 'En sucursal destino', 'Intentos de entrega fallidos']
    where_conditions.append("ee.nombre IN %s")
    params.append(tuple(estados_no_entregados))
    
    if sucursal_origen:
        where_conditions.append("te.id_sucursal_origen = %s")
        params.append(sucursal_origen)
    
    if estado_actual:
        where_conditions.append("ee.id = %s")
        params.append(estado_actual)
    
    where_clause = " AND ".join(where_conditions)
    
    sql = f'''
        SELECT DISTINCT
            p.tracking,
            p.clave,
            p.nombres_contacto_destinatario,
            p.apellidos_razon_destinatario,
            p.telefono_destinatario,
            p.valor,
            p.peso,
            CONCAT(p.alto, 'x', p.ancho, 'x', p.largo) as dimensiones,
            
            -- Información de origen
            so.direccion as sucursal_origen,
            so.abreviatura as abrev_origen,
            uo.departamento as dep_origen,
            uo.provincia as prov_origen,
            uo.distrito as dist_origen,
            
            -- Información de destino
            sd.direccion as sucursal_destino,
            sd.abreviatura as abrev_destino,
            ud.departamento as dep_destino,
            ud.provincia as prov_destino,
            ud.distrito as dist_destino,
            
            -- Estado actual
            ee.nombre as estado_actual,
            de.nombre as detalle_estado,
            s.fecha as fecha_ultimo_estado,
            s.hora as hora_ultimo_estado,
            
            -- Información de transacción
            te.fecha as fecha_envio,
            te.num_serie,
            DATEDIFF(CURDATE(), te.fecha) as dias_transcurridos,
            
            -- Cliente remitente
            CONCAT(c.nombre_siglas, ' ', c.apellidos_razon) as remitente,
            c.telefono as tel_remitente
            
        FROM paquete p
        INNER JOIN transaccion_encomienda te ON te.num_serie = p.transaccion_encomienda_num_serie
        INNER JOIN cliente c ON c.id = te.clienteid
        INNER JOIN sucursal so ON so.id = te.id_sucursal_origen
        INNER JOIN ubigeo uo ON uo.codigo = so.ubigeocodigo
        INNER JOIN sucursal sd ON sd.id = p.sucursal_destino_id
        INNER JOIN ubigeo ud ON ud.codigo = sd.ubigeocodigo
        
        -- Obtener el último estado del paquete
        INNER JOIN (
            SELECT 
                paquetetracking,
                MAX(CONCAT(fecha, ' ', hora)) as ultimo_momento
            FROM seguimiento
            GROUP BY paquetetracking
        ) ultimo ON ultimo.paquetetracking = p.tracking
        
        INNER JOIN seguimiento s ON s.paquetetracking = p.tracking 
            AND CONCAT(s.fecha, ' ', s.hora) = ultimo.ultimo_momento
        INNER JOIN detalle_estado de ON de.id = s.detalle_estadoid
        INNER JOIN estado_encomienda ee ON ee.id = de.estado_encomiendaid
        
        WHERE {where_clause}
        AND p.tracking NOT IN (
            SELECT DISTINCT paquetetracking 
            FROM seguimiento s2
            INNER JOIN detalle_estado de2 ON de2.id = s2.detalle_estadoid
            INNER JOIN estado_encomienda ee2 ON ee2.id = de2.estado_encomiendaid
            WHERE ee2.nombre IN ('Entregado', 'En devolución', 'Devuelto')
        )
        
        ORDER BY te.fecha ASC, p.tracking
    '''
    
    filas = sql_select_fetchall(sql, params)
    
    columnas = {
        'tracking': ['Tracking', 1.5],
        'clave': ['Clave', 1],
        'nombres_contacto_destinatario': ['Destinatario', 2],
        'telefono_destinatario': ['Teléfono', 1.2],
        'sucursal_origen': ['Origen', 2],
        'sucursal_destino': ['Destino', 2],
        'estado_actual': ['Estado', 1.5],
        'dias_transcurridos': ['Días', 0.8],
        'fecha_envio': ['F. Envío', 1],
        'valor': ['Valor S/.', 1],
    }
    
    return columnas, filas


def buscar_paquete_por_criterio(criterio):
    """
    Busca un paquete específico por tracking o nombre de destinatario
    """
    sql = '''
        SELECT 
            p.tracking,
            p.clave,
            p.nombres_contacto_destinatario,
            p.apellidos_razon_destinatario,
            p.telefono_destinatario,
            p.direccion_destinatario,
            p.valor,
            p.peso,
            CONCAT(p.alto, 'x', p.ancho, 'x', p.largo) as dimensiones,
            
            -- Información de origen
            so.direccion as sucursal_origen,
            so.abreviatura as abrev_origen,
            
            -- Información de destino  
            sd.direccion as sucursal_destino,
            sd.abreviatura as abrev_destino,
            
            -- Estado actual
            ee.nombre as estado_actual,
            de.nombre as detalle_estado,
            
            -- Información de transacción
            te.fecha as fecha_envio,
            te.num_serie,
            te.id_sucursal_origen,
            
            -- Unidad actual si existe
            u.placa as unidad_actual,
            CONCAT(m.nombre, ' ', ma.nombre) as modelo_unidad
            
        FROM paquete p
        INNER JOIN transaccion_encomienda te ON te.num_serie = p.transaccion_encomienda_num_serie
        INNER JOIN sucursal so ON so.id = te.id_sucursal_origen
        INNER JOIN sucursal sd ON sd.id = p.sucursal_destino_id
        
        -- Obtener el último estado
        INNER JOIN (
            SELECT 
                paquetetracking,
                MAX(CONCAT(fecha, ' ', hora)) as ultimo_momento
            FROM seguimiento
            GROUP BY paquetetracking
        ) ultimo ON ultimo.paquetetracking = p.tracking
        
        INNER JOIN seguimiento s ON s.paquetetracking = p.tracking 
            AND CONCAT(s.fecha, ' ', s.hora) = ultimo.ultimo_momento
        INNER JOIN detalle_estado de ON de.id = s.detalle_estadoid
        INNER JOIN estado_encomienda ee ON ee.id = de.estado_encomiendaid
        
        -- Unidad actual (opcional)
        LEFT JOIN salida sal ON sal.id = p.salidaid
        LEFT JOIN unidad u ON u.id = sal.unidadid
        LEFT JOIN modelo mo ON mo.id = u.modeloid
        LEFT JOIN marca ma ON ma.id = mo.marcaid
        LEFT JOIN tipo_unidad tu ON tu.id = mo.tipo_unidadid
        LEFT JOIN modelo m ON m.id = mo.id
        
        WHERE (
            p.tracking = %s 
            OR p.clave LIKE %s
            OR CONCAT(p.nombres_contacto_destinatario, ' ', p.apellidos_razon_destinatario) LIKE %s
        )
    '''
    
    like_criterio = f'%{criterio}%'
    return sql_select_fetchone(sql, (criterio, like_criterio, like_criterio))


def programar_devolucion(tracking, unidad_id, observaciones=None):
    """
    Programa la devolución de un paquete asignándolo a una unidad
    """
    try:
        # Verificar que el paquete existe y su estado actual
        paquete = sql_select_fetchone('''
            SELECT p.*, te.id_sucursal_origen
            FROM paquete p
            INNER JOIN transaccion_encomienda te ON te.num_serie = p.transaccion_encomienda_num_serie
            WHERE p.tracking = %s
        ''', (tracking,))
        
        if not paquete:
            return {"success": False, "message": "Paquete no encontrado"}
        
        # Verificar que la unidad está disponible
        unidad = sql_select_fetchone('''
            SELECT u.*, m.nombre as modelo, ma.nombre as marca
            FROM unidad u
            INNER JOIN modelo m ON m.id = u.modeloid
            INNER JOIN marca ma ON ma.id = m.marcaid
            WHERE u.id = %s AND u.estado = 'A'
        ''', (unidad_id,))
        
        if not unidad:
            return {"success": False, "message": "Unidad no disponible"}
        
        # Crear una salida para la devolución
        fecha_actual = datetime.now()
        
        salida_id = sql_execute('''
            INSERT INTO salida 
            (fecha, hora, recojo, entrega, estado, unidadid, origen_inicio_id, destino_final_id, conductor_principal)
            VALUES (%s, %s, 0, 1, 'P', %s, %s, %s, 1)
        ''', (
            fecha_actual.date(),
            fecha_actual.time(),
            unidad_id,
            paquete['sucursal_destino_id'],  # Origen: donde está el paquete
            paquete['id_sucursal_origen']    # Destino: sucursal de origen original
        ), return_lastrowid=True)
        
        # Actualizar el paquete con la nueva salida
        sql_execute('''
            UPDATE paquete 
            SET salidaid = %s 
            WHERE tracking = %s
        ''', (salida_id, tracking))
        
        # Registrar el estado "En devolución"
        # Primero buscar el ID del estado "En devolución"
        estado_devolucion = sql_select_fetchone('''
            SELECT de.id
            FROM detalle_estado de
            INNER JOIN estado_encomienda ee ON ee.id = de.estado_encomiendaid
            WHERE ee.nombre = 'En devolución'
            LIMIT 1
        ''')
        
        if estado_devolucion:
            sql_execute('''
                INSERT INTO seguimiento
                (paquetetracking, detalle_estadoid, fecha, hora)
                VALUES (%s, %s, %s, %s)
            ''', (
                tracking,
                estado_devolucion['id'],
                fecha_actual.date(),
                fecha_actual.time()
            ))
        
        return {
            "success": True, 
            "message": "Devolución programada exitosamente",
            "salida_id": salida_id,
            "unidad": f"{unidad['placa']} - {unidad['marca']} {unidad['modelo']}"
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error al programar devolución: {str(e)}"}


def get_unidades_disponibles():
    """
    Obtiene las unidades disponibles para asignar devoluciones
    """
    sql = '''
        SELECT 
            u.id,
            u.placa,
            u.capacidad,
            u.volumen,
            u.estado,
            CONCAT(ma.nombre, ' ', m.nombre) as modelo_completo,
            tu.nombre as tipo_unidad,
            
            -- Calcular ocupación actual
            COALESCE(ocupacion.paquetes_asignados, 0) as paquetes_asignados,
            COALESCE(ocupacion.peso_total, 0) as peso_ocupado,
            ROUND((COALESCE(ocupacion.peso_total, 0) / u.capacidad) * 100, 2) as porcentaje_ocupacion
            
        FROM unidad u
        INNER JOIN modelo m ON m.id = u.modeloid
        INNER JOIN marca ma ON ma.id = m.marcaid
        INNER JOIN tipo_unidad tu ON tu.id = m.tipo_unidadid
        
        LEFT JOIN (
            SELECT 
                sal.unidadid,
                COUNT(p.tracking) as paquetes_asignados,
                SUM(p.peso) as peso_total
            FROM salida sal
            INNER JOIN paquete p ON p.salidaid = sal.id
            WHERE sal.estado IN ('P', 'E')  -- Pendiente o En ruta
            GROUP BY sal.unidadid
        ) ocupacion ON ocupacion.unidadid = u.id
        
        WHERE u.estado = 'A'  -- Solo unidades activas
        ORDER BY porcentaje_ocupacion ASC, u.placa
    '''
    
    return sql_select_fetchall(sql)


def get_opciones_sucursales_origen():
    """
    Obtiene las sucursales que han sido origen de encomiendas
    """
    sql = '''
        SELECT DISTINCT
            s.id,
            s.abreviatura,
            s.direccion,
            CONCAT(u.departamento, ' - ', u.provincia, ' - ', u.distrito) as ubigeo_completo
        FROM sucursal s
        INNER JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        INNER JOIN transaccion_encomienda te ON te.id_sucursal_origen = s.id
        WHERE s.activo = 1
        ORDER BY s.abreviatura
    '''
    
    return sql_select_fetchall(sql)


def get_estadisticas_devolucion():
    """
    Obtiene estadísticas generales de devoluciones
    """
    sql = '''
        SELECT 
            COUNT(CASE WHEN ee.nombre IN ('En ruta de entrega', 'En sucursal destino') 
                       AND DATEDIFF(CURDATE(), te.fecha) > 7 THEN 1 END) as pendientes_devolucion,
            COUNT(CASE WHEN ee.nombre = 'En devolución' THEN 1 END) as en_devolucion,
            COUNT(CASE WHEN ee.nombre = 'Devuelto' THEN 1 END) as devueltos,
            AVG(CASE WHEN ee.nombre = 'Devuelto' 
                     THEN DATEDIFF(s.fecha, te.fecha) END) as promedio_dias_devolucion
        FROM paquete p
        INNER JOIN transaccion_encomienda te ON te.num_serie = p.transaccion_encomienda_num_serie
        INNER JOIN (
            SELECT 
                paquetetracking,
                MAX(CONCAT(fecha, ' ', hora)) as ultimo_momento
            FROM seguimiento
            GROUP BY paquetetracking
        ) ultimo ON ultimo.paquetetracking = p.tracking
        INNER JOIN seguimiento s ON s.paquetetracking = p.tracking 
            AND CONCAT(s.fecha, ' ', s.hora) = ultimo.ultimo_momento
        INNER JOIN detalle_estado de ON de.id = s.detalle_estadoid
        INNER JOIN estado_encomienda ee ON ee.id = de.estado_encomiendaid
    '''
    
    return sql_select_fetchone(sql)