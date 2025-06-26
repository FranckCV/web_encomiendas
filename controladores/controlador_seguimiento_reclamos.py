# controladores/controlador_seguimiento_reclamos.py

from controladores.bd import sql_execute, sql_select_fetchone, sql_select_fetchall
from datetime import datetime
from collections import defaultdict

# ===== FUNCIONES PRINCIPALES =====

def buscar_reclamo_por_id_o_documento(reclamo_id=None, numero_documento=None):
    """
    Busca un reclamo por ID o número de documento del reclamante
    """
    where_conditions = []
    params = []
    
    if reclamo_id:
        where_conditions.append("r.id = %s")
        params.append(reclamo_id)
    
    if numero_documento:
        where_conditions.append("r.n_documento = %s")
        params.append(numero_documento)
    
    if not where_conditions:
        return None
    
    where_clause = " AND ".join(where_conditions)
    
    sql = f"""
    SELECT 
        r.id,
        r.nombres_razon,
        r.direccion,
        r.correo,
        r.telefono,
        r.n_documento,
        r.monto_indemnizado,
        r.bien_contratado,
        r.monto_reclamado,
        r.relacion,
        r.fecha_recepcion,
        r.descripcion,
        r.detalles,
        r.pedido,
        r.foto,
        r.paquetetracking as tracking_paquete,
        s.direccion as sucursal_direccion,
        td.siglas as tipo_documento_siglas,
        tr.nombre as tipo_reclamo_nombre,
        mr.nombre as motivo_nombre,
        cr.nombre as causa_nombre,
        ti.nombre as tipo_indemnizacion_nombre
    FROM reclamo r
    LEFT JOIN sucursal s ON r.sucursal_id = s.id
    LEFT JOIN tipo_documento td ON r.tipo_documentoid = td.id
    LEFT JOIN causa_reclamo cr ON r.causa_reclamoid = cr.id
    LEFT JOIN motivo_reclamo mr ON cr.motivo_reclamoid = mr.id
    LEFT JOIN tipo_reclamo tr ON mr.tipo_reclamoid = tr.id
    LEFT JOIN tipo_indemnizacion ti ON r.tipo_indemnizacionid = ti.id
    WHERE {where_clause}
    ORDER BY r.fecha_recepcion DESC
    LIMIT 1
    """
    
    return sql_select_fetchone(sql, params)

def obtener_estados_reclamo():
    """
    Obtiene todos los estados posibles de un reclamo
    """
    sql = """
    SELECT 
        id,
        nombre
    FROM estado_reclamo
    WHERE activo = 1
    ORDER BY id ASC
    """
    
    return sql_select_fetchall(sql)

def obtener_detalles_reclamo():
    """
    Obtiene todos los detalles de reclamo activos
    """
    sql = """
    SELECT 
        id,
        nombre,
        descripcion,
        estado_reclamoid
    FROM detalle_reclamo
    WHERE activo = 1
    ORDER BY estado_reclamoid, nombre
    """
    
    return sql_select_fetchall(sql)

def obtener_detalles_reclamo_por_estado(estado_id):
    """
    Obtiene los detalles de reclamo disponibles para un estado específico
    """
    sql = """
    SELECT 
        id,
        nombre,
        descripcion
    FROM detalle_reclamo
    WHERE estado_reclamoid = %s
    AND activo = 1
    ORDER BY nombre ASC
    """
    
    return sql_select_fetchall(sql, (estado_id,))

def obtener_reclamos_admin(limit=50, offset=0):
    """
    Obtiene reclamos para la vista administrativa con información del último estado
    """
    sql = """
    SELECT 
        r.id,
        r.nombres_razon,
        r.correo,
        r.telefono,
        r.fecha_recepcion,
        r.descripcion,
        r.foto,
        COALESCE(ultimo_seguimiento.ultimo_estado_id, NULL) as ultimo_estado_id,
        COALESCE(ultimo_seguimiento.ultimo_estado_nombre, 'Sin seguimiento') as ultimo_estado_nombre
    FROM reclamo r
    LEFT JOIN (
        SELECT 
            sr.reclamoid,
            dr.estado_reclamoid as ultimo_estado_id,
            er.nombre as ultimo_estado_nombre,
            ROW_NUMBER() OVER (PARTITION BY sr.reclamoid ORDER BY sr.fecha DESC, sr.hora DESC) as rn
        FROM seguimiento_reclamo sr
        INNER JOIN detalle_reclamo dr ON sr.detalle_reclamoid = dr.id
        INNER JOIN estado_reclamo er ON dr.estado_reclamoid = er.id
    ) ultimo_seguimiento ON r.id = ultimo_seguimiento.reclamoid AND ultimo_seguimiento.rn = 1
    ORDER BY r.fecha_recepcion DESC
    LIMIT %s OFFSET %s
    """
    
    return sql_select_fetchall(sql, (limit, offset))

def buscar_reclamos_con_filtros(texto_busqueda='', estado_filtro='', limit=50, offset=0):
    """
    Busca reclamos con filtros de texto y estado
    """
    where_conditions = []
    params = []
    
    if texto_busqueda:
        where_conditions.append("(r.nombres_razon LIKE %s OR r.correo LIKE %s OR r.id LIKE %s)")
        texto_param = f"%{texto_busqueda}%"
        params.extend([texto_param, texto_param, texto_param])
    
    if estado_filtro:
        where_conditions.append("ultimo_seguimiento.ultimo_estado_id = %s")
        params.append(estado_filtro)
    
    where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
    
    sql = f"""
    SELECT 
        r.id,
        r.nombres_razon,
        r.correo,
        r.telefono,
        r.fecha_recepcion,
        r.descripcion,
        r.foto,
        COALESCE(ultimo_seguimiento.ultimo_estado_id, NULL) as ultimo_estado_id,
        COALESCE(ultimo_seguimiento.ultimo_estado_nombre, 'Sin seguimiento') as ultimo_estado_nombre
    FROM reclamo r
    LEFT JOIN (
        SELECT 
            sr.reclamoid,
            dr.estado_reclamoid as ultimo_estado_id,
            er.nombre as ultimo_estado_nombre,
            ROW_NUMBER() OVER (PARTITION BY sr.reclamoid ORDER BY sr.fecha DESC, sr.hora DESC) as rn
        FROM seguimiento_reclamo sr
        INNER JOIN detalle_reclamo dr ON sr.detalle_reclamoid = dr.id
        INNER JOIN estado_reclamo er ON dr.estado_reclamoid = er.id
    ) ultimo_seguimiento ON r.id = ultimo_seguimiento.reclamoid AND ultimo_seguimiento.rn = 1
    WHERE {where_clause}
    ORDER BY r.fecha_recepcion DESC
    LIMIT %s OFFSET %s
    """
    
    params.extend([limit, offset])
    return sql_select_fetchall(sql, params)

def obtener_seguimientos_reclamo(reclamo_id):
    """
    Obtiene todos los seguimientos de un reclamo con sus detalles
    """
    sql = """
    SELECT 
        sr.reclamoid,
        sr.detalle_reclamoid,
        sr.fecha,
        sr.hora,
        sr.comentario,
        dr.nombre as detalle_nombre,
        dr.descripcion as detalle_descripcion,
        dr.estado_reclamoid,
        er.nombre as estado_nombre
    FROM seguimiento_reclamo sr
    INNER JOIN detalle_reclamo dr ON sr.detalle_reclamoid = dr.id
    INNER JOIN estado_reclamo er ON dr.estado_reclamoid = er.id
    WHERE sr.reclamoid = %s
    ORDER BY sr.fecha ASC, sr.hora ASC
    """
    
    return sql_select_fetchall(sql, (reclamo_id,))

def obtener_ultimo_seguimiento_reclamo(reclamo_id):
    """
    Obtiene el último seguimiento de un reclamo
    """
    sql = """
    SELECT 
        sr.fecha,
        sr.hora,
        sr.comentario,
        dr.nombre as detalle_nombre,
        dr.descripcion as detalle_descripcion,
        er.nombre as estado_nombre
    FROM seguimiento_reclamo sr
    INNER JOIN detalle_reclamo dr ON sr.detalle_reclamoid = dr.id
    INNER JOIN estado_reclamo er ON dr.estado_reclamoid = er.id
    WHERE sr.reclamoid = %s
    ORDER BY sr.fecha DESC, sr.hora DESC
    LIMIT 1
    """
    
    return sql_select_fetchone(sql, (reclamo_id,))

def obtener_estados_usados_reclamo(reclamo_id):
    """
    Obtiene los IDs de estados que han sido usados en un reclamo
    """
    sql = """
    SELECT DISTINCT dr.estado_reclamoid
    FROM seguimiento_reclamo sr
    INNER JOIN detalle_reclamo dr ON sr.detalle_reclamoid = dr.id
    WHERE sr.reclamoid = %s
    """
    
    result = sql_select_fetchall(sql, (reclamo_id,))
    return [r['estado_reclamoid'] for r in result]

def agrupar_seguimientos_por_estado(seguimientos):
    """
    Agrupa los seguimientos por estado para mostrar en el timeline
    """
    seguimientos_por_estado = defaultdict(list)
    for seg in seguimientos:
        seguimientos_por_estado[seg['estado_reclamoid']].append(seg)
    return seguimientos_por_estado

def obtener_historial_reclamo(reclamo_id):
    """
    Obtiene el historial completo de seguimiento de un reclamo
    """
    sql = """
    SELECT 
        sr.reclamoid,
        sr.detalle_reclamoid,
        sr.fecha,
        sr.hora,
        sr.comentario,
        dr.nombre as detalle_nombre,
        dr.descripcion as detalle_descripcion,
        CONCAT(sr.fecha, ' ', sr.hora) as fecha_completa
    FROM seguimiento_reclamo sr
    INNER JOIN detalle_reclamo dr ON sr.detalle_reclamoid = dr.id
    WHERE sr.reclamoid = %s
    ORDER BY sr.fecha DESC, sr.hora DESC
    """
    
    return sql_select_fetchall(sql, (reclamo_id,))

def agregar_seguimiento_reclamo(reclamo_id, detalle_reclamo_id, comentario=None):
    """
    Agrega un nuevo seguimiento a un reclamo
    """
    try:
        ahora = datetime.now()
        fecha_actual = ahora.date()
        hora_actual = ahora.time()
        
        sql = """
        INSERT INTO seguimiento_reclamo (reclamoid, detalle_reclamoid, fecha, hora, comentario)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        sql_execute(sql, (reclamo_id, detalle_reclamo_id, fecha_actual, hora_actual, comentario))
        
        return {
            'success': True,
            'message': 'Seguimiento agregado exitosamente'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error al agregar seguimiento: {str(e)}'
        }

def procesar_respuesta_reclamo(reclamo_id, detalle_reclamo_id, observaciones=None):
    """
    Procesa la respuesta a un reclamo agregando un seguimiento
    """
    try:
        # Verificar que el reclamo existe
        reclamo = buscar_reclamo_por_id_o_documento(reclamo_id=reclamo_id)
        if not reclamo:
            return {
                'success': False,
                'message': 'Reclamo no encontrado'
            }
        
        # Verificar que el detalle existe
        detalle = sql_select_fetchone(
            "SELECT id, nombre FROM detalle_reclamo WHERE id = %s AND activo = 1",
            (detalle_reclamo_id,)
        )
        if not detalle:
            return {
                'success': False,
                'message': 'Tipo de respuesta no válido'
            }
        
        # Agregar el seguimiento
        resultado = agregar_seguimiento_reclamo(reclamo_id, detalle_reclamo_id, observaciones)
        
        if resultado['success']:
            # Aquí podrías agregar lógica para enviar notificaciones por correo
            return {
                'success': True,
                'message': f'Respuesta enviada exitosamente al reclamo #{reclamo_id}'
            }
        else:
            return resultado
            
    except Exception as e:
        return {
            'success': False,
            'message': f'Error al procesar respuesta: {str(e)}'
        }

def validar_tracking_existe(tracking):
    """
    Valida si un tracking existe en el sistema de paquetes
    """
    sql = """
    SELECT 
        tracking,
        CONCAT(nombres_contacto_destinatario, ' ', apellidos_razon_destinatario) as destinatario_completo
    FROM paquete
    WHERE tracking = %s
    LIMIT 1
    """
    
    return sql_select_fetchone(sql, (tracking,))

def obtener_reclamos_por_estado_activo(estado_id, limit=50):
    """
    Obtiene reclamos que están actualmente en un estado específico
    """
    sql = """
    SELECT DISTINCT
        r.id,
        r.nombres_razon,
        r.n_documento,
        r.fecha_recepcion,
        r.monto_reclamado
    FROM reclamo r
    INNER JOIN seguimiento_reclamo sr ON r.id = sr.reclamoid
    INNER JOIN detalle_reclamo dr ON sr.detalle_reclamoid = dr.id
    WHERE dr.estado_reclamoid = %s
    AND sr.fecha = (
        SELECT MAX(sr2.fecha) 
        FROM seguimiento_reclamo sr2 
        INNER JOIN detalle_reclamo dr2 ON sr2.detalle_reclamoid = dr2.id
        WHERE sr2.reclamoid = r.id
    )
    ORDER BY r.fecha_recepcion DESC
    LIMIT %s
    """
    
    return sql_select_fetchall(sql, (estado_id, limit))

def obtener_tipos_reclamo():
    """
    Obtiene todos los tipos de reclamo disponibles
    """
    sql = """
    SELECT 
        id,
        nombre,
        descripcion
    FROM tipo_reclamo
    WHERE activo = 1
    ORDER BY nombre ASC
    """
    
    return sql_select_fetchall(sql)

def obtener_motivos_por_tipo_reclamo(tipo_reclamo_id):
    """
    Obtiene los motivos disponibles para un tipo de reclamo específico
    """
    sql = """
    SELECT 
        id,
        nombre,
        descripcion
    FROM motivo_reclamo
    WHERE tipo_reclamoid = %s
    ORDER BY nombre ASC
    """
    
    return sql_select_fetchall(sql, (tipo_reclamo_id,))

def obtener_causas_por_motivo_reclamo(motivo_reclamo_id):
    """
    Obtiene las causas disponibles para un motivo de reclamo específico
    """
    sql = """
    SELECT 
        id,
        nombre,
        descripcion
    FROM causa_reclamo
    WHERE motivo_reclamoid = %s
    ORDER BY nombre ASC
    """
    
    return sql_select_fetchall(sql, (motivo_reclamo_id,))

def obtener_estadisticas_reclamos():
    """
    Obtiene estadísticas generales de los reclamos
    """
    sql = """
    SELECT 
        COUNT(*) as total_reclamos,
        COUNT(CASE WHEN MONTH(fecha_recepcion) = MONTH(CURRENT_DATE) THEN 1 END) as reclamos_mes_actual,
        AVG(monto_reclamado) as promedio_monto_reclamado
    FROM reclamo
    """
    
    estadisticas_basicas = sql_select_fetchone(sql)
    
    # Estadísticas por estado
    sql_estados = """
    SELECT 
        er.nombre as estado_nombre,
        COUNT(DISTINCT r.id) as cantidad
    FROM reclamo r
    LEFT JOIN seguimiento_reclamo sr ON r.id = sr.reclamoid
    LEFT JOIN detalle_reclamo dr ON sr.detalle_reclamoid = dr.id
    LEFT JOIN estado_reclamo er ON dr.estado_reclamoid = er.id
    GROUP BY er.id, er.nombre
    ORDER BY cantidad DESC
    """
    
    estadisticas_estados = sql_select_fetchall(sql_estados)
    
    return {
        'basicas': estadisticas_basicas,
        'por_estado': estadisticas_estados
    }

def eliminar_ultimo_seguimiento(reclamoid):
    try:
        sql = """
            SELECT * FROM seguimiento_reclamo
            WHERE reclamoid = %s
            ORDER BY fecha DESC, hora DESC
            LIMIT 1
        """
        ultimo = sql_select_fetchone(sql, (reclamoid,))
        if not ultimo:
            return {'success': False, 'message': "No se encontró seguimiento para este reclamo."}

        # Eliminar usando clave compuesta
        sql_delete = """
            DELETE FROM seguimiento_reclamo
            WHERE reclamoid = %s AND detalle_reclamoid = %s AND fecha = %s AND hora = %s
        """
        sql_execute(sql_delete, (
            ultimo['reclamoid'],
            ultimo['detalle_reclamoid'],
            ultimo['fecha'],
            ultimo['hora']
        ))

        return {'success': True}
    
    except Exception as e:
        print("Error al eliminar seguimiento:", e)
        return {'success': False, 'message': "Error interno al eliminar seguimiento."}
