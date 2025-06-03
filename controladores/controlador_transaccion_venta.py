from controladores.bd import sql_execute_lastrowid

def registrar_transaccion(tipo_comprobanteid, monto_total, clienteid):
    sql = '''
        INSERT INTO transaccion_venta (tipo_comprobanteid, monto_total, fecha, hora, clienteid)
        VALUES (%s, %s, CURDATE(), CURTIME(), %s)
    '''
    return sql_execute_lastrowid(sql, (tipo_comprobanteid, monto_total, clienteid))
