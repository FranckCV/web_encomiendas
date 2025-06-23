from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'empresa'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def delete_row( id ):
    bd.delete_row_table(table_name , id)

    
def get_rows():
    sql= f'''
        select 
            * ,
            CASE 
                WHEN emp.actual = 1 THEN 'actual'
                ELSE ''
            END AS e_actual,
            DATE_FORMAT(emp.fecha, "%d/%m/%Y") as fecha_txt 
        from empresa emp
        order by fecha desc , id desc
    '''
    resultados = sql_select_fetchall(sql)
    
    return resultados


def insert_row(nombre, correo, nro_telefono, logo, color_pri, color_sec, color_ter, porcentaje_recojo, ruc, id_sucursal, igv ):
    sql = '''
        INSERT INTO 
        empresa
        (nombre, correo, nro_telefono, logo, color_pri, color_sec, color_ter, porcentaje_recojo, ruc, id_sucursal, igv ) VALUES 
        ( %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s )
    '''
    emp_id = sql_execute_lastrowid(sql,(nombre, correo, nro_telefono, logo, color_pri, color_sec, color_ter, porcentaje_recojo, ruc, id_sucursal, igv ))
    return emp_id


def update_row( nombre , correo , nro_telefono , logo, porcentaje_recojo , color_pri , color_sec , color_ter ):
    sql = f'''
        update empresa set 
        nombre = %s ,
        correo = %s ,
        nro_telefono = %s ,
        logo = %s ,
        porcentaje_recojo = %s ,
        color_pri = %s ,
        color_sec = %s ,
        color_ter = %s 
        where actual = 1
    '''
    sql_execute(sql,( nombre , correo , nro_telefono , logo, porcentaje_recojo , color_pri , color_sec , color_ter ))


def dar_actual_empresa_id( id ):
    sql1 = f'''
        update empresa set 
        actual = 0
        where id != %s
    '''
    sql_execute(sql1,( id, ))

    sql2 = f'''
        update empresa set 
        actual = 1
        where id = %s
    '''
    sql_execute(sql2,( id, ))


def get_information():
    sql= f'''
        select 
            emp.id ,
            emp.nombre ,
            emp.correo ,
            emp.nro_telefono ,
            emp.color_pri ,
            emp.color_sec ,
            emp.color_ter 
        from empresa emp
        where actual = 1
    '''
    
    info = sql_select_fetchone(sql)
    
    return info


def get_data():
    sql= f'''
        select 
            emp.id ,
            emp.nombre ,
            emp.correo ,
            emp.nro_telefono ,
            emp.porcentaje_recojo , 
            emp.logo,
            emp.color_pri ,
            emp.color_sec ,
            emp.color_ter ,

            emp.ruc,
            emp.id_sucursal,
            emp.igv,
            emp.fecha,

            emp.actual
        from empresa emp
        where actual = 1
    '''
    
    info = sql_select_fetchone(sql)
    
    return info

def get_data_id(id):
    sql= f'''
        select 
            emp.id ,
            emp.nombre ,
            emp.correo ,
            emp.nro_telefono ,
            emp.porcentaje_recojo , 
            emp.logo,
            emp.color_pri ,
            emp.color_sec ,
            emp.color_ter ,

            emp.ruc,
            emp.id_sucursal,
            emp.igv,
            emp.fecha,

            emp.actual
        from empresa emp
        where id = %s
    '''
    
    info = sql_select_fetchone(sql,(id))
    
    return info

def get_logo():
    sql= f'''
        select 
            emp.logo 
        from empresa emp
        where actual = 1
    '''
    
    info = sql_select_fetchone(sql)['logo']
    
    return info


def get_porcentaje_recojo():
    sql= f'''
        select 
            emp.porcentaje_recojo 
        from empresa emp
        where actual = 1
    '''
    
    info = sql_select_fetchone(sql)['porcentaje_recojo']
    
    return info

def get_nombre():
    sql = """
        SELECT 
            emp.nombre
        FROM empresa emp
        WHERE actual = 1
    """
    fila = sql_select_fetchone(sql)
    return fila['nombre']

def getDataComprobante():
    sql='''
        select e.nombre,e.ruc,e.nro_telefono,e.correo,e.igv,s.direccion from empresa e 
        inner join sucursal s on s.id = e.id_sucursal
            '''
    fila = sql_select_fetchone(sql)
    return fila