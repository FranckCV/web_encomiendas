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
    sql= f'''
        SELECT
        s.id, 
    CONCAT(e.nombre, ' ', e.apellidos) AS nom_conductor,
    u.placa,
    ub.departamento AS destino,
    s.fecha,
    s.hora,
    u.capacidad,
    CASE s.estado
        WHEN 'P' THEN 'Pendiente (origen sucursal / domicilio)'
        WHEN 'E' THEN 'En curso (en ruta)'
        WHEN 'C' THEN 'Completada (destino sucursal / domicilio)'
        WHEN 'X' THEN 'Cancelada'
        ELSE 'Estado desconocido'
    END AS estado
FROM salida s
INNER JOIN unidad u ON u.id = s.unidadid
INNER JOIN empleado e ON e.id = s.conductor_principal
INNER JOIN sucursal su ON su.id = s.destino_final
INNER JOIN ubigeo ub ON ub.codigo = su.ubigeocodigo
    '''
    columnas = {
        'id': ['ID' , 0.5 ] , 
        'nom_conductor' : ['Conductor' , 1 ] , 
        'placa' : ['Placa' , 1] , 
        'destino' : ['Destino' , 3.5] , 
        'fecha' : ['Fecha' , 1.2] , 
        'hora' : ['Hora' , 1] , 
        'capacidad' : ['Capacidad' , 1.5] , 
        'estado' : ['Estado' , 3.5] ,

        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas



# def insert_rows(cliente:dict):
#     try:
        
#     except Exception as e:
        

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
         id_sucursal_origen, estado_pago, fecha, hora,
         direccion_recojo, clienteid, tipo_comprobanteid)
        VALUES (%s,%s,%s,%s,0,%s,'P',%s,%s,%s,%s,%s)
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
        
        
        qr_token = str(uuid.uuid4())
        
        dest = r['destinatario']
        tipo_doc_dest = int(dest.get('tipo_doc_destinatario', 1))
        num_doc_dest  = dest.get('num_doc_destinatario', '')
        tel_dest      = dest.get('num_tel_destinatario', '')
        nombre_dest   = dest.get('nombre_destinatario', '')

        suc_dest_id = int(r['destino']['sucursal_destino'])

        # Preparar contenido_paqueteid para permitir NULL
        raw_contenido = r.get('tipoArticuloId')
        if raw_contenido not in (None, ''):
            contenido_paqueteid = int(raw_contenido)
        else:
            contenido_paqueteid = None  # se insertará como NULL

        sql_execute(
            """
            INSERT INTO paquete
            (clave, valor, peso, alto, largo, precio_ruta, ancho,
            descripcion, direccion_destinatario, telefono_destinatario,
            num_documento_destinatario, sucursal_destino_id,
            tipo_documento_destinatario_id, tipo_empaqueid,
            contenido_paqueteid, tipo_recepcionid,
            salidaid, transaccion_encomienda_num_serie,
            qr_token, qr_image)
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,NULL,NULL)
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
            )
        )
        return num_serie