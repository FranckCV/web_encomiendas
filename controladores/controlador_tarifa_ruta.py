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

def get_sucursales_origen_destino():
    sql = '''
        SELECT 
            s_origen.id AS id_origen,
            u_origen.departamento AS dep_origen,
            u_origen.provincia AS prov_origen,
            u_origen.distrito AS dist_origen,
            s_origen.direccion AS direc_origen,
            
            s_destino.id AS id_destino,
            u_destino.departamento AS dep_destino,
            u_destino.provincia AS prov_destino,
            u_destino.distrito AS dist_destino,
            s_destino.direccion AS direc_destino,
            
            tr.tarifa
        FROM tarifa_ruta tr
        INNER JOIN sucursal s_origen ON s_origen.id = tr.sucursal_origen_id
        INNER JOIN ubigeo u_origen ON u_origen.codigo = s_origen.ubigeocodigo
        INNER JOIN sucursal s_destino ON s_destino.id = tr.sucursal_destino_id
        INNER JOIN ubigeo u_destino ON u_destino.codigo = s_destino.ubigeocodigo
    '''
    filas = sql_select_fetchall(sql)

    estructura = {}

    for fila in filas:
        origen_key = f"{fila['dep_origen']}|{fila['prov_origen']}|{fila['dist_origen']}"
        destino = {
            'id': fila['id_destino'],
            'departamento': fila['dep_destino'],
            'provincia': fila['prov_destino'],
            'distrito': fila['dist_destino'],
            'direccion': fila['direc_destino'],
            'tarifa': fila['tarifa'],
            'id_origen': fila['id_origen'] 
        }

        estructura.setdefault(origen_key, []).append(destino)

    return estructura


def get_departamentos_origen():
    sql = '''
        SELECT DISTINCT
            u.departamento
        FROM tarifa_ruta tr
        JOIN sucursal    s_origen ON s_origen.id     = tr.sucursal_origen_id
        JOIN ubigeo      u        ON u.codigo          = s_origen.ubigeocodigo;
    '''
    filas = sql_select_fetchall(sql)
    return  filas

def get_provincia_origen(dep):
    sql = '''
        SELECT DISTINCT
            u.provincia
        FROM tarifa_ruta tr
        JOIN sucursal    s_origen ON s_origen.id     = tr.sucursal_origen_id
        JOIN ubigeo      u        ON u.codigo          = s_origen.ubigeocodigo
        where u.departamento = %s;
    '''
    filas = sql_select_fetchall(sql,dep)
    return  filas

def get_distrito_origen(prov):
    sql = '''
        SELECT DISTINCT
            u.distrito
        FROM tarifa_ruta tr
        JOIN sucursal    s_origen ON s_origen.id     = tr.sucursal_origen_id
        JOIN ubigeo      u        ON u.codigo          = s_origen.ubigeocodigo
        where u.provincia = %s;
    '''
    filas = sql_select_fetchall(sql,prov)
    return  filas

def get_ubigeo_origen(dep,prov,dist):
    sql = '''
        select codigo from ubigeo where departamento = %s and provincia = %s and distrito = %s
    
    '''
    filas = sql_select_fetchall(sql,(dep,prov,dist))
    return filas



def get_departamento_destino(codigo):
    sql = '''
        SELECT codDestino.departamento
        from tarifa_ruta tr
            inner join sucursal origen on origen.id=tr.sucursal_origen_id
            inner join ubigeo codOrigen on codOrigen.codigo = origen.ubigeocodigo
            inner join sucursal destino on destino.id=tr.sucursal_destino_id
            inner join ubigeo codDestino on codDestino.codigo=destino.ubigeocodigo
            where origen.ubigeocodigo = %s    
    '''
    filas = sql_select_fetchall(sql,(codigo))
    return filas


def get_provincia_destino(dep):
    sql = '''
         SELECT distinct uDestino.provincia
        from tarifa_ruta tr
            inner join sucursal destino on destino.id=tr.sucursal_destino_id
            inner join ubigeo uDestino on uDestino.codigo=destino.ubigeocodigo
            where uDestino.departamento=%s
    '''
    filas = sql_select_fetchall(sql,(dep))
    return filas


def get_distrito_destino(prov):
    sql = '''
         SELECT distinct uDestino.distrito
        from tarifa_ruta tr
            inner join sucursal destino on destino.id=tr.sucursal_destino_id
            inner join ubigeo uDestino on uDestino.codigo=destino.ubigeocodigo
            where uDestino.provincia=%s
    '''
    filas = sql_select_fetchall(sql,(prov))
    return filas


def get_tarifa_origen():
    sql = '''
        SELECT DISTINCT
            s_origen.ubigeocodigo,
            u.departamento,
            u.provincia,
            u.distrito
        FROM tarifa_ruta tr
        JOIN sucursal    s_origen ON s_origen.id     = tr.sucursal_origen_id
        JOIN ubigeo      u        ON u.codigo          = s_origen.ubigeocodigo;

    '''
    filas = sql_select_fetchall(sql)
    return {f"{f['id_origen']}|{f['id_destino']}": f['tarifa'] for f in filas}

def get_tarifa_destino():
    sql = '''
        SELECT 
            s_origen.id AS id_origen,
            s_destino.id AS id_destino,
        FROM tarifa_ruta tr
        INNER JOIN sucursal s_origen ON s_origen.id = tr.sucursal_origen_id
        INNER JOIN sucursal s_destino ON s_destino.id = tr.sucursal_destino_id
    '''
    filas = sql_select_fetchall(sql)
    return {f"{f['id_origen']}|{f['id_destino']}": f['tarifa'] for f in filas}


def get_tarifas_ruta_dict():
    sql = '''
        SELECT 
            s_origen.id AS id_origen,
            s_destino.id AS id_destino,
            tr.tarifa
        FROM tarifa_ruta tr
        INNER JOIN sucursal s_origen ON s_origen.id = tr.sucursal_origen_id
        INNER JOIN sucursal s_destino ON s_destino.id = tr.sucursal_destino_id
    '''
    filas = sql_select_fetchall(sql)
    return {f"{f['id_origen']}|{f['id_destino']}": f['tarifa'] for f in filas}



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
        select distinct
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

from decimal import Decimal

from decimal import Decimal

def calcularTarifaTotal(tarifa_ruta, peso, porcentaje_recojo, porcentaje_valor, porcentaje_peso):
    # Convertir todos los valores a Decimal
    tarifa_ruta = Decimal(str(tarifa_ruta))
    peso = Decimal(str(peso))
    porcentaje_recojo = Decimal(str(porcentaje_recojo))
    porcentaje_valor = Decimal(str(porcentaje_valor))
    porcentaje_peso = Decimal(str(porcentaje_peso))
    print(tarifa_ruta) 
    print(peso)
    print(porcentaje_recojo)
    print(porcentaje_valor)
    print(porcentaje_peso)

    # Calcular kilos en exceso (solo los kilos adicionales a 1)
    kilos_exceso = peso - Decimal('1')
    kilos_exceso = kilos_exceso if kilos_exceso > 0 else Decimal('0')

    # Calcular aumentos
    valor = porcentaje_valor / Decimal('100')
    peso_porcentaje = kilos_exceso * (porcentaje_peso / Decimal('100'))
    aumento_recojo = tarifa_ruta * (porcentaje_recojo / Decimal('100'))
    aumento_peso = tarifa_ruta * peso_porcentaje
    aumento_valor = tarifa_ruta * valor

    # Total
    total = tarifa_ruta + aumento_peso + aumento_valor + aumento_recojo
    print(total)
    return round(total, 2)


    





