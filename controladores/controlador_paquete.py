from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'paquete'

def exists_Activo():
    return exists_column_Activo(table_name)

def get_primary_key():
    return show_primary_key(table_name)

def get_report_test():
    sql = f'''
        SELECT 
            paq.*, 
            con.nombre AS con_nombre, 
            est.nombre AS estado_nombre, 
            DATE_FORMAT(tra.fecha, '%d/%m/%Y') AS fecha_txt 
        FROM paquete paq 
        LEFT JOIN transaccion_encomienda tra 
        ON tra.num_serie = paq.transaccion_encomienda_num_serie 
        INNER JOIN contenido_paquete con ON con.id = paq.contenido_paqueteid 
        INNER JOIN ( 
        SELECT paquetetracking, MAX(detalle_estadoid) AS max_detalle_estadoid 
        FROM seguimiento GROUP BY paquetetracking ) ult_seg ON ult_seg.paquetetracking = paq.tracking 
        INNER JOIN detalle_estado det ON det.id = ult_seg.max_detalle_estadoid 
        INNER JOIN estado_encomienda est ON est.id = det.estado_encomiendaid
        

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
          t.monto_total

        FROM paquete p
        LEFT JOIN tipo_documento td ON td.id = p.tipo_documento_destinatario_id
        LEFT JOIN tipo_empaque te ON te.id = p.tipo_empaqueid
        LEFT JOIN contenido_paquete cp ON cp.id = p.contenido_paqueteid
        LEFT JOIN tipo_recepcion tr ON tr.id = p.tipo_recepcionid
        LEFT JOIN modalidad_pago mp ON mp.id = p.modalidad_pagoid
        LEFT JOIN sucursal s ON s.id = p.sucursal_destino_id
        LEFT JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        LEFT JOIN transaccion_encomienda t ON t.num_serie = p.transaccion_encomienda_num_serie

        WHERE t.num_serie = %s
    '''

    columnas = {
        'tracking': ['Tracking', 1],
        'valor': ['Valor S/.', 1],
        'peso': ['Peso (kg)', 1],
        'estado_pago': ['Pago', 0.7],
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
          p.valor,
          p.peso,
          CASE 
        WHEN p.estado_pago = 'P' THEN 'Pendiente'
        WHEN p.estado_pago = 'C' THEN 'Pagado'
        ELSE 'Desconocido'
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
          t.monto_total

        FROM paquete p
        LEFT JOIN tipo_documento td ON td.id = p.tipo_documento_destinatario_id
        LEFT JOIN tipo_empaque te ON te.id = p.tipo_empaqueid
        LEFT JOIN contenido_paquete cp ON cp.id = p.contenido_paqueteid
        LEFT JOIN tipo_recepcion tr ON tr.id = p.tipo_recepcionid
        LEFT JOIN modalidad_pago mp ON mp.id = p.modalidad_pagoid
        LEFT JOIN sucursal s ON s.id = p.sucursal_destino_id
        LEFT JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        LEFT JOIN transaccion_encomienda t ON t.num_serie = p.transaccion_encomienda_num_serie

    '''

    columnas = {
        'tracking': ['Tracking', 1],
        'valor': ['Valor S/.', 1],
        'peso': ['Peso (kg)', 1],
        'estado_pago': ['Pago', 0.7],
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
        WHEN p.estado_pago = 'C' THEN 'Pagado'
        ELSE 'Desconocido'
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
          t.monto_total

        FROM paquete p
        LEFT JOIN tipo_documento td ON td.id = p.tipo_documento_destinatario_id
        LEFT JOIN tipo_empaque te ON te.id = p.tipo_empaqueid
        LEFT JOIN contenido_paquete cp ON cp.id = p.contenido_paqueteid
        LEFT JOIN tipo_recepcion tr ON tr.id = p.tipo_recepcionid
        LEFT JOIN modalidad_pago mp ON mp.id = p.modalidad_pagoid
        LEFT JOIN sucursal s ON s.id = p.sucursal_destino_id
        LEFT JOIN ubigeo u ON u.codigo = s.ubigeocodigo
        LEFT JOIN transaccion_encomienda t ON t.num_serie = p.transaccion_encomienda_num_serie

        WHERE t.num_serie = %s
    '''

    columnas = {
        'tracking': ['Tracking', 1],
        'valor': ['Valor S/.', 1],
        'peso': ['Peso (kg)', 1],
        'estado_pago': ['Pago', 0.7],
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
            p.estado_pago,
            -- Origen
            so.direccion AS sucursal_origen,
            uo.distrito AS distrito_origen,
            uo.provincia AS provincia_origen,
            uo.departamento AS departamento_origen,
            -- Destino
            sd.abreviatura,
            sd.direccion AS sucursal_destino,
            ud.distrito AS distrito_destino,
            ud.provincia AS provincia_destino,
            ud.departamento AS departamento_destino,
            -- Empaque
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
        WHERE p.salidaid is null   
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
            p.descripcion AS descripcion_item,
            te.unidad_medida AS unidad_medida,
            p.peso AS peso,
            1 AS cantidad

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
        WHERE tec.num_serie = %s
        LIMIT 1
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
            "descripcion": fila["descripcion_item"],
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