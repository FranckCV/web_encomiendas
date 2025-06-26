from controladores.bd import sql_select_fetchall

def get_reporte_viajes_por_unidad():
    sql = '''
        SELECT 
            s.unidadid,
            u.placa AS nombre_unidad,
            COUNT(*) AS cantidad_viajes,
            MIN(s.fecha) AS primer_viaje,
            MAX(s.fecha) AS ultimo_viaje
        FROM salida s
        JOIN unidad u ON s.unidadid = u.id
        GROUP BY s.unidadid, u.placa
        ORDER BY cantidad_viajes DESC;
    '''

    columnas = {
        'unidadid'       : ['ID Unidad', 1],
        'nombre_unidad'  : ['Placa de Unidad', 2],
        'cantidad_viajes': ['Cantidad de Viajes', 1.5],
        'primer_viaje'   : ['Primer Viaje', 1.5],
        'ultimo_viaje'   : ['Último Viaje', 1.5],
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas
