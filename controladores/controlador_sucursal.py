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
    sql = f'''
        SELECT 
            s.id,
            s.abreviatura,
            s.codigo_postal,
            s.direccion,
            CONCAT(u.departamento, " / ", u.provincia, " / ", u.distrito) AS ubigeo,
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
        'abreviatura': ['Abreviatura', 1],
        'codigo_postal': ['C. Postal', 1], 
        'direccion': ['Dirección', 3],
        'ubigeo': ['Ubigeo', 2.5],
        # 'horario_l_v': ['Horario L-V', 2.5],
        # 'horario_s_d': ['Horario S-D', 2.5],
        # 'teléfono': ['Teléfono', 1.5],
        'activo': ['Activo', 1]
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas


######_ CRUD ESPECIFICAS _###### 

def unactive_row(id):
    unactive_row_table("sucursal", id)

def insert_row(abreviatura, codigo_postal, direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia):
    sql = f'''
        INSERT INTO {table_name} 
        (abreviatura, codigo_postal, direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
    '''


    horario_l_v = str(horario_l_v) if horario_l_v is not None else None
    horario_s_d = str(horario_s_d) if horario_s_d is not None else None

    sql_execute(sql, (abreviatura, codigo_postal, direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia))



def update_row(abreviatura, codigo_postal, direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia, id):
    sql = f'''
        UPDATE sucursal SET 
            abreviatura = %s,
            codigo_postal = %s,
            direccion = %s,
            ubigeocodigo = %s,
            horario_l_v = %s,
            horario_s_d = %s,
            latitud = %s,
            longitud = %s,
            teléfono = %s,
            referencia = %s
        WHERE {get_primary_key()} = %s
    '''
    sql_execute(sql, (abreviatura, codigo_postal, direccion, ubigeocodigo, horario_l_v, horario_s_d, latitud, longitud, teléfono, referencia, id))


#####_ ADICIONALES _#####
def get_options():
    sql= f'''
        select 
            {get_primary_key()} ,
            direccion
        from {table_name}
        where activo = 1
        order by direccion asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila[get_primary_key()], fila["direccion"]) for fila in filas]

    return lista


def get_agencias_data():
    sql = '''
        SELECT 
            s.id,
            s.abreviatura,
            s.direccion,
            s.latitud,
            s.longitud,
            s.teléfono,
            s.horario_l_v,
            s.horario_s_d,
            u.departamento,
            u.provincia,
            u.distrito
        FROM 
            sucursal s
        INNER JOIN 
            ubigeo u ON u.codigo = s.ubigeocodigo
        WHERE 
            s.activo = 1 AND u.activo = 1  AND latitud is not null and longitud is not null
    '''
    resultados = sql_select_fetchall(sql)

    # Convertimos los resultados a un formato similar al de agenciasData
    agencias = []
    for fila in resultados:
        agencias.append({
            "id": fila["id"],
            "nombre": f"Sucursal {fila['departamento']} - {fila['abreviatura'][-2:]}",  # Puedes cambiar esto si tienes un campo específico para nombre
            "departamento": fila["departamento"],
            "provincia": fila["provincia"],
            "distrito": fila["distrito"],
            "direccion": fila["direccion"],
            "lat": float(fila["latitud"]),
            "lng": float(fila["longitud"]),
            "telefono": fila["teléfono"],
            "horario": f"Lun-Vier: {fila['horario_l_v']}, Sáb-Dom: {fila['horario_s_d']}"
        })

    return agencias

def get_ubigeo():
    sql = '''
            select
            s.id, 
            s.direccion,
            u.departamento,
            u.provincia,
            u.distrito
            from 
            sucursal s
            inner join ubigeo u on u.codigo = s.ubigeocodigo
                 '''
    filas = sql_select_fetchall(sql)
    
    #Crear estructura de diccionario
    estructura = {}
    
    for fila in filas:
        dep = fila['departamento']
        prov = fila['provincia']
        dist = fila['distrito']
        sucursal = {
            'id' : fila['id'],
            'direc' : fila['direccion']
        }
        
        estructura.setdefault(dep,{}) #clave, diccionario
        estructura[dep].setdefault(prov,{})    
        estructura[dep][prov].setdefault(dist,[])
        estructura[dep][prov][dist].append(sucursal)
    
    return estructura
    
    

def get_ubigeo_sucursal():
    sql = '''
            select
            s.id, 
            CONCAT(u.departamento, ' / ', u.provincia, ' / ', u.distrito, ' / ' , s.direccion) AS direccion_completa
            from 
            sucursal s
            inner join ubigeo u on u.codigo = s.ubigeocodigo
                 '''
    filas = sql_select_fetchall(sql)
    
    
    
    return filas
    
    

def get_report_horario():
    sql = f'''
        SELECT 
            s.id,
            s.abreviatura,
            s.codigo_postal,
            s.direccion,
            CONCAT(u.departamento, " / ", u.provincia, " / ", u.distrito) AS ubigeo,
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
            ubigeo u ON u.codigo = s.ubigeocodigo
        where s.activo = 1
    '''

    columnas = {
        'id': ['ID', 0.5],
        'abreviatura': ['Abreviatura', 0.75],
        'horario_l_v': ['Horario L-V', 1.5],
        'horario_s_d': ['Horario S-D', 1.5],
        # 'direccion': ['Dirección', 3],
        'ubigeo': ['Ubigeo', 2.5],
        # 'codigo_postal': ['C. Postal', 0.5], 
        # 'teléfono': ['Teléfono', 1.5],
        # 'activo': ['Activo', 0.5]
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas







def get_options_departamento_sucursal():
    sql= f'''
        SELECT DISTINCT 
            ub.departamento 
        FROM ubigeo ub
        inner join sucursal su on ub.codigo = su.ubigeocodigo
        where ub.activo = 1
        order by ub.departamento
    '''
    filas = sql_select_fetchall(sql)
    return filas


def get_options_provincia_sucursal():
    sql= f'''
        SELECT DISTINCT 
            ub.departamento ,
            ub.provincia
        FROM ubigeo ub
        inner join sucursal su on ub.codigo = su.ubigeocodigo
        where ub.activo = 1
        order by ub.departamento , ub.provincia
    '''
    filas = sql_select_fetchall(sql)
    
    # lista = [( fila["departamento"] , fila["provincia"]) for fila in filas]
    lista = filas
    return lista


def get_options_distrito_sucursal():
    sql= f'''
        SELECT DISTINCT
            ub.codigo , 
            ub.departamento ,
            ub.provincia ,
            ub.distrito 
        FROM ubigeo ub
        inner join sucursal su on ub.codigo = su.ubigeocodigo
        where ub.activo = 1
        order by ub.departamento , ub.provincia , ub.distrito
    '''
    filas = sql_select_fetchall(sql)
    return filas


def get_options_ubigeo_sucursal():
    sql= f'''
        SELECT 
            ubi.codigo ,
            suc.id ,
            concat(suc.abreviatura,' / ', suc.direccion) as nom_sucursal
        FROM `sucursal` suc
        inner join ubigeo ubi on ubi.codigo = suc.ubigeocodigo
    '''
    filas = sql_select_fetchall(sql)
    return filas


