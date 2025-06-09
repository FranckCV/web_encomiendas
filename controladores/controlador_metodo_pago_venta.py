from controladores.bd import sql_execute

def registrar_metodo_pago_venta(num_serie, tipo_comprobante, metodo_pagoid):
    sql = '''
        INSERT INTO metodo_pago_venta (num_serie, tipo_comprobante, metodo_pagoid)
        VALUES (%s, %s, %s)
    '''
    sql_execute(sql, (num_serie, tipo_comprobante, metodo_pagoid))
