from controladores.bd import obtener_conexion

def obtener_colores():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql= "select id , nombre , valor from color"
            cursor.execute(sql)
            grupos = cursor.fetchall()
        conexion.close()
        return grupos
    except Exception as e:
        return e
    

def obtener_colores_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        query = "select id , nombre , valor from color where id = "+str(id)
        cursor.execute(query)
        usuario = cursor.fetchone()
    conexion.close()
    return usuario