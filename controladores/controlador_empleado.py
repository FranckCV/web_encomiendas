from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'empleado'

def get_info_columns():
    return show_columns(table_name)

def get_primary_key():
    return show_primary_key(table_name)

def exists_Activo():
    return exists_column_Activo(table_name)

def delete_row(id):
    bd.delete_row_table(table_name, id)

#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql = f'''
        SELECT 
            e.id,
            e.nombre,
            e.apellidos,
            e.correo,
            e.rolid,
            r.nombre AS nom_rol
        FROM {table_name} e
        LEFT JOIN rol r ON e.rolid = r.id
    '''
    resultados = sql_select_fetchall(sql)
    return resultados

def get_table():
    sql = f'''
        SELECT 
            e.id,
            e.nombre,
            e.apellidos,
            e.correo,
            e.rolid,
            r.nombre AS nom_rol
        FROM {table_name} e
        INNER JOIN rol r ON e.rolid = r.id
    '''
    columnas = {
        'id': ['Usuario ID', 1],
        'nombre': ['Nombre', 1.5],
        'apellidos': ['Apellidos', 1.5],
        'correo': ['Correo', 1.5],
        'nom_rol': ['Rol', 1.5],
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas

######_ CAMBIAR PARAMETROS Y SQL INTERNO _###### 

def unactive_row(id):
    unactive_row_table(table_name, id)

def insert_row(nombre, apellidos, correo, rolid):
    sql = f'''
        INSERT INTO 
            {table_name} (nombre, apellidos, correo, rolid)
        VALUES 
            (%s, %s, %s, %s)
    '''
    sql_execute(sql, (nombre, apellidos, correo, rolid))

def update_row(id, nombre, apellidos, correo, rolid):
    sql = f'''
        UPDATE {table_name} SET 
            nombre = %s,
            apellidos = %s,
            correo = %s,
            rolid = %s
        WHERE id = {id}
    '''
    sql_execute(sql, (nombre, apellidos, correo, rolid))

#####_ ADICIONALES _#####

def get_options_empleado():
    sql = f'''
        SELECT 
            id,
            CONCAT(nombre, ' ', apellidos) AS nombre_completo
        FROM {table_name}
        ORDER BY nombre ASC
    '''
    filas = sql_select_fetchall(sql)
    lista = [(fila["id"], fila["nombre_completo"]) for fila in filas]
    return lista


def get_report_test():
    sql = f'''
        SELECT 
            emp.id,
            emp.nombre,
            emp.apellidos,
            emp.correo,
            rol.id AS rol_id,
            rol.nombre AS nombre_rol
        FROM {table_name} emp
        INNER JOIN rol ON emp.rolid = rol.id
    '''
    
    columnas = {
        'id'   : ['ID', 0.5],
        'nombre'      : ['Nombre', 1.5],
        'apellidos'   : ['Apellidos', 1.5],
        'correo'      : ['Correo Electrónico', 2],
        'nombre_rol'  : ['Rol', 1.5],
    }
    
    filas = sql_select_fetchall(sql)
    
    return columnas, filas

