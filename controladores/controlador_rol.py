from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'rol'

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


from flask import request
import controladores.controlador_usuario as controlador_usuario
def get_table():
    usuario = controlador_usuario.get_usuario_empleado_user_id(request.cookies.get('user_id'))
    validar_admin = '' if usuario['rolid'] == 1 else ' where r.id != 1 '
 
    sql = f'''
        SELECT 
            r.id,
            r.nombre,
            r.descripcion,
            r.activo,
            r.tipo_rolid,
            tr.nombre AS nom_tiporol
        FROM {table_name} r
        INNER JOIN tipo_rol tr ON r.tipo_rolid = tr.id
        {validar_admin}

    '''
    columnas = {
        'id': ['ID', 0.5],
        'nombre': ['Nombre del Rol', 3],
        'descripcion': ['Descripción', 2],
        'nom_tiporol': ['Tipo de Rol', 2],
        'activo': ['Activo', 0.5]
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas


def unactive_row(id):
    unactive_row_table(table_name, id)


def insert_row(nombre, descripcion, tipo_rolid):
    sql = f'''
        INSERT INTO {table_name} (nombre, descripcion, activo, tipo_rolid)
        VALUES (%s, %s, 1, %s)
    '''
    sql_execute(sql, (nombre, descripcion, tipo_rolid))

def update_row(id, nombre, descripcion, tipo_rolid):
    sql = f'''
        UPDATE {table_name}
        SET nombre = %s,
            descripcion = %s,
            tipo_rolid = %s
        WHERE id = {id}
    '''
    sql_execute(sql, (nombre, descripcion, tipo_rolid))



def get_options():
    usuario = controlador_usuario.get_usuario_empleado_user_id(request.cookies.get('user_id'))
    validar_admin = '' if usuario['rolid'] == 1 else ' and r.id != 1 '

    sql= f'''
        select 
            id ,
            nombre
        from rol r
        where r.activo = 1 {validar_admin}
        order by nombre asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila['id'], fila["nombre"]) for fila in filas]

    return lista