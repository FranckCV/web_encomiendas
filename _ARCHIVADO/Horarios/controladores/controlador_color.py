from controladores.bd import obtener_conexion

def obtener_color():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            select 
                col.id,
                col.nombre,
                col.color_fondo,
                col.color_texto
            from color col 
            order by col.id 
        '''
        cursor.execute(sql)
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos


def obtener_listado_colores():
    conexion = obtener_conexion()
    # try:
    with conexion.cursor() as cursor:
        sql = '''
            select 
                col.id,
                col.nombre,
                col.color_fondo,
                col.color_texto
            from color col 
            order by col.id
        '''
        cursor.execute(sql)
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos


def insertar_color(nombre,fondo,texto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO color(nombre,color_fondo,color_texto) VALUES (%s, %s ,%s)",
            (nombre,fondo,texto)
            )
    conexion.commit()
    conexion.close()

