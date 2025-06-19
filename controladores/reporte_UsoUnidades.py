from controladores.bd import sql_select_fetchall

def get_reporte_uso_unidades():
    sql = '''
        SELECT 
            s.unidadid,
            COUNT(*) AS cantidad_usos,
            MIN(s.fecha) AS primera_salida,
            MAX(s.fecha) AS ultima_salida
        FROM salida s
        GROUP BY s.unidadid
        ORDER BY cantidad_usos DESC;
    '''

    columnas = {
        'unidadid'       : ['ID Unidad', 1],
        'cantidad_usos'  : ['Cantidad de Usos', 1.5],
        'primera_salida' : ['Primera Salida', 1.5],
        'ultima_salida'  : ['Última Salida', 1.5],
    }

    filas = sql_select_fetchall(sql)
    print(">>> ENTRANDO AL REPORTE DE VIAJES POR UNIDAD <<<")

    return columnas, filas
