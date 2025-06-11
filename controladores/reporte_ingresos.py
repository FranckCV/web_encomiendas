from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd

def get_ingresos_diarios():
    sql = f'''
        SELECT *
        FROM (
            SELECT 
                COALESCE(v.fecha, e.fecha) AS fecha,
                IFNULL(SUM(v.monto_total), 0) AS ingresos_venta,
                IFNULL(SUM(e.monto_total), 0) AS ingresos_encomienda,
                IFNULL(SUM(v.monto_total), 0) + IFNULL(SUM(e.monto_total), 0) AS ingresos_totales
            FROM (
                SELECT fecha, monto_total FROM transaccion_venta
                UNION ALL
                SELECT NULL AS fecha, NULL AS monto_total
            ) v
            LEFT JOIN (
                SELECT fecha, monto_total FROM transaccion_encomienda
                UNION ALL
                SELECT NULL AS fecha, NULL AS monto_total
            ) e ON v.fecha = e.fecha
            GROUP BY COALESCE(v.fecha, e.fecha)

            UNION

            SELECT 
                e.fecha,
                0 AS ingresos_venta,
                SUM(e.monto_total) AS ingresos_encomienda,
                SUM(e.monto_total) AS ingresos_totales
            FROM transaccion_encomienda e
            LEFT JOIN transaccion_venta v ON v.fecha = e.fecha
            WHERE v.fecha IS NULL
            GROUP BY e.fecha
        ) sub
        WHERE fecha IS NOT NULL
        ORDER BY fecha;
    '''
    
    columnas = {
        'fecha'               : ['Fecha', 1.5],
        'ingresos_venta'      : ['Ingresos por ventas', 1.5],
        'ingresos_encomienda' : ['Ingresos por envíos', 1.5],
        'ingresos_totales'    : ['Total diario', 1.5],
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas


def get_ingresos_por_sucursal():
    sql = f'''
        SELECT 
            s.id AS sucursal_id,
            s.abreviatura,
            te.fecha,
            SUM(te.monto_total) AS ingresos_totales
        FROM transaccion_encomienda te
        INNER JOIN paquete p ON te.num_serie = p.transaccion_encomienda_num_serie
        INNER JOIN salida sa ON p.salidaid = sa.id
        INNER JOIN escala e ON sa.id = e.salidaid
        INNER JOIN sucursal s ON e.sucursalid = s.id
        GROUP BY s.id, te.fecha
        ORDER BY ingresos_totales DESC;
    '''

    columnas = {
        'sucursal_id'     : ['ID Sucursal', 1],
        'abreviatura'     : ['Sucursal', 1.5],
        'fecha'           : ['Fecha', 1.5],
        'ingresos_totales': ['Ingresos Totales', 1.5],
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas
