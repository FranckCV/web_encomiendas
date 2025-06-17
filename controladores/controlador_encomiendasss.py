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

def consultar_tarifa(sucursal_origen_id, sucursal_destino_id):
    sql = '''
        SELECT tarifa
        FROM tarifa_ruta
        WHERE sucursal_origen_id = %s AND sucursal_destino_id = %s
    '''
    resultado = sql_select_fetchone(sql, (sucursal_origen_id, sucursal_destino_id))
    
    if resultado:
        return resultado['tarifa']
    else:
        return None
    
def insertar_pago(data, tipo_pago):
    sql = """
        INSERT INTO encomiendas (
            tipo_documento_origen, dni_origen, cel_origen, nombre_remitente, email,
            id_origen, tipo_recepcion, cod_seguridad, id_destino,
            id_empaque, valor_paquete, peso, largo, ancho, alto, descripcion,
            tipo_documento_destino, dni_destino, cel_destino, nombre_destinatario,
            contacto_destino, distrito_origen, distrito_destino_sucursal,
            direccion_destino, tarifa, estado, tipo_pago, folios
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, '1', %s, %s)
    """
    datos = (
        data['tipo_documento_origen'], data['dni_origen'], data['cel_origen'], data['nombre_remitente'], data['email'],
        data['id_origen'], data['tipo_recepcion'], data['cod_seguridad'], data['id_destino'],
        data['id_empaque'], data['valor_paquete'], data['peso'], data['largo'], data['ancho'], data['alto'], data['descripcion'],
        data['tipo_documento_destino'], data['dni_destino'], data['cel_destino'], data['nombre_destinatario'],
        data['contacto_destino'], data['distrito_origen'], data['distrito_destino_sucursal'],
        data['direccion_destino'], data['total'], tipo_pago, data['folios']
    )

    id = sql_execute_lastrowid(sql, datos)
    return id

import random
from datetime import datetime

ahora = datetime.now()
fecha = ahora.strftime('%Y-%m-%d')     # Formato: 2025-06-11
hora = ahora.strftime('%H:%M:%S')   


def insertar_pago_2(data, tipo_pago, clave):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            # 1. Insertar cliente
            sql1 = '''
                INSERT INTO cliente(correo, telefono, num_documento, nombre_siglas, tipo_documentoid, tipo_clienteid)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            datos1 = (
                data['email'], data['cel_origen'], data['dni_origen'], data['nombre_remitente'],
                data['tipo_documento_origen'], 1
            )
            cur.execute(sql1, datos1)
            id_cliente = cur.lastrowid

            # 2. Generar num_serie y registrar transacción
            num_serie = 'SERIE-' + str(random.randint(100000, 999999))
            sql2 = '''
                INSERT INTO transaccion_encomienda(
                    num_serie, masivo, descripcion, monto_total, recojo_casa,
                    id_sucursal_origen, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid, comprobante_serie 
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            datos2 = (
                num_serie, 0, data['descripcion'], float(data['total']), 0, int(data['id_origen']),
                fecha, hora, data['direccion_destino'], id_cliente, 1,num_serie
            )
            cur.execute(sql2, datos2)

            # 3. Insertar paquete
            sql3 = '''
                INSERT INTO paquete(
    clave, valor, peso, alto, largo, precio_ruta, ancho, descripcion,
    direccion_destinatario, telefono_destinatario, num_documento_destinatario,
    sucursal_destino_id, tipo_documento_destinatario_id, tipo_empaqueid,
    tipo_recepcionid, transaccion_encomienda_num_serie, contenido_paqueteid,
    modalidad_pagoid, qr_url, cantidad_folios, estado_pago
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            datos3 = (
    clave, float(data['valor_paquete']), float(data['peso']), float(data['alto']), float(data['largo']),
                float(data['tarifa']), float(data['ancho']), data['descripcion'],
                data['direccion_destino'], data['cel_destino'], data['dni_destino'], int(data['id_destino']),
                data['tipo_documento_destino'], int(data['id_empaque']), data['tipo_recepcion'], 
                num_serie,
                data['tipo_articulo'] if data.get('tipo_articulo') not in [None, '', ' '] else None,
                "1","13","1","1"
)
            cur.execute(sql3, datos3)

        # ✅ Si todo salió bien, se hace el commit
        conexion.commit()
        return num_serie

    except Exception as e:
        # ❌ Si algo falla, rollback
        conexion.rollback()
        print("ERROR en transacción:", e)
        raise e  # Puedes manejarlo o relanzarlo

    finally:
        conexion.close()
