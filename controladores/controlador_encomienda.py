from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
import uuid
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
import logging
from decimal import Decimal

from flask import current_app
logger = logging.getLogger(__name__)


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
            
            CASE 
                WHEN te.masivo = 1 THEN 'Masivo'
                ELSE 'Individual'
            END AS isMasivo,
            te.recojo_casa,

            te.monto_total,
            CONCAT(
                COALESCE(u.departamento, ''), ' ',
                COALESCE(u.provincia, ''), ' ',
                COALESCE(u.distrito, ''), ' ',
                COALESCE(s.direccion, '')
            ) AS sucursal_origen,

            CASE 
                WHEN te.estado_pago = 'P' THEN 'Pendiente'
                WHEN te.estado_pago = 'C' THEN 'Cancelado'
                ELSE 'Desconocido'
            END AS pago,

            te.fecha,
            te.hora,

            te.direccion_recojo,

            COALESCE(tc.nombre, '') AS nom_tip_comprobante,

            CONCAT(
                COALESCE(c.nombre_siglas, ''), ' ',
                COALESCE(c.apellidos_razon, '')
            ) AS nombre_cliente

        FROM transaccion_encomienda te
        INNER JOIN cliente c ON c.id = te.clienteid
        INNER JOIN tipo_comprobante tc ON tc.id = te.tipo_comprobanteid
        INNER JOIN sucursal s ON s.id = te.id_sucursal_origen
        INNER JOIN ubigeo u ON u.codigo = s.ubigeocodigo;
    '''

    columnas = {
        'num_serie': ['N° Serie', 1],
        'isMasivo': ['Tipo de envío', 1.2],
        'monto_total': ['Monto Total', 1],
        # 'recojo_casa': ['Recojo a Domicilio', 1.2],
        'sucursal_origen': ['Sucursal Origen', 1.5],
        'pago': ['Estado de Pago', 1],
        'fecha': ['Fecha', 1],
        'hora': ['Hora', 1],
        # 'direccion': ['Dirección de Recojo', 2],
        'nom_tip_comprobante': ['Tipo de Comprobante', 1.5],
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

def crear_transaccion_y_paquetes(registros, cliente_data, tipo_comprobante):
    # 1) Cliente: obtener o crear
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

    # 2) Obtener la serie del tipo de comprobante
    result = sql_select_fetchone("SELECT inicial FROM tipo_comprobante WHERE id = %s", tipo_comprobante)
    if not result:
        raise ValueError("Tipo de comprobante no válido")
    inicial = result['inicial'].strip().upper()
    comprobante_serie = f"{inicial}001"

    # 3) Generar el nuevo correlativo
    row = sql_select_fetchone(
        """
        SELECT MAX(CAST(num_serie AS UNSIGNED)) as numero
        FROM transaccion_encomienda;
        """
    )
    nuevo_correlativo = (row['numero'] if row and row['numero'] else 0) + 1
    correlativo_str = str(nuevo_correlativo).zfill(6)
    num_serie = correlativo_str
    comprobante_serie_final = f"{comprobante_serie}-{correlativo_str}"

    # 4) Insertar transacción
    masivo = 1 if registros and registros[0].get('modo') == 'masivo' else 0
    monto_total = sum(Decimal(r.get('tarifa', 0)) for r in registros).quantize(Decimal('0.01'))
    descripcion = f"Envío {'masivo' if masivo else 'individual'} #{comprobante_serie_final}"
    direccion_recojo = ''

    sql_execute(
        """
        INSERT INTO transaccion_encomienda
        (num_serie, masivo, descripcion, monto_total, recojo_casa,
         id_sucursal_origen, fecha, hora,
         direccion_recojo, clienteid, tipo_comprobanteid, comprobante_serie)
        VALUES (%s, %s, %s, %s, 0, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            num_serie,
            masivo,
            descripcion,
            float(monto_total),
            int(registros[0]['origen']['sucursal_origen']),
            date.today(),
            datetime.now().strftime('%H:%M:%S'),
            direccion_recojo,
            cliente_id,
            tipo_comprobante,
            comprobante_serie_final
        )
    )

    # 5) Insertar paquetes y seguimiento
    trackings = []
    for idx, r in enumerate(registros):
        clave = r['clave']
        valor = float(r.get('valorEnvio') or 0)
        peso = float(r.get('peso') or 0)
        alto = float(r.get('alto') or 0)
        largo = float(r.get('largo') or 0)
        tarifa = float(r.get('tarifa') or 0)
        ancho = float(r.get('ancho') or 0)

        dest = r['destinatario']
        tipo_doc_dest = int(dest.get('tipo_doc_destinatario', 1))
        num_doc_dest = dest.get('num_doc_destinatario', '')
        tel_dest = dest.get('num_tel_destinatario', '')
        nombre_contacto_destinatario = dest.get('nombre_contacto')
        apellido_razon_destinatario = dest.get('apellido_razon')

        suc_dest_id = int(r['destino']['sucursal_destino'])
        estado_pago = r.get('estado_pago', 'P')
        modalidad_pago = r.get('modalidad_pago')
 
        contenido_paqueteid = int(r.get('tipoArticuloId')) if r.get('tipoArticuloId') not in (None, '') else None

        
        cantidad_folios = r.get('cantidad_folios')

        paquete_id = sql_execute_lastrowid(
            """
            INSERT INTO paquete
            (clave, valor, peso, alto, largo, precio_ruta, ancho,
            descripcion, direccion_destinatario, telefono_destinatario,
            num_documento_destinatario, sucursal_destino_id,
            tipo_documento_destinatario_id, tipo_empaqueid,
            contenido_paqueteid, tipo_recepcionid,
            salidaid, transaccion_encomienda_num_serie,
            qr_url, estado_pago, modalidad_pagoid,
            nombres_contacto_destinatario, apellidos_razon_destinatario,
            cantidad_folios)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s)
            """,
            (
                clave,
                valor,
                peso,
                alto,
                largo,
                tarifa,
                ancho,
                '',  # descripcion
                '',  # direccion_destinatario
                tel_dest,
                num_doc_dest,
                suc_dest_id,
                tipo_doc_dest,
                int(r.get('tipoEmpaqueId', 1)),
                contenido_paqueteid,
                int(r.get('tipoEntregaId', 1)),
                None,  # salidaid
                num_serie,
                None,  # qr_url
                estado_pago,
                modalidad_pago,
                nombre_contacto_destinatario,
                apellido_razon_destinatario,
                cantidad_folios  
            )
        )





        sql_execute(
            """
            INSERT INTO seguimiento
            (paquetetracking, detalle_estadoid, fecha, hora)
            VALUES (%s, %s, %s, %s)
            """,
            (
                paquete_id,
                1,
                date.today(),
                datetime.now().strftime('%H:%M:%S'),
            )
        )
        trackings.append(paquete_id)

    return comprobante_serie_final, trackings





def get_transaction_by_tracking(tracking):
    sql = '''
        SELECT 
            tc.nombre AS tipo_comprobante,
            te.comprobante_serie,
            te.num_serie,
            te.masivo,
            te.descripcion,
            te.monto_total,
            te.fecha,
            te.hora,
            te.tipo_comprobanteid,
            te.clienteid,
            c.nombre_siglas,
            c.apellidos_razon
        FROM paquete p
        INNER JOIN transaccion_encomienda te 
            ON te.num_serie = p.transaccion_encomienda_num_serie
        INNER JOIN cliente c 
            ON c.id = te.clienteid
        INNER JOIN tipo_comprobante tc 
            ON tc.id = te.tipo_comprobanteid
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

    return {
        'base_imponible': base_imponible,
        'igv': igv_valor,
        'total': monto_total
    }
