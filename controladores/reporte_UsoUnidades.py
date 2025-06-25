from controladores.bd import sql_select_fetchall


from controladores.bd import sql_select_fetchall

def get_reporte_uso_unidades():
    sql = '''
        SELECT 
            u.id AS unidadid,
            u.placa,
            m.nombre AS modelo,
            ma.nombre AS marca,
            CASE u.estado
                WHEN 'A' THEN 'Activo'
                WHEN 'I' THEN 'Inactivo'
                WHEN 'M' THEN 'Mantenimiento'
                ELSE 'Desconocido'
            END AS estado_legible,
            u.descripcion,
            COUNT(s.id) AS cantidad_salidas,
            MIN(s.fecha) AS primera_salida,
            MAX(s.fecha) AS ultima_salida
        FROM unidad u
        LEFT JOIN salida s ON s.unidadid = u.id
        LEFT JOIN modelo m ON m.id = u.modeloid
        LEFT JOIN marca ma ON ma.id = m.marcaid
        GROUP BY u.id, u.placa, m.nombre, ma.nombre, estado_legible, u.descripcion
        ORDER BY cantidad_salidas DESC;
    '''

    columnas = {
        'unidadid': ['ID Unidad', 1],
        'placa': ['Placa', 1.5],
        'modelo': ['Modelo', 1.5],
        'marca': ['Marca', 1.5],
        'estado_legible': ['Estado', 1.2],  # <- estado con nombre legible
        'descripcion': ['Descripción', 2],
        'cantidad_salidas': ['Cantidad de Salidas', 1.2],
        'primera_salida': ['Primera Salida', 1.2],
        'ultima_salida': ['Última Salida', 1.2],
    }

    filas = sql_select_fetchall(sql)
    print(">>> ENTRANDO AL REPORTE COMPLETO DE USO DE UNIDADES (estado legible) <<<")
    return columnas, filas
