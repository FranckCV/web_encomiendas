from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd

table_name = 'transaccion_encomienda'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)



#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql= f'''
        select 
            *
        from {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    
    return resultados


def get_table():
    sql= f'''
        SELECT
        s.id, 
    CONCAT(e.nombre, ' ', e.apellidos) AS nom_conductor,
    u.placa,
    ub.departamento AS destino,
    s.fecha,
    s.hora,
    u.capacidad,
    CASE s.estado
        WHEN 'P' THEN 'Pendiente (origen sucursal / domicilio)'
        WHEN 'E' THEN 'En curso (en ruta)'
        WHEN 'C' THEN 'Completada (destino sucursal / domicilio)'
        WHEN 'X' THEN 'Cancelada'
        ELSE 'Estado desconocido'
    END AS estado
FROM salida s
INNER JOIN unidad u ON u.id = s.unidadid
INNER JOIN empleado e ON e.id = s.conductor_principal
INNER JOIN sucursal su ON su.id = s.destino_final
INNER JOIN ubigeo ub ON ub.codigo = su.ubigeocodigo
    '''
    columnas = {
        'id': ['ID' , 0.5 ] , 
        'nom_conductor' : ['Conductor' , 1 ] , 
        'placa' : ['Placa' , 1] , 
        'destino' : ['Destino' , 3.5] , 
        'fecha' : ['Fecha' , 1.2] , 
        'hora' : ['Hora' , 1] , 
        'capacidad' : ['Capacidad' , 1.5] , 
        'estado' : ['Estado' , 3.5] ,

        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas



# def insert_rows(cliente:dict):
#     try:
        
#     except Exception as e:
        

def insert_cliente(correo, telefono, num_doc, nombre, tipo_doc):
    verificar_sql = "SELECT id FROM cliente WHERE num_documento = %s"
    existente = sql_select_fetchall(verificar_sql, (num_doc,))
    if existente:
        return existente[0]['id']

    if tipo_doc == 2:
        column = 'apellidos_razon'
        tipo_cliente = 2
    else:
        column = 'nombre_siglas'
        tipo_cliente = 1

    insert_sql = f"""
        INSERT INTO cliente (
            correo,
            telefono,
            num_documento,
            {column},
            tipo_documentoid,
            tipo_clienteid
        ) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    params = (correo, telefono, num_doc, nombre, tipo_doc, tipo_cliente)

    new_row = sql_execute(insert_sql, params, fetchone=True)
    return new_row['id']



# def registrar_encomienda(num_serie, masivo, descripcion, recojo_casa, id_sucursal_origen, estado_pago, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid) :
#     sql = f'''
#         INSERT INTO transaccion_encomienda
#         (num_serie, masivo, descripcion, recojo_casa, id_sucursal_origen, estado_pago, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid) 
#         VALUES
#         (%, %s, %s, %s, %s, estado_pago, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid) 
#     '''
#     id = sql_execute_lastrowid(sql,(num_serie, masivo, descripcion, recojo_casa, id_sucursal_origen, estado_pago, fecha, hora, direccion_recojo, clienteid, tipo_comprobanteid) )
#     return id






