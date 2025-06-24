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