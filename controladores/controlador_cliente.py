from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'cliente'

def get_info_columns():
    return show_columns(table_name)

def get_primary_key():
    return show_primary_key(table_name)

def exists_Activo():
    return exists_column_Activo(table_name)

def delete_row(id):
    sql = f'''
        DELETE FROM {table_name}
        WHERE id = {id}
    '''
    sql_execute(sql)

#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql = f'''
        SELECT 
            cl.*, 
            td.nombre AS nom_tipodoc,
            tc.nombre AS nom_tipocliente
        FROM {table_name} cl
        LEFT JOIN tipo_documento td ON cl.tipo_documentoid = td.id
        LEFT JOIN tipo_cliente tc ON cl.tipo_clienteid = tc.id
    '''
    resultados = sql_select_fetchall(sql)
    return resultados

def get_table():
    sql = f'''
        SELECT 
            cl.id,
            cl.nombre_siglas,
            cl.apellidos_razon,
            cl.correo,
            cl.telefono,
            cl.num_documento,
            td.nombre AS nom_tipodoc,
            tc.nombre AS nom_tipocliente
        FROM {table_name} cl
        INNER JOIN tipo_documento td ON cl.tipo_documentoid = td.id
        INNER JOIN tipo_cliente tc ON cl.tipo_clienteid = tc.id
    '''
    
    columnas = {
        'id': ['ID', 0.5],
        'nombre_siglas': ['Nombre o siglas', 1.5],
        'apellidos_razon': ['Apellidos o razón social', 1.5],
        'correo': ['Correo', 1.5],
        'telefono': ['Teléfono', 1],
        'num_documento': ['N° Documento', 1],
        'nom_tipodoc': ['Tipo Doc.', 1],
        'nom_tipocliente': ['Tipo Cliente', 1]
    }
    
    filas = sql_select_fetchall(sql)
    return columnas, filas

#####_ CAMBIAR PARAMETROS Y SQL INTERNO _#####

def unactive_row(id):
    unactive_row_table(table_name, id)

def insert_row(correo, telefono, num_documento, nombre_siglas, apellidos_razon, tipo_documentoid, tipo_clienteid):
    sql = f'''
        INSERT INTO {table_name} (
            correo, telefono, num_documento,
            nombre_siglas, apellidos_razon,
            tipo_documentoid, tipo_clienteid
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    sql_execute(sql, (correo, telefono, num_documento, nombre_siglas, apellidos_razon, tipo_documentoid, tipo_clienteid))

def update_row(id, correo, telefono, num_documento, nombre_siglas, apellidos_razon, tipo_documentoid, tipo_clienteid):
    sql = f'''
        UPDATE {table_name} SET 
            correo = %s,
            telefono = %s,
            num_documento = %s,
            nombre_siglas = %s,
            apellidos_razon = %s,
            tipo_documentoid = %s,
            tipo_clienteid = %s
        WHERE id = {id}
    '''
    sql_execute(sql, (correo, telefono, num_documento, nombre_siglas, apellidos_razon, tipo_documentoid, tipo_clienteid))

#####_ ADICIONALES _#####

def get_report_test():
    sql = f'''
        SELECT 
            cl.id,
            cl.nombre_siglas,
            cl.apellidos_razon,
            cl.correo,
            cl.num_documento,
            cl.telefono,
            td.nombre AS nom_tipodoc,
            tc.nombre AS nom_tipocliente
        FROM {table_name} cl
        INNER JOIN tipo_documento td ON cl.tipo_documentoid = td.id
        INNER JOIN tipo_cliente tc ON cl.tipo_clienteid = tc.id
    '''
    
    columnas = {
        'id': ['ID', 0.5],
        'nombre_siglas': ['Nombre o siglas', 1.5],
        'apellidos_razon': ['Apellidos o razón social', 1.5],
        'correo': ['Correo', 1.5],
        'num_documento': ['Documento', 1],
        'telefono': ['Teléfono', 1],
        'nom_tipodoc': ['Tipo Doc.', 1],
        'nom_tipocliente': ['Tipo Cliente', 1]
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas


def get_reporte_ventas():
    sql = '''
        SELECT 
            tv.num_serie,
            DATE_FORMAT(tv.fecha, '%d/%m/%Y') AS fecha_txt,
            tv.fecha AS fecha,
            tv.hora,
            CONCAT(cl.nombre_siglas, ' ', cl.apellidos_razon) AS cliente,
            GROUP_CONCAT(art.nombre SEPARATOR ', ') AS articulos,
            tv.monto_total
        FROM transaccion_venta tv
        INNER JOIN cliente cl ON tv.clienteid = cl.id
        INNER JOIN detalle_venta dv ON tv.num_serie = dv.ventanum_serie AND tv.tipo_comprobanteid = dv.ventatipo_comprobanteid
        INNER JOIN articulo art ON dv.articuloid = art.id
        GROUP BY tv.num_serie, tv.fecha, tv.hora, cliente, tv.monto_total
        ORDER BY tv.fecha DESC, tv.hora DESC 
    '''
    
    columnas = {
        'num_serie'   : ['Serie', 0.7],
        'fecha_txt'   : ['Fecha', 1],
        'hora'        : ['Hora', 0.8],
        'cliente'     : ['Cliente', 1.8],
        'articulos'   : ['Artículos Comprados', 2],
        'monto_total' : ['Total Transacción', 1.2],
    }

    filas = sql_select_fetchall(sql)
    
    return columnas, filas

