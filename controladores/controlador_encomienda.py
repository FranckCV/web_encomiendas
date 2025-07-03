from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import uuid
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
import logging
from decimal import Decimal
from controladores.bd import obtener_conexion
from flask import current_app
logger = logging.getLogger(__name__)
from num2words import num2words


table_name = 'transaccion_encomienda'

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
    sql = '''
        SELECT 
            te.num_serie,
            te.masivo,
            te.id_sucursal_origen,
            te.monto_total,
            te.fecha,
            te.hora,
            te.clienteid,
            te.monto_total,
            te.recojo_casa,
            te.direccion_recojo,
            te.descripcion,
            CASE 
                WHEN te.masivo = 1 THEN 'Masivo'
                ELSE 'Individual'
            END AS masivo_txt,
            CASE 
                WHEN te.recojo_casa = 1 THEN 'Sí'
                ELSE 'No'
            END AS recojo_casa_txt,
            CONCAT(
                u.departamento, '/', u.provincia, '/', u.distrito, ' - ', s.direccion
            ) AS nom_sucursal_origen,
            CONCAT(
                COALESCE(c.nombre_siglas, ''), ' ', COALESCE(c.apellidos_razon, '')
            ) AS nombre_cliente 

        FROM transaccion_encomienda te
        INNER JOIN cliente c ON c.id = te.clienteid
        INNER JOIN sucursal s ON s.id = te.id_sucursal_origen
        INNER JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        ORDER BY te.fecha DESC, te.hora DESC;
    '''

    columnas = {
        'num_serie': ['N° Serie', 2],
        'masivo_txt': ['Tipo de Envío', 1.2], 
        'monto_total': ['Monto Total S/.', 1],
        'nom_sucursal_origen': ['Sucursal Origen', 4],
        # 'recojo_casa_txt': ['¿Recojo en casa?', 1],
        'fecha': ['Fecha', 1],
        'hora': ['Hora', 1],
        'nombre_cliente': ['Cliente', 2],
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas




# def insert_rows(cliente:dict):
#     try:
        
#     except Exception as e:
        
def update_row( id , nombre ):
    sql = f'''
        update {table_name} set 
        nombre = %s 
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql, (nombre ))

    unactive_row_table(table_name , id)
 

def insert_cliente(correo, telefono, num_doc, nombre, tipo_doc):
    # 1) Verificamos si ya existe
    verificar_sql = "SELECT id FROM cliente WHERE num_documento = %s"
    existente = sql_select_fetchall(verificar_sql, (num_doc,))
    if existente:
        return existente[0]['id']

    # 2) Elegimos columna y tipo_cliente según tipo de documento
    if tipo_doc == 2:
        column = 'apellidos_razon'
        tipo_cliente = 2
    else:
        column = 'nombre_siglas'
        tipo_cliente = 1

    # 3) Insertamos y devolvemos el id recién generado
    insert_sql = f"""
        INSERT INTO cliente (
            correo,
            telefono,
            num_documento,
            {column},
            tipo_documentoid,
            tipo_clienteid
        ) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    params = (correo, telefono, num_doc, nombre, tipo_doc, tipo_cliente)
    new_row = sql_execute(insert_sql, params, fetchone=True)
    return new_row['id']



# def registrar_encomienda(num_serie, masivo, descripcion, recojo_casa, id_sucursal_origen, estado_pago, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid) :
#     sql = f'''
#         INSERT INTO transaccion_encomienda
#         (num_serie, masivo, descripcion, recojo_casa, id_sucursal_origen, estado_pago, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid) 
#         VALUES
#         (%, %s, %s, %s, %s, estado_pago, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid) 
#     '''
#     id = sql_execute_lastrowid(sql,(num_serie, masivo, descripcion, recojo_casa, id_sucursal_origen, estado_pago, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid) )
#     return id

# Firma de la función

def crear_transaccion_y_paquetes(registros, cliente_data, tipo_comprobante, metodo_pago, sucursal_origen,modo):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            row = sql_select_fetchone(
                "SELECT id FROM cliente WHERE num_documento = %s",
                (cliente_data['num_documento'],)
            )
            if row:
                cliente_id = row['id']
            else:
                cliente_id = sql_execute_lastrowid(
                    """
                    INSERT INTO cliente
                    (correo, telefono, num_documento, nombre_siglas,
                     apellidos_razon, tipo_documentoid, tipo_clienteid)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        cliente_data['correo'],
                        cliente_data['telefono'],
                        cliente_data['num_documento'],
                        cliente_data['nombre_siglas'],
                        cliente_data['apellidos_razon'],
                        cliente_data['tipo_documentoid'],
                        cliente_data['tipo_clienteid']
                    )
                )

            masivo = 1 if modo == 'masivo' else 0
            print("masivo : ",masivo)
            monto_total = sum(Decimal(r.get('tarifa', 0)) for r in registros).quantize(Decimal('0.01'))
            print(monto_total)
            descripcion = f"Envío {'masivo' if masivo else 'individual'}"

            cursor.execute(
                """
                INSERT INTO transaccion_encomienda
                (masivo, descripcion, monto_total, 
                recojo_casa, id_sucursal_origen, fecha, hora, clienteid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    masivo,
                    descripcion,
                    float(monto_total),
                    0,  
                    sucursal_origen,
                    date.today(),
                    datetime.now().strftime('%H:%M:%S'),
                    cliente_id
                )
            )


            num_serie = cursor.lastrowid
            print("num_serie", num_serie)

            if tipo_comprobante and metodo_pago:
                cursor.execute(
                    """
                    INSERT INTO metodo_pago_venta (num_serie, tipo_comprobante, metodo_pagoid)
                    VALUES (%s, %s, %s)
                    """,
                    (num_serie, tipo_comprobante, metodo_pago)
                )
                
            print("metodo_pago : ",cursor.lastrowid)
            trackings = []

            for r in registros:
                tipo_empaque = int(r.get('tipoEmpaqueId', 1))
                tipo_entrega = int(r.get('tipoEntregaId', 1))

                clave = r['clave']
                valor = float(r.get('valorEnvio') or 0)
                peso = float(r.get('peso') or 0)
                tarifa = float(r.get('tarifa') or 0)
                ancho = float(r.get('ancho') or 0) if tipo_empaque != 2 else None
                alto = float(r.get('alto') or 0) if tipo_empaque != 2 else None
                largo = float(r.get('largo') or 0) if tipo_empaque != 2 else None

                dest = r['destinatario']
                tipo_doc_dest = int(dest.get('tipo_doc_destinatario', 1))
                num_doc_dest = dest.get('num_doc_destinatario', '')
                tel_dest = dest.get('num_tel_destinatario', '')

                if tipo_doc_dest == 2:
                    nombre_contacto_destinatario = dest.get('contacto')
                    apellido_razon_destinatario = dest.get('razon_social')
                else:
                    nombre_contacto_destinatario = dest.get('nombres')
                    apellido_razon_destinatario = dest.get('apellidos')

                suc_dest_id = int(r['destino']['sucursal_destino'])
                modalidad_pago = r.get('modalidadPago')
                estado_pago = 'C' if modalidad_pago == '1' else 'P'
                contenido_paqueteid = int(r.get('tipoArticuloId')) if tipo_empaque == 1 else None
                cantidad_folios = r.get('cantidad_folios') if tipo_empaque == 2 else None
                direccion_destinatario = r.get('direccion_destinatario') if tipo_entrega == 2 else ''

                cursor.execute(
                    """
                    INSERT INTO paquete
                    (clave, valor, peso, alto, largo, precio_ruta, ancho, descripcion,
                    direccion_destinatario, telefono_destinatario, num_documento_destinatario,
                    sucursal_destino_id, tipo_documento_destinatario_id, tipo_empaqueid,
                    contenido_paqueteid, tipo_recepcionid, salidaid, transaccion_encomienda_num_serie,
                    qr_url, estado_pago, modalidad_pagoid, nombres_contacto_destinatario,
                    apellidos_razon_destinatario, cantidad_folios)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        clave, valor, peso, alto, largo, tarifa, ancho, '',  # descripcion
                        direccion_destinatario, tel_dest, num_doc_dest,
                        suc_dest_id, tipo_doc_dest, tipo_empaque,
                        contenido_paqueteid, tipo_entrega, None, num_serie,
                        None, estado_pago, modalidad_pago,
                        nombre_contacto_destinatario, apellido_razon_destinatario, cantidad_folios
                    )
                )


                paquete_id = cursor.lastrowid
                cursor.execute(
                    """
                    INSERT INTO seguimiento
                    (paquetetracking, detalle_estadoid, fecha, hora)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (paquete_id, 1, date.today(), datetime.now().strftime('%H:%M:%S'))
                )
                trackings.append(paquete_id)

            conexion.commit()
            return num_serie, trackings

    except Exception as e:
        conexion.rollback()
        print(str(e))
        return str(e), []

    finally:
        conexion.close()


def get_transaction_by_tracking(tracking):
    sql = '''
SELECT 
            te.num_serie,
            te.masivo,
            te.descripcion,
            te.monto_total,
            te.fecha,
            te.hora,
            te.clienteid,
            c.nombre_siglas,
            c.apellidos_razon
        FROM paquete p
        INNER JOIN transaccion_encomienda te 
            ON te.num_serie = p.transaccion_encomienda_num_serie
        INNER JOIN cliente c 
            ON c.id = te.clienteid
        WHERE p.tracking = %s
    '''
    fila = sql_select_fetchone(sql, (tracking,))
    return fila



def obtener_items_por_num_serie(num_serie):
    transaccion = sql_select_fetchone("""
        SELECT masivo, id_sucursal_origen
        FROM transaccion_encomienda
        WHERE num_serie = %s
    """, (num_serie,))

    if not transaccion:
        raise ValueError("No se encontró la transacción para el número de serie dado")

    masivo = transaccion['masivo']
    sucursal_origen_id = transaccion['id_sucursal_origen']

    origen = sql_select_fetchone("""
        SELECT s.direccion AS sucursal, 
               u.distrito AS distrito,
               u.provincia AS provincia,
               u.departamento AS departamento
        FROM sucursal s
        INNER JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        WHERE s.id = %s
    """, (sucursal_origen_id,))

    if not origen:
        raise ValueError("Sucursal de origen no encontrada")

    paquetes = sql_select_fetchall("""
       SELECT
            p.clave,
            p.precio_ruta AS tarifa,
            p.estado_pago,
            s.direccion AS sucursal_destino,
            u.distrito AS distrito_destino,
            u.provincia AS provincia_destino,
            u.departamento AS departamento_destino
        FROM paquete p
        JOIN sucursal s ON p.sucursal_destino_id = s.id
        INNER JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        WHERE p.transaccion_encomienda_num_serie = %s
    """, (num_serie,))

    items = []
    for p in paquetes:
        destino = {
            'sucursal': p['sucursal_destino'],
            'distrito': p['distrito_destino'],
            'provincia': p['provincia_destino'],
            'departamento': p['departamento_destino']
        }

        quien_paga = 'Destinatario' if p['estado_pago'] == 'P' else 'Remitente'

        items.append({
            'clave': p['clave'],
            'tarifa': float(p['tarifa']),
            'quien_paga': quien_paga,
            'origen': origen,
            'destino': destino
        })

    return items, masivo





def calcular_resumen_venta(monto_total, igv):
    monto_total = Decimal(monto_total)
    igv = Decimal(igv)

    factor = (igv / Decimal(100)) + Decimal(1)
    base_imponible = (monto_total / factor).quantize(Decimal('0.01'))
    igv_valor = (monto_total - base_imponible).quantize(Decimal('0.01'))

    entero = int(monto_total)
    centimos = int(round((monto_total - entero) * 100))
    importe_letras = f"{num2words(entero, lang='es').upper()} CON {centimos:02d}/100 SOLES"

    return {
        'base_imponible': base_imponible,
        'igv': igv_valor,
        'total': monto_total,
        'importe_letras': importe_letras
    }



def insert_row(
        num_serie, 
        masivo, 
        id_sucursal_origen, 
        fecha, 
        hora, 
        comprobante_serie, 
        clienteid, 
        tipo_comprobanteid,
        monto_total = None, 
        recojo_casa = None, 
        direccion_recojo = None, 
        descripcion = None
        ):
    sql = f'''
        INSERT INTO {table_name} (
        num_serie, masivo, descripcion, monto_total, recojo_casa, id_sucursal_origen, fecha, hora, direccion_recojo, comprobante_serie, clienteid, tipo_comprobanteid
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    sql_execute(sql, (num_serie, masivo, descripcion, monto_total, recojo_casa, id_sucursal_origen, fecha, hora, direccion_recojo, comprobante_serie, clienteid, tipo_comprobanteid))

MASIVO = {
    0: 'Individual' ,
    1: 'Masivo' ,
}

RECOJO_CASA = {
    1: 'Si' ,
    0: 'No' ,
}


def get_select_tipo_envio():
    lst = MASIVO.keys()
    filas = []
    for ele in lst:
        filas.append([ele , MASIVO[ele]])
    return filas


def get_select_recojo_casa():
    lst = RECOJO_CASA.keys()
    filas = []
    for ele in lst:
        filas.append([ele , RECOJO_CASA[ele]])
    return filas



def get_recojo_casa():
    sql = '''
        select
    num_serie,
    direccion_recojo,
    concat(c.nombre_siglas,' ',c.apellidos_razon),
    c.telefono
    from transaccion_encomienda te 
    inner join cliente c on c.id = te.clienteid
    where te.recojo_casa != 0
    '''
    fila = sql_select_fetchall(sql)
    return fila


def get_num_serie_by_tracking(tracking):
    sql = '''
        select transaccion_encomienda_num_serie from paquete where tracking = %s
    '''
    fila = sql_select_fetchone(sql,(tracking,))
    
    return fila

def datos_rotulo(tracking):
    sql = '''
        select te.fecha, 
        concat(c.nombre_siglas,' ',c.apellidos_razon) as nombre_remitente, 
        c.num_documento as doc_remitente,
        concat(u.departamento,' / ',u.provincia,' / ',u.distrito) as origen 
        ,concat(p.nombres_contacto_destinatario,' ',p.apellidos_razon_destinatario) as nom_destinatario,
        p.num_documento_destinatario as doc_destinatario,
        concat(ud.departamento,' / ',ud.provincia,' / ',ud.distrito) as destino,
        p.tracking
        from paquete p
        inner join transaccion_encomienda te on te.num_serie = p.transaccion_encomienda_num_serie
        inner join cliente c on c.id = te.clienteid
        inner join sucursal so on so.id = te.id_sucursal_origen
        inner join sucursal sd on sd.id = p.sucursal_destino_id
        inner join ubigeo u on u.codigo = so.ubigeocodigo
        inner join ubigeo ud on ud.codigo = sd.ubigeocodigo
        where p.tracking = %s
    '''
    fila = sql_select_fetchone(sql,(tracking,))
    return fila