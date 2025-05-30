from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####


def get_report_test():
    sql = f'''
        SELECT 
        * ,
        DATE_FORMAT(tra.fecha, '%d/%m/%Y') AS fecha_txt
        FROM paquete paq 
        left join transaccion_encomienda tra on tra.num_serie = paq.transaccion_encomienda_num_serie;

    '''
    
    columnas = {
        'tracking'            : ['Tracking', 0.5],
        'codigo_postal'       : ['Nombre', 1.5],
        'contenido_paqueteid' : ['Contenido de paquete', 1.5],
        'fecha_txt'           : ['Fecha', 2],
    }
    
    filas = sql_select_fetchall(sql)
    
    return columnas, filas
