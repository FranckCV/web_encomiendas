from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'paquete'

def exists_Activo():
    return exists_column_Activo(table_name)

def get_primary_key():
    return show_primary_key(table_name)

def get_report_estado_fecha():
    sql = f'''
        SELECT 
            paq.*, 
            con.nombre AS con_nombre, 
            est.nombre AS estado_nombre, 
            DATE_FORMAT(tra.fecha, '%d/%m/%Y') AS fecha_txt 
        FROM paquete paq 
        LEFT JOIN transaccion_encomienda tra 
        ON tra.num_serie = paq.transaccion_encomienda_num_serie 
        LEFT JOIN contenido_paquete con ON con.id = paq.contenido_paqueteid 
        LEFT JOIN ( 
        SELECT paquetetracking, MAX(detalle_estadoid) AS max_detalle_estadoid 
        FROM seguimiento GROUP BY paquetetracking ) ult_seg ON ult_seg.paquetetracking = paq.tracking 
        INNER JOIN detalle_estado det ON det.id = ult_seg.max_detalle_estadoid 
        LEFT JOIN estado_encomienda est ON est.id = det.estado_encomiendaid      

    '''
    
    columnas = {
        'tracking'      : ['Tracking', 0.5],
        'con_nombre'    : ['Contenido de paquete', 1.5],
        'estado_nombre' : ['Estado Actual de paquete', 1.5],
        'fecha_txt'     : ['Fecha de envio', 2],
    }
    
    filas = sql_select_fetchall(sql)
    
    return columnas, filas

def buscar_paquete(tracking, anio):
    sql = '''SELECT p.tracking, te.fecha 
             FROM paquete p
             INNER JOIN transaccion_encomienda te 
             ON p.transaccion_encomienda_num_serie = te.num_serie
             WHERE p.tracking = %s AND YEAR(te.fecha) = %s'''
    
    fila = sql_select_fetchone(sql, (tracking, anio))
    return fila['tracking'] if fila else None




def get_table_paquete_detalle(num_serie):
    sql = '''
        
         SELECT 
            p.tracking,
            p.valor,
            p.peso,
            p.estado_pago,
            p.qr_url,
            p.nombres_contacto_destinatario,
            p.apellidos_razon_destinatario,
            p.num_documento_destinatario,
            td.nombre AS tipo_documento,
            te.nombre AS tipo_empaque,
            cp.nombre AS contenido_paquete,
            tr.nombre AS tipo_recepcion,
            mp.nombre AS modalidad_pago,
            s.direccion AS direccion_destino,
            CONCAT(u.departamento, '/', u.provincia, '/', u.distrito) AS localidad,
            t.num_serie,
            t.fecha,
            t.hora,
            t.monto_total,
             
            CASE 
                WHEN p.ultimo_estado = 'PE' THEN 'Pendiente de entrega en sucursal de origen'
                WHEN p.ultimo_estado = 'EO' THEN 'En sucursal de origen'
                WHEN p.ultimo_estado = 'RD' THEN 'Entregado al destinatario'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'P' THEN 'Listo para salir'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'T' THEN 'En tránsito'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'C' THEN 'En destino'
                ELSE p.ultimo_estado
            END AS ultimo_estado
        
        FROM paquete p
        LEFT JOIN tipo_documento td ON td.id = p.tipo_documento_destinatario_id
        LEFT JOIN tipo_empaque te ON te.id = p.tipo_empaqueid
        LEFT JOIN contenido_paquete cp ON cp.id = p.contenido_paqueteid
        LEFT JOIN tipo_recepcion tr ON tr.id = p.tipo_recepcionid
        LEFT JOIN modalidad_pago mp ON mp.id = p.modalidad_pagoid
        LEFT JOIN sucursal s ON s.id = p.sucursal_destino_id
        LEFT JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        LEFT JOIN transaccion_encomienda t ON t.num_serie = p.transaccion_encomienda_num_serie
        LEFT JOIN salida sl ON sl.id = p.salidaid 
        WHERE t.num_serie = %s
        order by t.fecha desc;
    '''

    columnas = {
        'tracking': ['Tracking', 1],
        'valor': ['Valor S/.', 1],
        'peso': ['Peso (kg)', 1],
        'estado_pago': ['Pago', 0.7],
        'ultimo_estado':['Ultimo estado',4],
        'nombres_contacto_destinatario': ['Nombre destinatario', 2],
        'apellidos_razon_destinatario': ['Apellido/Razón', 2],
        'num_documento_destinatario': ['Doc. Identidad', 1.2],
        'tipo_documento': ['Tipo doc', 1],
        'tipo_empaque': ['Empaque', 1],
        'contenido_paquete': ['Contenido', 1.5],
        'tipo_recepcion': ['Recepción', 1.3],
        'modalidad_pago': ['Pago modalidad', 1.3],
        'direccion_destino': ['Dirección destino', 2.5],
        'localidad': ['Ubigeo destino', 2],
        'num_serie': ['N° Serie', 1],
        'fecha': ['Fecha envío', 1],
        'hora': ['Hora envío', 1],
        'monto_total': ['Total S/.', 1.2],
    }

    filas = sql_select_fetchall(sql,num_serie)

    return columnas, filas



def get_table():
    sql = '''
        SELECT 
            p.tracking,
            p.clave ,
            p.valor,
            p.peso,
            p.qr_url,
            p.alto ,
            p.cantidad_folios ,
            p.estado_pago ,
            CASE 
                WHEN p.estado_pago = 'P' THEN 'Pendiente'
                WHEN p.estado_pago = 'C' THEN 'Completado'
                ELSE p.estado_pago
            END AS estado_pago_nom ,
            p.largo ,
            p.ancho ,
            p.precio_ruta ,
            p.descripcion ,           
            p.nombres_contacto_destinatario,
            p.apellidos_razon_destinatario,
            p.direccion_destinatario ,
            p.telefono_destinatario ,
            p.num_documento_destinatario,
            p.sucursal_destino_id ,
            p.tipo_documento_destinatario_id ,
            p.tipo_empaqueid ,
            p.contenido_paqueteid,
            p.tipo_recepcionid ,
            p.salidaid ,
            p.transaccion_encomienda_num_serie ,
            p.modalidad_pagoid ,
            p.ultimo_estado  ,
            CASE 
                WHEN p.ultimo_estado = 'PE' THEN 'Pendiente de entrega en sucursal de origen'
                WHEN p.ultimo_estado = 'EO' THEN 'En sucursal de origen'
                WHEN p.ultimo_estado = 'RD' THEN 'Entregado al destinatario'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'P' THEN 'Listo para salir'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'T' THEN 'En tránsito'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'C' THEN 'En destino'
                ELSE p.ultimo_estado
            END AS ultimo_estado_nom      
        FROM paquete p
        LEFT JOIN salida sl ON sl.id = p.salidaid
        order by p.tracking desc;
        '''

    columnas = {
        'tracking': ['Tracking', 1],
        'transaccion_encomienda_num_serie': ['N° Serie Encomienda', 1],
        'valor': ['Valor (S/.)', 1],
        'peso': ['Peso (kg)', 1],
        'ultimo_estado_nom': ['Último estado', 1],
        'estado_pago_nom': ['Estado de pago', 3],
        'contenido_paqueteid': ['Contenido de paquete', 1],
        'apellidos_razon_destinatario': ['Dest. Apellidos / Razon Social', 1],
        'nombres_contacto_destinatario': ['Dest. Nombres', 1],
        'sucursal_destino_id': ['Sucursal de destino', 1],
        'precio_ruta': ['Precio de ruta', 1],
        'salidaid': ['Salida', 1],
        'tipo_recepcionid': ['Tipo de recepción', 1],
    }

    filas = sql_select_fetchall(sql)

    return columnas, filas



def get_table_pk_foreign(pk_foreign):
    sql = '''
        
            SELECT 
            p.tracking,
            p.valor,
            p.peso,
                        CASE 
                    WHEN p.estado_pago = 'P' THEN 'Pendiente'
                    WHEN p.estado_pago = 'C' THEN 'Completado'
                    ELSE p.estado_pago
                END AS estado_pago,  
            p.qr_url,
            p.nombres_contacto_destinatario,
            p.apellidos_razon_destinatario,
            p.num_documento_destinatario,
            td.nombre AS tipo_documento,
            te.nombre AS tipo_empaque,
            cp.nombre AS contenido_paquete,
            tr.nombre AS tipo_recepcion,
            mp.nombre AS modalidad_pago,
            s.direccion AS direccion_destino,
            CONCAT(u.departamento, '/', u.provincia, '/', u.distrito) AS localidad,
            t.num_serie,
            t.fecha,
            t.hora,
            t.monto_total,

             
            CASE 
                WHEN p.ultimo_estado = 'PE' THEN 'Pendiente de entrega en sucursal de origen'
                WHEN p.ultimo_estado = 'EO' THEN 'En sucursal de origen'
                WHEN p.ultimo_estado = 'RD' THEN 'Entregado al destinatario'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'P' THEN 'Listo para salir'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'T' THEN 'En tránsito'
                WHEN p.salidaid IS NOT NULL AND sl.estado = 'C' THEN 'En destino'
                ELSE p.ultimo_estado
            END AS ultimo_estado
        
        FROM paquete p
        LEFT JOIN tipo_documento td ON td.id = p.tipo_documento_destinatario_id
        LEFT JOIN tipo_empaque te ON te.id = p.tipo_empaqueid
        LEFT JOIN contenido_paquete cp ON cp.id = p.contenido_paqueteid
        LEFT JOIN tipo_recepcion tr ON tr.id = p.tipo_recepcionid
        LEFT JOIN modalidad_pago mp ON mp.id = p.modalidad_pagoid
        LEFT JOIN sucursal s ON s.id = p.sucursal_destino_id
        LEFT JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        LEFT JOIN transaccion_encomienda t ON t.num_serie = p.transaccion_encomienda_num_serie
        LEFT JOIN salida sl ON sl.id = p.salidaid 
        WHERE t.num_serie = %s
        order by t.fecha desc;

    '''

    columnas = {
        'tracking': ['Tracking', 1],
        'valor': ['Valor S/.', 1],
        'peso': ['Peso (kg)', 1],
        'estado_pago': ['Pago', 1],
        'ultimo_estado':['Ultimo estado',3.5],
        'nombres_contacto_destinatario': ['Nombre destinatario', 2],
        'apellidos_razon_destinatario': ['Apellido/Razón', 2],
        'num_documento_destinatario': ['Doc. Identidad', 1.2],
        'tipo_documento': ['Tipo Doc.', 1],
        'tipo_empaque': ['Empaque', 1],
        'contenido_paquete': ['Contenido', 1.5],
        'tipo_recepcion': ['Recepción', 1.3],
        'modalidad_pago': ['Pago modalidad', 1.3],
        # 'direccion_destino': ['Dirección destino', 5],
        'localidad': ['Ubigeo destino', 2],
        'num_serie': ['N° Serie', 1],
        'fecha': ['Fecha envío', 1],
        'hora': ['Hora envío', 1],
        'monto_total': ['Total S/.', 1.2],
    }

    filas = sql_select_fetchall(sql,(pk_foreign,))

    return columnas, filas

def get_contenido(tracking):
    sql = '''
        SELECT 
    tp.nombre,
    CASE 
        WHEN tp.nombre = 'Caja' THEN c.nombre
        WHEN tp.nombre = 'Sobre' THEN p.cantidad_folios
        ELSE NULL
    END AS detalle_empaque
FROM paquete p
INNER JOIN tipo_empaque tp ON tp.id = p.tipo_empaqueid
INNER JOIN contenido_paquete c ON c.id = p.contenido_paqueteid
where p.tracking = %s
    '''
    fila = sql_select_fetchone(sql,(tracking,))
    return fila


def get_paquete_by_tracking(tracking):
    sql = '''
        SELECT 
            p.clave,
            p.tracking,
                        CASE 
                    WHEN p.estado_pago = 'P' THEN 'Pendiente'
                    WHEN p.estado_pago = 'C' THEN 'Completado'
                    ELSE p.estado_pago
                END AS estado_pago,  
            so.direccion AS sucursal_origen,
            uo.distrito AS distrito_origen,
            uo.provincia AS provincia_origen,
            uo.departamento AS departamento_origen,
            sd.abreviatura,
            sd.direccion AS sucursal_destino,
            ud.distrito AS distrito_destino,
            ud.provincia AS provincia_destino,
            ud.departamento AS departamento_destino,
            te.nombre AS tipo_empaque,
            cp.nombre AS contenido_paquete
        FROM paquete p
        inner join transaccion_encomienda tre on tre.num_serie = p.transaccion_encomienda_num_serie
        INNER JOIN sucursal so ON so.id = tre.id_sucursal_origen
        INNER JOIN ubigeo uo ON uo.codigo = so.ubigeocodigo
        INNER JOIN sucursal sd ON sd.id = p.sucursal_destino_id
        INNER JOIN ubigeo ud ON ud.codigo = sd.ubigeocodigo
        LEFT JOIN tipo_empaque te ON te.id = p.tipo_empaqueid
        LEFT JOIN contenido_paquete cp ON cp.id = p.contenido_paqueteid
        WHERE p.tracking = %s
    '''
    return sql_select_fetchone(sql, (tracking,))


def listar_paquetes_por_sucursal_escalas():
    sql = '''  
          SELECT 
            p.tracking,                  
            p.peso,                     
            te.id_sucursal_origen,       
            p.sucursal_destino_id         
        FROM paquete p 
        INNER JOIN transaccion_encomienda te 
            ON te.num_serie = p.transaccion_encomienda_num_serie
        WHERE p.salidaid is null and p.estado_pago  = 'C' and p.ultimo_estado='EO'
        ORDER BY p.tracking;

    '''
    filas = sql_select_fetchall(sql)
    return filas

def obtener_datos_guia_remision(transaccion_id):
    sql = """
        SELECT 
            -- Emisor
            e.ruc AS emisor_ruc,
            e.nombre AS emisor_razon_social,
            s_origen.direccion AS emisor_direccion,

            -- Destinatario
            p.num_documento_destinatario AS destinatario_doc,
            p.nombres_contacto_destinatario AS destinatario_nombres,
            p.apellidos_razon_destinatario AS destinatario_apellidos,
            p.direccion_destinatario AS destinatario_direccion,

            -- Transporte
            sa.fecha AS fecha_inicio_traslado,
            suc_origen.direccion AS punto_partida,
            suc_destino.direccion AS punto_llegada,
            u.placa AS vehiculo_placa,
            emp.nombre AS conductor_nombre,
            emp.n_documento AS conductor_dni,

            -- Bienes
            p.descripcion AS descripcion,
            te.unidad_medida AS unidad_medida,
            p.peso AS peso,
            1 AS cantidad,
            conpa.nombre as contenido_paquete

        FROM transaccion_encomienda tec
        JOIN paquete p ON p.transaccion_encomienda_num_serie = tec.num_serie
        JOIN salida sa ON sa.id = p.salidaid
        JOIN unidad u ON u.id = sa.unidadid
        JOIN empleado emp ON emp.id = sa.conductor_principal
        JOIN sucursal s_origen ON s_origen.id = tec.id_sucursal_origen
        JOIN sucursal suc_origen ON suc_origen.id = sa.origen_inicio_id
        JOIN sucursal suc_destino ON suc_destino.id = sa.destino_final_id
        JOIN empresa e ON e.actual = 1
        JOIN tipo_empaque te ON te.id = p.tipo_empaqueid
        JOIN contenido_paquete conpa ON p.contenido_paqueteid = conpa.id
        WHERE tec.num_serie = %s
        LIMIT 1;
    """
    fila = sql_select_fetchone(sql, (transaccion_id,))
    if not fila:
        return None

    return {
        "emisor": {
            "ruc": fila["emisor_ruc"],
            "razon_social": fila["emisor_razon_social"],
            "direccion": fila["emisor_direccion"],
        },
        "destinatario": {
            "ruc_dni": fila["destinatario_doc"],
            "nombre": f"{fila['destinatario_nombres']} {fila['destinatario_apellidos']}",
            "direccion": fila["destinatario_direccion"],
        },
        "transporte": {
            "fecha_inicio": fila["fecha_inicio_traslado"].strftime("%Y-%m-%d"),
            "punto_partida": fila["punto_partida"],
            "punto_llegada": fila["punto_llegada"],
            "placa": fila["vehiculo_placa"],
            "conductor": fila["conductor_nombre"],
            "dni_conductor": fila["conductor_dni"],
        },
        "bienes": [{
            "descripcion": fila["descripcion"] if fila['descripcion'] != '' or fila['descripcion'] is None else fila['contenido_paquete'],
            "unidad": fila["unidad_medida"],
            "cantidad": fila["cantidad"],
            "peso": fila["peso"]
        }]
    }


def get_num_serie_por_tracking(tracking):
    sql = """
        SELECT transaccion_encomienda_num_serie 
        FROM paquete 
        WHERE tracking = %s
        LIMIT 1
    """
    fila = sql_select_fetchone(sql, (tracking,))
    return fila['transaccion_encomienda_num_serie'] if fila else None




#############3
def get_paquetes_por_ruta_sucursales(sucursal_origen_id, sucursal_destino_id):
    """
    Obtiene los tracking de los paquetes que serán enviados desde una sucursal origen
    hacia una sucursal destino específica.
    
    Args:
        sucursal_origen_id (int): ID de la sucursal origen
        sucursal_destino_id (int): ID de la sucursal destino
    
    Returns:
        list: Lista de tracking numbers de los paquetes que coinciden con la ruta
    """
    sql = """
        SELECT p.tracking
        FROM paquete p
        INNER JOIN salida s ON p.salidaid = s.id
        WHERE (s.origen_inicio_id = %s OR True) 
        AND p.sucursal_destino_id = %s
    """
    
    filas = sql_select_fetchall(sql, (sucursal_origen_id, sucursal_destino_id))
    return [fila['tracking'] for fila in filas] if filas else []


# Versión alternativa si necesitas más información de los paquetes
def get_paquetes_detallados_por_ruta(sucursal_origen_id, sucursal_destino_id):
    """
    Obtiene información detallada de los paquetes que serán enviados desde una sucursal origen
    hacia una sucursal destino específica.
    
    Args:
        sucursal_origen_id (int): ID de la sucursal origen
        sucursal_destino_id (int): ID de la sucursal destino
    
    Returns:
        list: Lista de diccionarios con información de los paquetes
    """
    sql = """
        SELECT p.tracking, 
               p.valor, 
               p.peso, 
               p.nombres_contacto_destinatario,
               p.apellidos_razon_destinatario,
               p.telefono_destinatario,
               s.fecha as fecha_salida,
               s.hora as hora_salida
        FROM paquete p
        INNER JOIN salida s ON p.salidaid = s.id
        WHERE s.origen_inicio_id = %s 
        AND p.sucursal_destino_id = %s
        ORDER BY s.fecha, s.hora
    """
    
    filas = sql_select_fetchall(sql, (sucursal_origen_id, sucursal_destino_id))
    return filas if filas else []

def get_data_pay(tracking):
    sql = '''
    SELECT 
        CASE 
            WHEN p.estado_pago = 'P' THEN 'Pendiente'
            WHEN p.estado_pago = 'C' THEN 'Completado'
            ELSE p.estado_pago
        END AS nombre_estado_pago,
        
        p.estado_pago,
        
        p.ultimo_estado,
        
        CASE 
            WHEN p.ultimo_estado = 'PE' THEN 'Pendiente de entrega en sucursal de origen'
            WHEN p.ultimo_estado = 'EO' THEN 'En sucursal de origen'
            WHEN p.ultimo_estado = 'RD' THEN 'Entregado al destinatario'
            WHEN p.salidaid IS NOT NULL AND sl.estado = 'P' THEN 'Listo para salir'
            WHEN p.salidaid IS NOT NULL AND sl.estado = 'T' THEN 'En tránsito'
            WHEN p.salidaid IS NOT NULL AND sl.estado = 'C' THEN 'En destino'
            ELSE p.ultimo_estado
        END AS nombre_estado
        
    FROM paquete p
    LEFT JOIN salida sl ON sl.id = p.salidaid
    WHERE p.tracking = %s
    '''
    
    fila = sql_select_fetchone(sql, (tracking,))
    
    return fila


def verificar_clave_seguridad(tracking, security_code):
    sql = '''
            SELECT clave FROM paquete WHERE tracking = %s
    '''
    fila = sql_select_fetchone(sql, (tracking,))
    
    if fila is None:
        return False

    if 'clave' in fila and fila['clave'] == security_code:
        return True
    
    if fila[0] == security_code:
        return True

    return False


def actualizar_estado_entrega_sucursal(tracking, tipo_comprobante):
    sql_update = '''
        UPDATE paquete
        SET ultimo_estado = 'EO'
        WHERE tracking = %s
    '''
    try:
        sql_execute(sql_update, (tracking,))

        for estado_id in range(2, 7):  # del 2 al 6 inclusive
            sql_insert = '''
                INSERT INTO seguimiento (paquetetracking, detalle_estadoid, tipo_comprobanteid, fecha, hora)
                VALUES (%s, %s, %s, NOW(), NOW())
            '''

            tipo = tipo_comprobante if estado_id == 2 else None

            sql_execute(sql_insert, (tracking, estado_id, tipo))

        return True

    except Exception as e:
        print(f"Error al actualizar estado: {e}")
        return False



def actualizar_estado_entrega_destinatario(tracking, tipo_comprobante=None):
    sql_update = '''
        UPDATE paquete 
        SET ultimo_estado = 'RD' 
        WHERE tracking = %s
    '''
    try:
        sql_execute(sql_update, (tracking,))
        print(f"Estado 'RD' actualizado para tracking: {tracking}")

        sql_insert_19 = '''
            INSERT INTO seguimiento (paquetetracking, detalle_estadoid, tipo_comprobanteid, fecha, hora)
            VALUES (%s, 19, %s, NOW(), NOW())
        '''
        sql_execute(sql_insert_19, (tracking, tipo_comprobante))
        print(f"Insertado estado 19 con tipo_comprobante = {tipo_comprobante}")

        sql_insert_21 = '''
            INSERT INTO seguimiento (paquetetracking, detalle_estadoid, tipo_comprobanteid, fecha, hora)
            VALUES (%s, 21, NULL, NOW(), NOW())
        '''
        sql_execute(sql_insert_21, (tracking,))
        print("Insertado estado 21 sin tipo_comprobante")

        return True

    except Exception as e:
        print(f"Error al actualizar estado: {e}")
        return False


def obtener_ultimo_estado(tracking):
    sql = '''
        select ultimo_estado from paquete where tracking = %s
    '''
    fila = sql_select_fetchone(sql,(tracking))
    return fila

