from controladores.bd import sql_execute, sql_select_fetchone, sql_select_fetchall
from datetime import datetime
from collections import defaultdict

# Función para buscar reclamo por ID o documento
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

# Función para obtener estados de reclamo
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

# Función para obtener seguimientos de un reclamo
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

# Función para obtener el último seguimiento de un reclamo
def obtener_ultimo_seguimiento_reclamo(reclamo_id):
    """
    Obtiene el último seguimiento de un reclamo
    """
    sql = """
    SELECT 
        sr.fecha,
        sr.hora,
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

# Función para obtener estados usados en un reclamo
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

# Función para agrupar seguimientos por estado
def agrupar_seguimientos_por_estado(seguimientos):
    """
    Agrupa los seguimientos por estado para mostrar en el timeline
    """
    seguimientos_por_estado = defaultdict(list)
    for seg in seguimientos:
        seguimientos_por_estado[seg['estado_reclamoid']].append(seg)
    return seguimientos_por_estado

# Función para agregar seguimiento a un reclamo
def agregar_seguimiento_reclamo(reclamo_id, detalle_reclamo_id):
    """
    Agrega un nuevo seguimiento a un reclamo existente
    """
    try:
        ahora = datetime.now()
        fecha_actual = ahora.date()
        hora_actual = ahora.time()
        
        sql = """
        INSERT INTO seguimiento_reclamo (reclamoid, detalle_reclamoid, fecha, hora)
        VALUES (%s, %s, %s, %s)
        """
        
        sql_execute(sql, (reclamo_id, detalle_reclamo_id, fecha_actual, hora_actual))
        
        return {
            'success': True,
            'message': 'Seguimiento agregado exitosamente'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error al agregar seguimiento: {str(e)}'
        }

# Función para obtener detalles de reclamo por estado
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

# Función para obtener todos los reclamos (para administración)
def obtener_todos_los_reclamos(limit=50):
    """
    Obtiene todos los reclamos para vista administrativa
    """
    sql = """
    SELECT 
        r.id,
        r.nombres_razon,
        r.n_documento,
        r.fecha_recepcion,
        r.monto_reclamado,
        s.direccion as sucursal,
        tr.nombre as tipo_reclamo
    FROM reclamo r
    LEFT JOIN sucursal s ON r.sucursal_id = s.id
    LEFT JOIN causa_reclamo cr ON r.causa_reclamoid = cr.id
    LEFT JOIN motivo_reclamo mr ON cr.motivo_reclamoid = mr.id
    LEFT JOIN tipo_reclamo tr ON mr.tipo_reclamoid = tr.id
    ORDER BY r.fecha_recepcion DESC
    LIMIT %s
    """
    
    return sql_select_fetchall(sql, (limit,))

# Función para validar si un tracking de paquete existe
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

# Función para obtener reclamos por estado
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

# Función para obtener tipos de reclamo disponibles
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

# Función para obtener motivos de reclamo por tipo
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

# Función para obtener causas por motivo de reclamo
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