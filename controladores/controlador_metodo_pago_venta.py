from controladores.bd import sql_execute,obtener_conexion

def registrar_metodo_pago_venta(num_serie, tipo_comprobante, metodo_pagoid):
    sql = '''
        INSERT INTO metodo_pago_venta (num_serie, tipo_comprobante, metodo_pagoid)
        VALUES (%s, %s, %s)
    '''
    sql_execute(sql, (num_serie, tipo_comprobante, metodo_pagoid))

def pagar_encomienda(num_serie, tipo_comprobante, metodo_pago, tracking):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = '''
                INSERT INTO metodo_pago_venta (num_serie, tipo_comprobante, metodo_pagoid)
                VALUES (%s, %s, %s)
            '''
            cursor.execute(sql, (num_serie, tipo_comprobante, metodo_pago))

            sql = '''
                UPDATE paquete
                SET estado_pago = 'C'
                WHERE tracking = %s
            '''
            cursor.execute(sql, (tracking,))
            
            
        conexion.commit()
    finally:
        conexion.close()
