from controladores.bd import sql_select_fetchall, sql_select_fetchone, sql_execute, sql_execute_lastrowid

def get_estadisticas_cliente(cliente_id):
    """Obtiene estadísticas del cliente"""
    try:
        # Consulta más simple para evitar errores
        sql = """
        SELECT 
            COUNT(p.tracking) as total_envios,
            SUM(CASE WHEN p.estado_pago = 'C' THEN 1 ELSE 0 END) as entregados,
            SUM(CASE WHEN p.estado_pago = 'T' THEN 1 ELSE 0 END) as en_transito,
            SUM(CASE WHEN p.estado_pago = 'P' THEN 1 ELSE 0 END) as pendientes
        FROM transaccion_encomienda te
        LEFT JOIN paquete p ON te.num_serie = p.transaccion_encomienda_num_serie
        WHERE te.clienteid = %s
        """
        
        result = sql_select_fetchone(sql, (cliente_id,))
        
        # Verificar si result es un Exception
        if isinstance(result, Exception):
            print(f"Error en consulta estadísticas: {result}")
            return {
                'total_envios': 0,
                'entregados': 0,
                'en_transito': 0,
                'pendientes': 0
            }
        
        if result:
            return {
                'total_envios': result['total_envios'] or 0,
                'entregados': result['entregados'] or 0,
                'en_transito': result['en_transito'] or 0,
                'pendientes': result['pendientes'] or 0
            }
        else:
            return {
                'total_envios': 0,
                'entregados': 0,
                'en_transito': 0,
                'pendientes': 0
            }
            
    except Exception as e:
        print(f"Error en get_estadisticas_cliente: {e}")
        return {
            'total_envios': 0,
            'entregados': 0,
            'en_transito': 0,
            'pendientes': 0
        }

def get_reclamos_cliente(cliente_id):
    """Obtiene la cantidad de reclamos del cliente"""
    try:
        sql = """
        SELECT COUNT(*) as total_reclamos
        FROM reclamo r
        INNER JOIN paquete p ON r.paquetetracking = p.tracking
        INNER JOIN transaccion_encomienda te ON p.transaccion_encomienda_num_serie = te.num_serie
        WHERE te.clienteid = %s
        """
        
        result = sql_select_fetchone(sql, (cliente_id,))
        
        # Verificar si result es un Exception
        if isinstance(result, Exception):
            print(f"Error en consulta reclamos: {result}")
            return 0
            
        return result['total_reclamos'] if result else 0
        
    except Exception as e:
        print(f"Error en get_reclamos_cliente: {e}")
        return 0

def get_paquetes_cliente(cliente_id):
    """Obtiene los paquetes del cliente con información de seguimiento"""
    try:
        # Consulta simplificada
        sql = """
        SELECT 
            te.num_serie as num_comprobante,
            p.tracking as num_seguimiento,
            suc_origen.direccion as origen,
            suc_destino.direccion as destino,
            te.fecha as fecha_envio,
            p.estado_pago,
            CASE p.estado_pago
                WHEN 'C' THEN 'Completado'
                WHEN 'P' THEN 'Pendiente' 
                WHEN 'T' THEN 'En tránsito'
                ELSE 'Sin estado'
            END as estado_nombre,
            CASE p.estado_pago
                WHEN 'C' THEN 'delivered'
                WHEN 'P' THEN 'pending'
                WHEN 'T' THEN 'transit'
                ELSE 'pending'
            END as estado_clase,
            p.nombres_contacto_destinatario,
            p.apellidos_razon_destinatario,
            p.valor,
            COALESCE(cp.nombre, 'Sin especificar') as contenido
        FROM transaccion_encomienda te
        INNER JOIN paquete p ON te.num_serie = p.transaccion_encomienda_num_serie
        LEFT JOIN sucursal suc_origen ON te.id_sucursal_origen = suc_origen.id
        LEFT JOIN sucursal suc_destino ON p.sucursal_destino_id = suc_destino.id
        LEFT JOIN contenido_paquete cp ON p.contenido_paqueteid = cp.id
        WHERE te.clienteid = %s
        ORDER BY te.fecha DESC, te.hora DESC
        LIMIT 20
        """
        
        result = sql_select_fetchall(sql, (cliente_id,))
        
        # Verificar si result es un Exception
        if isinstance(result, Exception):
            print(f"Error en consulta paquetes: {result}")
            return []
            
        return result if result else []
        
    except Exception as e:
        print(f"Error en get_paquetes_cliente: {e}")
        return []

def get_compras_cliente(cliente_id):
    """Obtiene las compras (transacciones de venta) del cliente"""
    try:
        sql = """
        SELECT 
            tv.num_serie as num_comprobante,
            tv.fecha as fecha_compra,
            tv.monto_total,
            CASE tv.estado 
                WHEN 1 THEN 'Pagado'
                WHEN 0 THEN 'Pendiente'
                ELSE 'Desconocido'
            END as estado_pago,
            CASE tv.estado 
                WHEN 1 THEN 'delivered'
                WHEN 0 THEN 'pending'
                ELSE 'pending'
            END as estado_clase,
            tc.nombre as tipo_comprobante,
            COALESCE(mp.nombre, 'No especificado') as metodo_pago
        FROM transaccion_venta tv
        LEFT JOIN tipo_comprobante tc ON tv.tipo_comprobanteid = tc.id
        LEFT JOIN metodo_pago_venta mpv ON tv.num_serie = mpv.num_serie
        LEFT JOIN metodo_pago mp ON mpv.metodo_pagoid = mp.id
        WHERE tv.clienteid = %s
        ORDER BY tv.fecha DESC, tv.hora DESC
        LIMIT 20
        """
        
        result = sql_select_fetchall(sql, (cliente_id,))
        
        # Verificar si result es un Exception
        if isinstance(result, Exception):
            print(f"Error en consulta compras: {result}")
            return []
            
        return result if result else []
        
    except Exception as e:
        print(f"Error en get_compras_cliente: {e}")
        return []

def get_ordenes_cliente(cliente_id):
    """Obtiene las órdenes (transacciones de encomienda) del cliente"""
    try:
        sql = """
        SELECT 
            te.num_serie as num_comprobante,
            te.fecha as fecha_orden,
            COUNT(p.tracking) as total_paquetes,
            te.monto_total,
            CASE 
                WHEN COUNT(CASE WHEN p.estado_pago = 'C' THEN 1 END) = COUNT(p.tracking) THEN 'Completado'
                WHEN COUNT(CASE WHEN p.estado_pago = 'P' THEN 1 END) > 0 THEN 'Pendiente'
                ELSE 'En Proceso'
            END as estado_general,
            CASE 
                WHEN COUNT(CASE WHEN p.estado_pago = 'C' THEN 1 END) = COUNT(p.tracking) THEN 'delivered'
                WHEN COUNT(CASE WHEN p.estado_pago = 'P' THEN 1 END) > 0 THEN 'pending'
                ELSE 'transit'
            END as estado_clase,
            GROUP_CONCAT(
                CONCAT(p.tracking, ': ', COALESCE(cp.nombre, 'Sin especificar'))
                SEPARATOR '|'
            ) as paquetes_info
        FROM transaccion_encomienda te
        LEFT JOIN paquete p ON te.num_serie = p.transaccion_encomienda_num_serie
        LEFT JOIN contenido_paquete cp ON p.contenido_paqueteid = cp.id
        WHERE te.clienteid = %s
        GROUP BY te.num_serie, te.fecha, te.monto_total
        ORDER BY te.fecha DESC
        LIMIT 20
        """
        
        result = sql_select_fetchall(sql, (cliente_id,))
        
        # Verificar si result es un Exception
        if isinstance(result, Exception):
            print(f"Error en consulta ordenes: {result}")
            return []
            
        return result if result else []
        
    except Exception as e:
        print(f"Error en get_ordenes_cliente: {e}")
        return []

def get_reclamos_detalle_cliente(cliente_id):
    """Obtiene los reclamos detallados del cliente"""
    try:
        sql = """
        SELECT 
            r.id as num_reclamo,
            r.paquetetracking as num_envio,
            COALESCE(cr.nombre, 'Sin motivo') as motivo,
            r.fecha_recepcion as fecha_reclamo,
            'Sin estado' as estado,
            'pending' as estado_clase,
            r.descripcion,
            r.monto_reclamado
        FROM reclamo r
        INNER JOIN paquete p ON r.paquetetracking = p.tracking
        INNER JOIN transaccion_encomienda te ON p.transaccion_encomienda_num_serie = te.num_serie
        LEFT JOIN causa_reclamo cr ON r.causa_reclamoid = cr.id
        WHERE te.clienteid = %s
        ORDER BY r.fecha_recepcion DESC
        LIMIT 20
        """
        
        result = sql_select_fetchall(sql, (cliente_id,))
        
        # Verificar si result es un Exception
        if isinstance(result, Exception):
            print(f"Error en consulta reclamos detalle: {result}")
            return []
            
        return result if result else []
        
    except Exception as e:
        print(f"Error en get_reclamos_detalle_cliente: {e}")
        return []

def actualizar_datos_cliente(cliente_id, datos):
    """Actualiza los datos del cliente"""
    try:
        # Validar que los IDs de tipo_documento y tipo_cliente existen
        sql_check_tipo_doc = "SELECT id FROM tipo_documento WHERE id = %s AND activo = 1"
        result_tipo_doc = sql_select_fetchone(sql_check_tipo_doc, (datos['tipo_documentoid'],))
        
        sql_check_tipo_cliente = "SELECT id FROM tipo_cliente WHERE id = %s AND activo = 1"
        result_tipo_cliente = sql_select_fetchone(sql_check_tipo_cliente, (datos['tipo_clienteid'],))
        
        # Verificar si las consultas devolvieron errores
        if isinstance(result_tipo_doc, Exception):
            print(f"Error validando tipo documento: {result_tipo_doc}")
            return False
            
        if isinstance(result_tipo_cliente, Exception):
            print(f"Error validando tipo cliente: {result_tipo_cliente}")
            return False
        
        if not result_tipo_doc:
            print(f"Tipo de documento ID {datos['tipo_documentoid']} no existe")
            return False
            
        if not result_tipo_cliente:
            print(f"Tipo de cliente ID {datos['tipo_clienteid']} no existe")
            return False
        
        sql = """
        UPDATE cliente 
        SET nombre_siglas = %s,
            apellidos_razon = %s,
            correo = %s,
            telefono = %s,
            num_documento = %s,
            tipo_documentoid = %s,
            tipo_clienteid = %s
        WHERE id = %s
        """
        
        sql_execute(sql, (
            datos['nombre_siglas'],
            datos['apellidos_razon'],
            datos['correo'],
            datos['telefono'],
            datos['num_documento'],
            int(datos['tipo_documentoid']),
            int(datos['tipo_clienteid']),
            cliente_id
        ))
        
        return True
        
    except Exception as e:
        print(f"Error en actualizar_datos_cliente: {e}")
        return False

def get_opciones_tipo_documento():
    """Obtiene las opciones de tipo de documento"""
    try:
        sql = "SELECT id, nombre, siglas FROM tipo_documento WHERE activo = 1"
        result = sql_select_fetchall(sql)
        
        # Verificar si result es un Exception
        if isinstance(result, Exception):
            print(f"Error obteniendo tipos de documento: {result}")
            return []
            
        return result if result else []
    except Exception as e:
        print(f"Error en get_opciones_tipo_documento: {e}")
        return []

def get_opciones_tipo_cliente():
    """Obtiene las opciones de tipo de cliente"""
    try:
        sql = "SELECT id, nombre FROM tipo_cliente WHERE activo = 1"
        result = sql_select_fetchall(sql)
        
        # Verificar si result es un Exception
        if isinstance(result, Exception):
            print(f"Error obteniendo tipos de cliente: {result}")
            return []
            
        return result if result else []
    except Exception as e:
        print(f"Error en get_opciones_tipo_cliente: {e}")
        return []