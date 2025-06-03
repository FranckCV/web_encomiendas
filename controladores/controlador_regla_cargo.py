from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
####################################################
def get_condiciones_tarifa():
    sql = '''
        SELECT tipo_condicion, inferior, superior, porcentaje
        FROM regla_cargo
    '''
    return sql_select_fetchall(sql)
