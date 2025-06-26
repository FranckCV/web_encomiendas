from controladores.bd import sql_select_fetchall

def get_reporte_encomiendas_por_tipo():
    sql = '''
        SELECT 
            te.num_serie AS transaccion_id,
            te.fecha,
            te.hora,
            te.descripcion,
            te.monto_total,
            te.recojo_casa,
            c.nombre_siglas AS cliente,
            td.nombre AS tipo_documento,
            so.direccion AS direccion_sucursal_origen,
            COUNT(p.tracking) AS cantidad_paquetes,
            GROUP_CONCAT(DISTINCT e.nombre SEPARATOR ', ') AS tipos_empaque,
            te.masivo
        FROM transaccion_encomienda te
        JOIN cliente c ON c.id = te.clienteid
        JOIN tipo_documento td ON td.id = c.tipo_documentoid
        JOIN sucursal so ON so.id = te.id_sucursal_origen
        LEFT JOIN paquete p ON p.transaccion_encomienda_num_serie = te.num_serie
        LEFT JOIN tipo_empaque e ON e.id = p.tipo_empaqueid
        GROUP BY te.num_serie
        ORDER BY te.fecha DESC, te.hora DESC;
    '''

    columnas = {
    'transaccion_id': ['N° Transacción', 1.2],
    'fecha': ['Fecha', 1],
    'hora': ['Hora', 1],
    'descripcion': ['Descripción', 2],
    'monto_total': ['Monto Total', 1.2],
    # 'recojo_casa': ['Recojo en Casa', 1.2],
    'cliente': ['Cliente', 2],
    'tipo_documento': ['Tipo Documento', 1.5],
    # 'tipo_comprobante': ['Tipo Comprobante', 1.5],
    'direccion_sucursal_origen': ['Dirección Sucursal Origen', 2],
    'cantidad_paquetes': ['# Paquetes', 1.2],
    'tipos_empaque': ['Tipo(s) de Empaque', 2],
    'masivo': ['¿Masivo?', 1]
}
    filas = sql_select_fetchall(sql)
    print(">>> Generando Reporte de Encomiendas por Tipo <<<")
    return columnas, filas
