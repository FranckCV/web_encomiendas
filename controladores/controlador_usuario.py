from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'usuario'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where id = {id}
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


def get_table():
    sql = f'''
        SELECT 
            usu.id,
            usu.correo,
            -- usu.contrasenia,  -- comentado según tu ejemplo
            CASE 
                WHEN usu.tipo_usuario = 'E' THEN 'Empleado'
                WHEN usu.tipo_usuario = 'C' THEN 'Cliente'
                ELSE 'Otro'
            END AS tipo_usuario,
            usu.activo
        FROM {table_name} usu
    '''
    
    columnas = {
        'id'           : ['ID', 0.5],
        'correo'       : ['Correo', 4.5],
        'tipo_usuario' : ['Tipo Usuario', 4.5],
        'activo'       : ['Actividad', 1],
    }

    filas = sql_select_fetchall(sql)
    
    return columnas, filas



######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( nombre ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( nombre , activo )
        VALUES 
            ( %s , 1 )
    '''
    sql_execute(sql,( nombre ))


def update_row( id , nombre ):
    sql = f'''
        update {table_name} set 
        nombre = %s 
        where {get_primary_key()} = {id}
    '''
    sql_execute(sql, (nombre ))


#####_ ADICIONALES _#####

def get_options():
    sql= f'''
        select 
            {get_primary_key()} ,
            nombre
        from {table_name}
        where activo = 1
        order by nombre asc
    '''
    filas = sql_select_fetchall(sql)
    
    lista = [(fila[get_primary_key()], fila["nombre"]) for fila in filas]

    return lista


def get_usuario_por_correo(correo):
    sql= f'''
        select 
            usu.id ,
            usu.correo ,
            usu.contrasenia ,
            usu.tipo_usuario ,
            usu.activo ,
            emp.id as emp_id ,
            emp.nombre,
            emp.apellidos ,
            emp.rolid ,
            cli.id as cli_id ,
            cli.telefono ,
            cli.num_documento ,
            cli.nombre_siglas ,
            cli.apellidos_razon ,
            cli.tipo_documentoid ,
            cli.tipo_clienteid
        from usuario usu
        left join cliente cli on cli.correo = usu.correo
        left join empleado emp on emp.correo = usu.correo
        where usu.correo = %s and usu.activo = 1
    '''

    info = sql_select_fetchone(sql , (correo))
    return info


def get_usuario_por_id(user_id):
    sql= f'''
        select 
            usu.id ,
            usu.correo ,
            usu.contrasenia ,
            usu.tipo_usuario ,
            usu.activo ,
            emp.id as emp_id ,
            emp.nombre,
            emp.apellidos ,
            emp.rolid ,
            cli.id as cli_id ,
            cli.telefono ,
            cli.num_documento ,
            cli.nombre_siglas ,
            cli.apellidos_razon ,
            cli.tipo_documentoid ,
            cli.tipo_clienteid
        from usuario usu
        left join cliente cli on cli.correo = usu.correo
        left join empleado emp on emp.correo = usu.correo
        where usu.id = %s and usu.activo = 1
    '''

    info = sql_select_fetchone(sql , (user_id))
    return info


def get_usuario_cliente_por_id(user_id):
    sql= f'''
        select 
            usu.id ,
            usu.correo ,
            usu.contrasenia ,
            usu.tipo_usuario ,
            usu.activo ,
            cli.id as cli_id ,
            cli.telefono ,
            cli.num_documento ,
            cli.nombre_siglas ,
            cli.apellidos_razon ,
            cli.tipo_documentoid ,
            cli.tipo_clienteid ,
            tdc.siglas as tdc_siglas,
            tdc.nombre as tdc_nombre,
            tcl.nombre as tcl_nombre
        from usuario usu
        inner join cliente cli on cli.correo = usu.correo
        left join tipo_documento tdc on tdc.id = cli.tipo_documentoid
        left join tipo_cliente tcl on tcl.id = cli.tipo_clienteid
        where usu.tipo_usuario = 'C' and usu.id = %s and usu.activo = 1;
    '''

    info = sql_select_fetchone(sql , (user_id))
    return info


def get_usuario_empleado_user_id(user_id):
    sql= f'''
        select 
            usu.id ,
            usu.correo ,
            usu.contrasenia ,
            usu.tipo_usuario ,
            usu.activo ,
            emp.id as emp_id ,
            emp.nombre,
            emp.apellidos ,
            emp.rolid ,
            rol.nombre as rol_nombre ,
            rol.tipo_rolid ,
            tip.nombre as tip_nombre 
        from usuario usu
        inner join empleado emp on emp.correo = usu.correo
        inner join rol on rol.id = emp.rolid
        inner join tipo_rol tip on tip.id = rol.tipo_rolid
        where usu.tipo_usuario = 'E' and usu.id = %s 
        and usu.activo = 1 and rol.activo = 1 and tip.activo = 1
    '''

    info = sql_select_fetchone(sql , (user_id))
    return info

def get_report_usuarios():
    sql = '''
        SELECT 
            id,
            correo,
            tipo_usuario,
            activo
        FROM usuario
        ORDER BY id 
    '''

    columnas = {
        'id': ['ID', 0.5],
        'correo': ['Correo', 2],
        'tipo_usuario': ['Tipo de Usuario', 1.5],
        'activo': ['Activo', 1],
    }

    filas = sql_select_fetchall(sql)
    return columnas, filas


def get_options():
    sql = '''
        SELECT 
            tipo_usuario,
            tipo_usuario AS nombre
        FROM usuario
        WHERE activo = 1
        GROUP BY tipo_usuario
        ORDER BY tipo_usuario 
    '''
    filas = sql_select_fetchall(sql)
    lista = [(fila['tipo_usuario'], fila['tipo_usuario']) for fila in filas]
    return lista


def register_user_client( correo , contrasenia ):
    sql = f'''
        INSERT INTO 
            usuario 
            ( correo , contrasenia , tipo_usuario , activo )
        VALUES 
            ( %s , %s , 'C' , 1 )
    '''
    id = sql_execute_lastrowid(sql,( correo , contrasenia ))
    return id


def get_info_usuario_por_correo(correo):
    sql= f'''
        select 
            usu.id , 
            usu.correo as usu_correo, 
            emp.id as emp_id , 
            emp.correo , 
            cli.id as cli_id , 
            cli.correo as cli_correo 
        from usuario usu 
        left join cliente cli on cli.correo = usu.correo 
        left join empleado emp on emp.correo = usu.correo
        where usu.correo = %s
    '''

    info = sql_select_fetchone(sql , (correo))
    return info


