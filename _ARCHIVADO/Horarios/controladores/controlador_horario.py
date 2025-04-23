from controladores.bd import obtener_conexion

def obtener_horarios():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            select 
                hor.id, 
                hor.dia, 
                hor.h_inicio, 
                hor.h_final, 
                gr.denominacion, 
                gr.semestrecodigo, 
                cur.nombre, 
                cur.abreviacion, 
                cur.ciclo,
                col.color_fondo,
                col.color_texto,
                doc.nombres, 
                doc.apellidos,
                gr.id
            from grupo gr 
            inner join docente doc on doc.id = gr.docenteid 
            inner join curso cur on cur.id = gr.cursoid 
            inner join horario hor on hor.grupoid = gr.id
            inner join color col on col.id = cur.colorid
            order by gr.semestrecodigo
        '''
        cursor.execute(sql)
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos


def obtener_horario_semestre(semestre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            select 
                hor.id, 
                hor.dia, 
                hor.h_inicio, 
                hor.h_final, 
                gr.denominacion, 
                gr.semestrecodigo, 
                cur.nombre, 
                cur.abreviacion, 
                cur.ciclo,
                col.color_fondo,
                col.color_texto,
                doc.nombres, 
                doc.apellidos,
                gr.id
            from grupo gr 
            inner join docente doc on doc.id = gr.docenteid 
            inner join curso cur on cur.id = gr.cursoid 
            inner join horario hor on hor.grupoid = gr.id
            inner join color col on col.id = cur.colorid
            where gr.semestrecodigo = %s
        '''
        cursor.execute(sql,semestre)
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos


def obtener_horario_matricula(matricula):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            select 
                hor.id, 
                hor.dia, 
                hor.h_inicio, 
                hor.h_final, 
                gr.denominacion, 
                gr.semestrecodigo, 
                cur.nombre, 
                cur.abreviacion, 
                cur.ciclo,
                col.color_fondo,
                col.color_texto,
                doc.nombres, 
                doc.apellidos,
                gr.id
            from grupo gr 
            left join docente doc on doc.id = gr.docenteid 
            left join curso cur on cur.id = gr.cursoid 
            left join horario hor on hor.grupoid = gr.id
            left join color col on col.id = cur.colorid
            left join detalles_matricula det on det.grupoid = gr.id
            left join matricula mat on mat.id = det.matriculaid
            where mat.id = %s
        '''
        cursor.execute(sql,matricula)
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos





