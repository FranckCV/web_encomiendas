from controladores.bd import sql_select_fetchall

def get_reporte_encomiendas_rutas_estado():
    sql = '''
        -- (usa el SQL que te puse arriba)
    '''
    columnas = {
        'tracking': ['Tracking', 1],
        'fecha_salida': ['Fecha de Salida', 1.2],
        'origen': ['Origen', 2],
        'destino': ['Destino', 2],
        'cliente': ['Cliente', 2],
        'estado_encomienda': ['Estado Actual', 2],
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas
