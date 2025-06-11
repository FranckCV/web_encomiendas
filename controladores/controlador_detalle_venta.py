from controladores.bd import sql_execute

def registrar_detalle_venta(articuloid, num_serie, tipo_comprobanteid, cantidad):
    sql = '''
        INSERT INTO detalle_venta (articuloid, ventanum_serie, ventatipo_comprobanteid, cantidad)
        VALUES (%s, %s, %s, %s)
    '''
    sql_execute(sql, (articuloid, num_serie, tipo_comprobanteid, cantidad))
