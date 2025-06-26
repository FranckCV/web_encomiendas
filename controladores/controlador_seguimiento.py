from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'seguimiento'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( paquetetracking , detalle_estadoid ):
    sql = f'''
        delete from seguimiento
        where paquetetracking = {paquetetracking} and detalle_estadoid = {detalle_estadoid}
    '''
    sql_execute(sql)


#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql= f'''
        select 
            *
        from {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    
    return resultados


def get_table_pk_foreign(pk_foreign):
    sql = '''
        SELECT 
	e.nombre as estado,
	de.nombre as nombre_det,
    tc.nombre as tip_comp
        FROM 
            seguimiento s
        INNER JOIN detalle_estado de ON de.id = s.detalle_estadoid
        inner join estado_encomienda e on e.id = de.estado_encomiendaid
        LEFT join tipo_comprobante tc on tc.id = s.tipo_comprobanteid
        where s.paquetetracking = %s;
    '''

    columnas = {
        'estado':['Estado',2],
        'nombre_det': ['Detalle estado', 3],
        'tip_comp':['Comprobante',2]
    }

    filas = sql_select_fetchall(sql,pk_foreign)
    return columnas, filas



######_ CRUD ESPECIFICAS _###### 

# def unactive_row(id):
#     unactive_row_table("sucursal", id)


def insert_row(pk_foreign, detalle_estadoid,tipo_comprobante):
    sql = '''
        INSERT INTO seguimiento (paquetetracking, detalle_estadoid,tipo_comprobanteid)
        VALUES (%s, %s,%s)
    '''
    sql_execute(sql, (pk_foreign, detalle_estadoid,tipo_comprobante))


def update_row(paquetetracking, detalle_estadoid):
    sql = '''
        UPDATE seguimiento
        SET detalle_estadoid = %s
        WHERE paquetetracking = %s 
    '''
    sql_execute(sql, (detalle_estadoid,paquetetracking))


#####_ ADICIONALES _#####

def get_options_dict():
    sql= f'''
        select de.id,concat(de.nombre,'-',e.nombre) as nombre from detalle_estado de
        inner join estado_encomienda e on e.id = de.estado_encomiendaid
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila['id'], fila["nombre"]) for fila in filas]

    return lista