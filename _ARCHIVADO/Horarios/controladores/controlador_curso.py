from controladores.bd import obtener_conexion

def obtener_cursos():
    conexion = obtener_conexion()
    # try:
    with conexion.cursor() as cursor:
        sql = '''
            select 
                cur.id,
                cur.nombre,
                cur.abreviacion,
                cur.ciclo,
                col.color_fondo,
                col.color_texto,
                pre.id,
                pre.nombre,
                pre.abreviacion,
                pre.ciclo,
                clr.color_fondo,
                clr.color_texto
            from curso cur
            left join color col on col.id = cur.colorid
            left join curso_curso cuc on cur.id = cuc.cursoid
            left join curso pre on pre.id = cuc.cursoid_pre
            left join color clr on clr.id = pre.colorid
            order by cur.ciclo , cur.nombre, pre.ciclo  , pre.nombre 
        '''
        cursor.execute(sql)
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos
    # except Exception as e:
    #     return e

def obtener_listado_cursos():
    conexion = obtener_conexion()
    # try:
    with conexion.cursor() as cursor:
        sql = '''
            select 
                cur.ciclo,
                cur.id,
                cur.nombre,
                cur.abreviacion,
                cur.creditos,
                col.color_fondo,
                col.color_texto
            from curso cur
            left join color col on col.id = cur.colorid
            order by cur.ciclo , cur.nombre
        '''
        cursor.execute(sql)
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos
    # except Exception as e:
    #     return e

def insertar_curso(nombre,abrev,cred,ciclo,colorid):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO curso(nombre,abreviacion,creditos,ciclo,colorid) VALUES (%s, %s,%s,%s,%s)",
            (nombre,abrev,cred,ciclo,colorid)
            )
    conexion.commit()
    conexion.close()

