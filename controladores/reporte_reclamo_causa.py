from controladores.bd import sql_select_fetchall

def get_reporte_reclamos_tipo_causa_periodo():
    sql = '''
        SELECT 
            tr.nombre AS tipo_reclamo,
            mr.nombre AS motivo_reclamo,
            cr.nombre AS causa_reclamo,
            DATE_FORMAT(r.fecha_recojo, '%Y-%m') AS periodo,
            COUNT(*) AS cantidad_reclamos
        FROM reclamo r
        INNER JOIN causa_reclamo cr ON r.causa_reclamoid = cr.id
        INNER JOIN motivo_reclamo mr ON cr.motivo_reclamoid = mr.id
        INNER JOIN tipo_reclamo tr ON mr.tipo_reclamoid = tr.id
        GROUP BY tr.nombre, mr.nombre, cr.nombre, DATE_FORMAT(r.fecha_recojo, '%Y-%m')
        ORDER BY periodo DESC, cantidad_reclamos DESC;
    '''

    columnas = {
        'tipo_reclamo'      : ['Tipo de Reclamo', 1.5],
        'motivo_reclamo'    : ['Motivo', 1.5],
        'causa_reclamo'     : ['Causa', 2],
        'periodo'           : ['Periodo', 1],
        'cantidad_reclamos' : ['Cantidad', 1]
    }

    filas = sql_select_fetchall(sql)
    print(">>> ENTRANDO AL REPORTE DE RECLAMOS POR TIPO, CAUSA Y PERIODO <<<")
    return columnas, filas
