#Cuando programo una salida también inserto una escala y un empleado-salida
from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'salida'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( id ):
    bd.delete_row_table(table_name , id)


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
                WHEN 'P' THEN 'Pendiente (sucursal de origen)'
                WHEN 'T' THEN 'En curso (en ruta)'
                WHEN 'C' THEN 'Completada (sucursal de destino)'
                WHEN 'X' THEN 'Cancelada'
                ELSE 'Estado desconocido'
            END AS estado
        FROM salida s
        LEFT JOIN unidad u ON u.id = s.unidadid
        LEFT JOIN empleado e ON e.id = s.conductor_principal
        LEFT JOIN sucursal su ON su.id = s.destino_final_id
        LEFT JOIN ubigeo ub ON ub.codigo = su.ubigeocodigo
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


######_ CAMBIAR PARAMETROS Y SQL INTERNO _###### 

# def unactive_row( id ):
#     unactive_row_table(table_name , id)


# def insert_row( nombre , descripcion = None ):
#     sql = f'''
#         INSERT INTO 
#             {table_name} ( nombre , descripcion , activo )
#         VALUES 
#             ( %s , %s , 1 )
#     '''
#     sql_execute(sql,( nombre , descripcion ))


# def update_row( id , nombre , descripcion =None ):
#     sql = f'''
#         update {table_name} set 
#         nombre = %s ,
#         descripcion = %s
#         where {get_primary_key()} = {id}
#     '''
#     sql_execute(sql,(nombre , descripcion))


#####_ ADICIONALES _#####


def get_salida_pendiente_placa(placa):
    sql= f'''
        SELECT so.id AS salida_id, o.id AS origen_id, 
        o.latitud AS origen_latitud, o.longitud AS origen_longitud, 
        d.id AS destino_id, d.latitud AS destino_latitud, 
        d.longitud AS destino_longitud, u.placa AS unidad_placa 
        FROM salida so 
        JOIN sucursal o ON o.id = so.origen_inicio_id 
        JOIN sucursal d ON d.id = so.destino_final_id 
        JOIN unidad u ON u.id = so.unidadid
        where u.placa = %s and so.estado = 'E'
    '''
    
    filas = sql_select_fetchall(sql,(placa))
    
    return filas


def get_info_salida_pendiente_placa(placa):
    sql= f'''
        SELECT 
            so.id AS salida_id,
            o.id AS origen_id,
            o.latitud AS origen_latitud,
            o.longitud AS origen_longitud,
            uo.departamento AS origen_departamento,
            uo.provincia AS origen_provincia,
            uo.distrito AS origen_distrito,

            d.id AS destino_id,
            d.latitud AS destino_latitud,
            d.longitud AS destino_longitud,
            ud.departamento AS destino_departamento,
            ud.provincia AS destino_provincia,
            ud.distrito AS destino_distrito,

            u.placa AS unidad_placa,
            CONCAT(c.nombre , ' ' , c.apellidos) AS conductor_nombre,
            so.estado,
            so.fecha,
            so.hora
        FROM salida so
        JOIN sucursal o ON o.id = so.origen_inicio_id
        JOIN ubigeo uo ON uo.codigo = o.ubigeocodigo
        JOIN sucursal d ON d.id = so.destino_final_id
        JOIN ubigeo ud ON ud.codigo = d.ubigeocodigo
        JOIN unidad u ON u.id = so.unidadid
        JOIN empleado c ON c.id = so.conductor_principal
        WHERE u.placa = %s AND so.estado = 'E'

    '''
    
    filas = sql_select_fetchall(sql,(placa))
    
    return filas

def change_state_exit(id):
    try:
        sql_check = "SELECT COUNT(*) as cantidad FROM salida WHERE id = %s"
        resultado = sql_select_fetchone(sql_check,(id,))
        if resultado['cantidad'] == 0:
            return {'success': False, 'message': 'No existe una salida con ese ID'}
        sql_update = "UPDATE salida SET estado = 'T' WHERE id = %s"
        sql_execute(sql_update,(id,))
        return {'success': True, 'message': 'Estado actualizado correctamente'}

    except Exception as e:
        return {'success': False, 'message': f'Error al actualizar: {str(e)}'}

def get_data_by_id_salida(id):
    sql = '''
        select u.placa, concat(e.nombre,' ',e.apellidos) as conductor,s.fecha,
        concat(uo.departamento,' / ',uo.provincia,' / ',uo.distrito) as origen, concat(ud.departamento,' / ',ud.provincia,' / ',ud.distrito) as destino,
        CASE
            WHEN s.estado = 'P' THEN 'Pendiente'
            WHEN s.estado = 'T' then 'En curso'
        END as estado
        from salida s
        inner join unidad u on u.id=s.unidadid
        inner join empleado_salida es on es.salidaid = s.id
        inner join empleado e on e.id = es.empleadoid
        inner join sucursal so on so.id = s.origen_inicio_id
        inner join ubigeo uo on uo.codigo = so.ubigeocodigo
        inner join sucursal sd on sd.id = s.destino_final_id
        inner join ubigeo ud on ud.codigo = sd.ubigeocodigo
        where s.id = %s
    '''
    fila = sql_select_fetchone(sql,(id,))
    return fila


def crear_transaccion_salida(vehiculo, empleados, escalas, paquetes):
    conexion = obtener_conexion()
    with conexion:
        with conexion.cursor() as cursor:
            # 1. Determinar conductor principal (primer empleado)
            conductor_principal = empleados[0]

            # 2. Insertar en tabla salida
            sql_salida = '''
                INSERT INTO salida (fecha, hora, recojo, entrega, estado, unidadid, destino_final_id, conductor_principal, origen_inicio_id)
                VALUES (CURDATE(), CURTIME(), 0, 0, 'P', %s, %s, %s, %s)
            '''
            cursor.execute(sql_salida, (
                vehiculo['id'],
                vehiculo['destino_final_id'],
                conductor_principal,
                vehiculo['origen_inicio_id']
            ))

            salida_id = cursor.lastrowid  # Obtener el ID generado

            # 3. Insertar en empleado_salida
            sql_empleado = 'INSERT INTO empleado_salida (salidaid, empleadoid) VALUES (%s, %s)'
            for empleado_id in empleados:
                cursor.execute(sql_empleado, (salida_id, empleado_id))

            # 4. Insertar escalas
            sql_escala = 'INSERT INTO escala (sucursalid, salidaid) VALUES (%s, %s)'
            for sucursal_id in escalas:
                cursor.execute(sql_escala, (sucursal_id, salida_id))

            # 5. Actualizar paquetes
            sql_paquete = "UPDATE paquete SET salidaid = %s, ultimo_estado = 'ET' WHERE tracking = %s"
            for paquete in paquetes:
                cursor.execute(sql_paquete, (salida_id, paquete['tracking']))

        conexion.commit()
        return salida_id

