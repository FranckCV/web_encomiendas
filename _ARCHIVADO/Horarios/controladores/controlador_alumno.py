from controladores.bd import obtener_conexion

def obtener_prerrequisitos(alu_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT
                cur.*,
                col.*
            FROM
                curso cur
            LEFT JOIN color col ON col.id = cur.colorid
            LEFT JOIN curso_curso ccc ON ccc.cursoid = cur.id
            WHERE 
                (
                    ccc.cursoid_pre IS NULL
                    OR
                    cur.id IN (
                        SELECT 
                            ccc2.cursoid
                        FROM
                            curso_curso ccc2
                        WHERE 
                            ccc2.cursoid_pre IN (
                                SELECT 
                                    gr.cursoid
                                FROM 
                                    grupo gr
                                LEFT JOIN detalles_matricula det ON det.grupoid = gr.id
                                LEFT JOIN matricula mat ON mat.id = det.matriculaid
                                WHERE 
                                    mat.alumnoid = %s
                            )
                        GROUP BY 
                            ccc2.cursoid
                        HAVING 
                            COUNT(ccc2.cursoid_pre) = (
                                SELECT COUNT(*)
                                FROM curso_curso cc_all
                                WHERE cc_all.cursoid = ccc2.cursoid
                            )
                    )
                )
                AND 
                cur.id NOT IN (
                    SELECT 
                        gr.cursoid
                    FROM 
                        grupo gr
                    LEFT JOIN detalles_matricula det ON det.grupoid = gr.id
                    LEFT JOIN matricula mat ON mat.id = det.matriculaid
                    WHERE 
                        mat.alumnoid = %s
                )
                group by cur.id
            ORDER BY 
                cur.ciclo ASC , cur.nombre ;
        '''
        cursor.execute(sql,(alu_id,alu_id))
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos


# def obtener_prerrequisitos(alu_id):
#     conexion = obtener_conexion()
#     with conexion.cursor() as cursor:
#         sql = '''
#             WITH CursosMatriculados AS (
#                 SELECT DISTINCT g.cursoid
#                 FROM detalles_matricula dm
#                 INNER JOIN grupo g ON dm.grupoid = g.id
#                 INNER JOIN matricula m ON dm.matriculaid = m.id
#                 WHERE m.alumnoid = '''+str(alu_id)+'''
#             ),
#             PrerrequisitosAprobados AS (
#                 SELECT DISTINCT cc.cursoid
#                 FROM curso_curso cc
#                 INNER JOIN grupo g_pre ON cc.cursoid_pre = g_pre.cursoid
#                 INNER JOIN detalles_matricula dm ON dm.grupoid = g_pre.id
#                 INNER JOIN matricula m ON dm.matriculaid = m.id
#                 WHERE m.alumnoid = '''+str(alu_id)+'''
#             ),
#             CursosDisponibles AS (
#                 SELECT c.id AS curso_id, c.nombre, c.ciclo , col.color_fondo , col.color_texto
#                 FROM curso c
#                 left join color col on col.id = c.colorid
#                 LEFT JOIN curso_curso cc ON c.id = cc.cursoid
#                 WHERE cc.cursoid_pre IS NULL
#                 OR c.id IN (
#                     SELECT cursoid
#                     FROM PrerrequisitosAprobados
#                     GROUP BY cursoid
#                     HAVING COUNT(cc.cursoid_pre) = COUNT(DISTINCT cc.cursoid_pre)
#                 )
#             )
#             SELECT cd.*
#             FROM CursosDisponibles cd
#             WHERE cd.curso_id NOT IN (SELECT cursoid FROM CursosMatriculados)
#             ORDER BY cd.ciclo, cd.nombre
#         '''
#         cursor.execute(sql)
#         elementos = cursor.fetchall() 
#     conexion.close()
#     return elementos
