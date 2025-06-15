from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
import uuid
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
import logging
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

    # ——————————————————————————————
    # 2) Cabecera de transacción
    num_serie = str(uuid.uuid4())
    masivo    = 1 if registros and registros[0].get('modo') == 'masivo' else 0

    # Calculamos el total usando el campo 'tarifa' de cada registro
    monto_total = sum(Decimal(r.get('tarifa', 0)) for r in registros)\
                  .quantize(Decimal('0.01'), ROUND_HALF_UP)

    # Puedes poner aquí la descripción que quieras. 
    # Por ejemplo: tipo de envío o simplemente cadena vacía.
    descripcion     = f"Envío {'masivo' if masivo else 'individual'} #{num_serie}"
    direccion_recojo = ''  # o tomarla de registros[0]['origen']['direccion'] si la tienes

    sql_execute(
        """
        INSERT INTO transaccion_encomienda
        (num_serie, masivo, descripcion, monto_total, recojo_casa,
        id_sucursal_origen, fecha, hora,
        direccion_recojo, clienteid, tipo_comprobanteid)
        VALUES (%s, %s, %s, %s, 0, %s, %s, %s, %s, %s, %s)
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
            tipo_comprobante
        )
    )


    # ——————————————————————————————
    # 3) Detalle de paquetes
    for idx, r in enumerate(registros):
        try:
            clave  = r['clave']
            valor  = float(r.get('valorEnvio') or 0)
            peso   = float(r.get('peso') or 0)
            alto   = float(r.get('alto') or 0)
            largo  = float(r.get('largo') or 0)
            tarifa = float(r.get('tarifa') or 0)
            ancho  = float(r.get('ancho') or 0)
        except ValueError as ve:
            current_app.logger.error(f"[Registro {idx}] Error conversión: {ve}")
            current_app.logger.error(f"[Registro {idx}] Datos: {r!r}")
            raise
        
                
        dest = r['destinatario']
        tipo_doc_dest = int(dest.get('tipo_doc_destinatario', 1))
        num_doc_dest  = dest.get('num_doc_destinatario', '')
        tel_dest      = dest.get('num_tel_destinatario', '')
        nombre_dest   = dest.get('nombre_destinatario', '')

        suc_dest_id = int(r['destino']['sucursal_destino'])
        estado_pago = r.get('estado_pago', 'P') 

        # Preparar contenido_paqueteid para permitir NULL
        raw_contenido = r.get('tipoArticuloId')
        if raw_contenido not in (None, ''):
            contenido_paqueteid = int(raw_contenido)
        else:
            contenido_paqueteid = None  # se insertará como NULL

        paquete_id = sql_execute_lastrowid(
            """
            INSERT INTO paquete
            (clave, valor, peso, alto, largo, precio_ruta, ancho,
            descripcion, direccion_destinatario, telefono_destinatario,
            num_documento_destinatario, sucursal_destino_id,
            tipo_documento_destinatario_id, tipo_empaqueid, 
            contenido_paqueteid, tipo_recepcionid,
            salidaid, transaccion_encomienda_num_serie,
            qr_url,estado_pago )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                clave,
                valor,
                peso,
                alto,
                largo,
                tarifa,
                ancho,
                nombre_dest,         # descripción del paquete
                '',                  # dirección_destinatario (vacío → NULL en la BDD)
                tel_dest,
                num_doc_dest,
                suc_dest_id,
                tipo_doc_dest,
                int(r.get('tipoEmpaqueId', 1)),
                contenido_paqueteid,       # None → SQL NULL
                int(r.get('tipoEntregaId',1) ),
                None,               # salidaid → SQL NULL
                num_serie,
                None,
                estado_pago
            )
        )
        
        sql_execute(
            """
            INSERT INTO seguimiento
            (paquetetracking, detalle_estadoid, fecha, hora, tipo_comprobanteid)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                paquete_id, 
                1,         
                date.today(),
                datetime.now().strftime('%H:%M:%S'),
                None
            )
        )

        
        return num_serie