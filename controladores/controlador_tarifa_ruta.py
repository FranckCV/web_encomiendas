from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'tarifa_ruta'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( sucursal_origen_id , sucursal_destino_id ):
    sql = f'''
        delete from tarifa_ruta
        where sucursal_origen_id = {sucursal_origen_id} and sucursal_destino_id = {sucursal_destino_id}
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
    sql = '''
        SELECT 
            tr.sucursal_origen_id,
            tr.sucursal_destino_id,
            so.abreviatura AS sucursal_origen,
            sd.abreviatura AS sucursal_destino,
            tr.tarifa
        FROM 
            tarifa_ruta tr
        INNER JOIN sucursal so ON so.id = tr.sucursal_origen_id
        INNER JOIN sucursal sd ON sd.id = tr.sucursal_destino_id;
    '''

    columnas = {
        'sucursal_origen': ['Sucursal Origen', 2],
        'sucursal_destino': ['Sucursal Destino', 2],
        'tarifa': ['Tarifa (S/)', 1.5]
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas



######_ CRUD ESPECIFICAS _###### 

def unactive_row(id):
    unactive_row_table("sucursal", id)


def insert_row(sucursal_origen_id, sucursal_destino_id, tarifa):
    sql = '''
        INSERT INTO tarifa_ruta (sucursal_origen_id, sucursal_destino_id, tarifa)
        VALUES (%s, %s, %s)
    '''
    sql_execute(sql, (sucursal_origen_id, sucursal_destino_id, tarifa))


def update_row(sucursal_origen_id, sucursal_destino_id, tarifa):
    sql = '''
        UPDATE tarifa_ruta
        SET tarifa = %s
        WHERE sucursal_origen_id = %s AND sucursal_destino_id = %s
    '''
    sql_execute(sql, (tarifa, sucursal_origen_id, sucursal_destino_id))


#####_ ADICIONALES _#####


def get_options_departamento_origen():
    sql= f'''
        select distinct
            uori.departamento as departamento
        from tarifa_ruta tar 
        inner join sucursal ori on ori.id = tar.sucursal_origen_id 
        inner join sucursal des on des.id = tar.sucursal_destino_id 
        inner join ubigeo uori on uori.codigo = ori.ubigeocodigo 
        inner join ubigeo udes on udes.codigo = des.ubigeocodigo
    '''
    filas = sql_select_fetchall(sql)
    return filas


def get_options_provincia_origen():
    sql= f'''
        select distinct
            uori.departamento as departamento ,
            uori.provincia as provincia
        from tarifa_ruta tar 
        inner join sucursal ori on ori.id = tar.sucursal_origen_id 
        inner join sucursal des on des.id = tar.sucursal_destino_id 
        inner join ubigeo uori on uori.codigo = ori.ubigeocodigo 
        inner join ubigeo udes on udes.codigo = des.ubigeocodigo
    '''
    filas = sql_select_fetchall(sql)
    return filas


def get_options_distrito_origen():
    sql= f'''
        select distinct
            uori.codigo , 
            uori.departamento ,
            uori.provincia ,
            uori.distrito as distrito
        from tarifa_ruta tar 
        inner join sucursal ori on ori.id = tar.sucursal_origen_id 
        inner join sucursal des on des.id = tar.sucursal_destino_id 
        inner join ubigeo uori on uori.codigo = ori.ubigeocodigo 
        inner join ubigeo udes on udes.codigo = des.ubigeocodigo
    '''
    filas = sql_select_fetchall(sql)
    return filas


def get_options_sucursal_origen():
    sql= f'''
        select 
            uori.codigo ,
            ori.id as id ,
            concat(ori.abreviatura,' / ', ori.direccion) as nom_sucursal
        from tarifa_ruta tar 
        inner join sucursal ori on ori.id = tar.sucursal_origen_id 
        inner join sucursal des on des.id = tar.sucursal_destino_id 
        inner join ubigeo uori on uori.codigo = ori.ubigeocodigo 
        inner join ubigeo udes on udes.codigo = des.ubigeocodigo
    '''
    filas = sql_select_fetchall(sql)
    return filas




def get_options_departamento_destino(sucursal_id):
    sql= f'''
        select distinct
            udes.departamento as departamento
        from tarifa_ruta tar 
        inner join sucursal ori on ori.id = tar.sucursal_origen_id 
        inner join sucursal des on des.id = tar.sucursal_destino_id 
        inner join ubigeo uori on uori.codigo = ori.ubigeocodigo 
        inner join ubigeo udes on udes.codigo = des.ubigeocodigo
        where ori.id = %s
    '''
    filas = sql_select_fetchall(sql,(sucursal_id))
    return filas


def get_options_provincia_destino(sucursal_id):
    sql= f'''
        select distinct
            udes.departamento as departamento ,
            udes.provincia as provincia
        from tarifa_ruta tar 
        inner join sucursal ori on ori.id = tar.sucursal_origen_id 
        inner join sucursal des on des.id = tar.sucursal_destino_id 
        inner join ubigeo uori on uori.codigo = ori.ubigeocodigo 
        inner join ubigeo udes on udes.codigo = des.ubigeocodigo
        where ori.id = %s
    '''
    filas = sql_select_fetchall(sql,(sucursal_id))
    return filas


def get_options_distrito_destino(sucursal_id):
    sql= f'''
        select distinct
            udes.codigo , 
            udes.departamento ,
            udes.provincia ,
            udes.distrito as distrito
        from tarifa_ruta tar 
        inner join sucursal ori on ori.id = tar.sucursal_origen_id 
        inner join sucursal des on des.id = tar.sucursal_destino_id 
        inner join ubigeo uori on uori.codigo = ori.ubigeocodigo 
        inner join ubigeo udes on udes.codigo = des.ubigeocodigo
        where ori.id = %s
    '''
    filas = sql_select_fetchall(sql,(sucursal_id))
    return filas


def get_options_sucursal_destino(sucursal_id):
    sql= f'''
        select 
            udes.codigo ,
            des.id as id ,
            concat(des.abreviatura,' / ', des.direccion) as nom_sucursal
        from tarifa_ruta tar 
        inner join sucursal ori on ori.id = tar.sucursal_origen_id 
        inner join sucursal des on des.id = tar.sucursal_destino_id 
        inner join ubigeo uori on uori.codigo = ori.ubigeocodigo 
        inner join ubigeo udes on udes.codigo = des.ubigeocodigo
        where ori.id = %s
    '''
    filas = sql_select_fetchall(sql,(sucursal_id))
    return filas


def get_tarifa_ids(origen_id , destino_id):
    sql= f'''
        select
            tarifa 
        FROM tarifa_ruta 
        WHERE sucursal_origen_id = %s and sucursal_destino_id = %s
    '''
    filas = sql_select_fetchone(sql,(origen_id , destino_id))
    return filas


def calcularTarifaTotal( tarifa_ruta , peso , porcentaje_recojo , porcentaje_valor , porcentaje_peso ):
    kilos_exceso = peso - 1 
    porcentaje_valor = porcentaje_valor / 100 
    
    peso_porcentaje = kilos_exceso * porcentaje_peso / 100 if porcentaje_recojo > 0 else kilos_exceso
    aumento_peso = tarifa_ruta * peso_porcentaje
    aumento_valor = tarifa_ruta * porcentaje_valor

    aumento_recojo = tarifa_ruta * porcentaje_recojo / 100

    total = tarifa_ruta + aumento_peso + aumento_valor + aumento_recojo

    return total



