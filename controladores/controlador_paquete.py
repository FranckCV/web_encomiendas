from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####


def get_report_test():
    sql = f'''
        SELECT 
            paq.*, con.nombre AS con_nombre, est.nombre AS estado_nombre, 
            DATE_FORMAT(tra.fecha, '%d/%m/%Y') AS fecha_txt 
        FROM paquete paq 
        LEFT JOIN transaccion_encomienda tra 
        ON tra.num_serie = paq.transaccion_encomienda_num_serie 
        INNER JOIN contenido_paquete con ON con.id = paq.contenido_paqueteid 
        INNER JOIN ( SELECT paquetetracking, MAX(detalle_estadoid) AS max_detalle_estadoid FROM seguimiento GROUP BY paquetetracking ) ult_seg ON ult_seg.paquetetracking = paq.tracking INNER JOIN detalle_estado det ON det.id = ult_seg.max_detalle_estadoid INNER JOIN estado_encomienda est ON est.id = det.estado_encomiendaid
        ;

    '''
    
    columnas = {
        'tracking'            : ['Tracking', 0.5],
        'con_nombre' : ['Contenido de paquete', 1.5],
        'estado_nombre' : ['Estado Actual de paquete', 1.5],
        'fecha_txt'           : ['Fecha de envio', 2],
    }
    
    filas = sql_select_fetchall(sql)
    
    return columnas, filas
