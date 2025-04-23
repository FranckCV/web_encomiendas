from controladores.bd import obtener_conexion

def obtener_matriculas_alumno(alu_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = '''
            SELECT 
                mat.id,
                mat.semestrecodigo
            FROM alumno alu
            left join matricula mat on mat.alumnoid = alu.id
            where mat.alumnoid = %s;
        '''
        cursor.execute(sql,alu_id)
        elementos = cursor.fetchall() 
    conexion.close()
    return elementos
