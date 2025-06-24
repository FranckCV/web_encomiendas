from controladores.bd import sql_select_fetchall

def get_reporte_reclamos_tipo_causa_periodo():
    print(">>> ENTRANDO AL REPORTE DE RECLAMOS POR TIPO, CAUSA Y PERIODO <<<")

    columnas = {
        'tipo_reclamo': ['Tipo de Reclamo', 2],
        'causa_reclamo': ['Causa de Reclamo', 2],
        'cantidad_reclamos': ['Cantidad', 1]
    }

    sql = '''
        SELECT 
            tr.nombre AS tipo_reclamo,
            cr.nombre AS causa_reclamo,
            COUNT(r.id) AS cantidad_reclamos
        FROM reclamo r
        JOIN causa_reclamo cr ON r.causa_reclamoid = cr.id
        JOIN motivo_reclamo mr ON cr.motivo_reclamoid = mr.id
        JOIN tipo_reclamo tr ON mr.tipo_reclamoid = tr.id
        GROUP BY tr.nombre, cr.nombre
        ORDER BY tr.nombre, cr.nombre;
    '''

    try:
        filas = sql_select_fetchall(sql)
        return columnas, filas
    except Exception as e:
        print(f"ERROR en el reporte de reclamos por tipo, causa y periodo: {e}")
        return columnas, []
