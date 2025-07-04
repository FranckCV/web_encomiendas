from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'detalle_reclamo'

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

def table_fetchall():
    sql = f'''
        SELECT 
            r.*, tr.nombre AS nom_tiporol
        FROM {table_name} r
        LEFT JOIN tipo_rol tr ON r.tipo_rolid = tr.id
    '''
    return sql_select_fetchall(sql)


def get_table():
    sql = f'''
        SELECT 
            det.* ,
            est.nombre as est_nom
        FROM {table_name} det
        INNER JOIN estado_reclamo est 
        ON est.id= det.estado_reclamoid
        order by 1
    '''
    columnas = {
        'id': ['ID', 0.5],
        'nombre': ['Nombre del detalle', 1.5],
        'descripcion': ['Descripción', 2],
        'est_nom': ['Estado de reclamo', 2],
        'activo': ['Activo', 0.5]
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas


def unactive_row(id):
    unactive_row_table(table_name, id)


def insert_row(nombre, descripcion, estado_reclamoid):
    sql = f'''
        INSERT INTO {table_name} (nombre, descripcion, activo, estado_reclamoid)
        VALUES (%s, %s, 1, %s)
    '''
    sql_execute(sql, (nombre, descripcion, estado_reclamoid))


def update_row(id, nombre, descripcion, estado_reclamoid):
    sql = f'''
        UPDATE {table_name}
        SET nombre = %s,
            descripcion = %s,
            estado_reclamoid = %s
        WHERE id = {id}
    '''
    sql_execute(sql, (nombre, descripcion, estado_reclamoid))


def get_options():
    sql = '''
        SELECT id, nombre
        FROM detalle_reclamo
        WHERE activo = 1
        ORDER BY nombre ASC
    '''
    filas = sql_select_fetchall(sql)
    return [(fila['id'], fila['nombre']) for fila in filas]


# def get_options():
#     sql= f'''
#         select 
#             id ,
#             nombre
#         from estado_reclamo
#         where activo = 1
#         order by nombre asc
#     '''
#     filas = sql_select_fetchall(sql)
    
#     lista = [(fila['id'], fila["nombre"]) for fila in filas]

#     return lista