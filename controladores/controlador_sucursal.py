from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'sucursal'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where id = {id}
    '''
    sql_execute(sql)


#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql= f'''
        select 
            *
        from {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    
    return resultados


def get_table():
    sql =f'''
            SELECT 
                s.id,
                s.direccion,
                CONCAT(u.distrito, "/", u.provincia, "/", u.departamento) AS ubigeo,
                s.ubigeocodigo,
                s.horario_l_v,
                s.horario_s_d,
                s.latitud,
                s.longitud,
                s.teléfono,
                s.referencia,
                s.activo
            FROM 
                {table_name} s
            INNER JOIN 
                ubigeo u ON u.codigo = s.ubigeocodigo;
            '''

    columnas = {
        'id': ['ID', 0.5],
        'direccion': ['Dirección', 2.5],
        # 'ubigeocodigo': ['Codigo', 2.5],
        'ubigeo': ['Ubigeo', 2.5], 
        'horario_l_v': ['Horario L-V', 2.5],
        'horario_s_d': ['Horario S-D', 2.5],
        # 'latitud': ['Latitud', 1],
        # 'longitud': ['Longitud', 1],
        'teléfono': ['Teléfono', 1.5],
        # 'referencia': ['Referencia', 2],
        'activo': ['Activo', 0.5]
    }

    filas = sql_select_fetchall(sql)
    return columnas,filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row(id):
    unactive_row_table("sucursal", id)


def insert_row(direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia):
    sql = f'''
        INSERT INTO {table_name} 
        (direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
    '''
    sql_execute(sql, (direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia))


def update_row(direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia, id):
    sql = f'''
        UPDATE sucursal SET 
            direccion = %s,
            ubigeocodigo = %s,
            horario_l_v = %s,
            horario_s_d = %s,
            latitud = %s,
            longitud = %s,
            teléfono = %s,
            referencia = %s,
        WHERE {get_primary_key()} = {id}
    '''
    sql_execute(sql, (direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia, id))

#####_ ADICIONALES _#####


