from controladores.bd import (
    sql_select_fetchall, sql_select_fetchone, sql_execute,
    show_columns, show_primary_key, exists_column_Activo, unactive_row_table
)

table_name = 'reclamo'

def get_info_columns():
    return show_columns(table_name)

def get_primary_key():
    return show_primary_key(table_name)

def exists_Activo():
    return exists_column_Activo(table_name)

def delete_row(id):
    sql = f"DELETE FROM {table_name} WHERE id = {id}"
    sql_execute(sql)

def get_table():
    sql = f'''
        SELECT id, nombres_razon, direccion, correo, telefono, n_documento,
               monto_indemnizado, titulo_incidencia, bien_contratado, monto_reclamado,
               relacion, fecha_recojo, sucursal_id, descripcion, pedido,
               causa_reclamoid, tipo_indemnizacionid,
               paquetetracking, ubigeocodigo, tipo_documentoid
        FROM {table_name}
    '''
    columnas = {
        'id': ['ID', 0.5],
        'nombres_razon': ['Cliente', 1.5],
        'direccion': ['Dirección', 1.5],
        'correo': ['Correo', 1.2],
        'telefono': ['Teléfono', 1.2],
        'titulo_incidencia': ['Incidencia', 1.5],
        'monto_reclamado': ['Monto Reclamado', 1],
        'fecha_recojo': ['Fecha', 1],
        'estado_reclamoid': ['Estado', 1],
        'sucursal_id': ['Sucursal', 1],
    }

    try:
        filas = sql_select_fetchall(sql)
    except Exception as e:
        print("❌ Error en get_table reclamo:", e)
        filas = []

    return columnas, filas

def insert_row(nombres_razon, direccion, correo, telefono, n_documento,
               monto_indemnizado, titulo_incidencia, bien_contratado, monto_reclamado,
               relacion, fecha_recojo, sucursal_id, descripcion, pedido,
               causa_reclamoid, tipo_indemnizacionid,
               paquetetracking, ubigeocodigo, tipo_documentoid):
    sql = f'''
        INSERT INTO {table_name} (
            nombres_razon, direccion, correo, telefono, n_documento,
            monto_indemnizado, titulo_incidencia, bien_contratado, monto_reclamado,
            relacion, fecha_recojo, sucursal_id, descripcion, pedido,
            causa_reclamoid, tipo_indemnizacionid,
            paquetetracking, ubigeocodigo, tipo_documentoid
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    sql_execute(sql, (
        nombres_razon, direccion, correo, telefono, n_documento,
        monto_indemnizado, titulo_incidencia, bien_contratado, monto_reclamado,
        relacion, fecha_recojo, sucursal_id, descripcion, pedido,
        causa_reclamoid, tipo_indemnizacionid,
        paquetetracking, ubigeocodigo, tipo_documentoid
    ))

def update_row(id, nombres_razon, direccion, correo, telefono, n_documento,
               monto_indemnizado, titulo_incidencia, bien_contratado, monto_reclamado,
               relacion, fecha_recojo, sucursal_id, descripcion, pedido,
               causa_reclamoid, tipo_indemnizacionid,
               paquetetracking, ubigeocodigo, tipo_documentoid):
    sql = f'''
        UPDATE {table_name} SET
            nombres_razon = %s,
            direccion = %s,
            correo = %s,
            telefono = %s,
            n_documento = %s,
            monto_indemnizado = %s,
            titulo_incidencia = %s,
            bien_contratado = %s,
            monto_reclamado = %s,
            relacion = %s,
            fecha_recojo = %s,
            sucursal_id = %s,
            descripcion = %s,
            pedido = %s,
            causa_reclamoid = %s,
            tipo_indemnizacionid = %s,
            paquetetracking = %s,
            ubigeocodigo = %s,
            tipo_documentoid = %s
        WHERE id = %s
    '''
    sql_execute(sql, (
        nombres_razon, direccion, correo, telefono, n_documento,
        monto_indemnizado, titulo_incidencia, bien_contratado, monto_reclamado,
        relacion, fecha_recojo, sucursal_id, descripcion, pedido,
        causa_reclamoid, tipo_indemnizacionid,
        paquetetracking, ubigeocodigo, tipo_documentoid,
        id
    ))

class ControladorReclamo:
    def get_info_columns(self):
        return get_info_columns()

    def get_primary_key(self):
        return get_primary_key()

    def exists_Activo(self):
        return exists_Activo()

    def delete_row(self, id):
        return delete_row(id)

    def get_table(self):
        return get_table()

    def insert_row(self, *args):
        return insert_row(*args)

    def update_row(self, *args):
        return update_row(*args)




BIEN_CONTRATADO = {
    "P" : "Producto" ,
    "S" : "Servicio" ,
    "A" : "Producto y servicio" ,
}


def get_list_bien_contratado():
    lst = BIEN_CONTRATADO.keys()
    filas = []
    for bien in lst:
        filas.append([bien , BIEN_CONTRATADO[bien]])
    return filas


def get_dict_tipo_reclamo():
    sql= f'''
        select 
            tip.id,
            tip.nombre
        from tipo_reclamo tip
        where tip.activo = 1
        order by tip.nombre
    '''
    filas = sql_select_fetchall(sql)
    return filas


def get_dict_motivo_reclamo():
    sql= f'''
        select
            mot.id ,
            mot.nombre ,
            tip.id as tip_id
        from motivo_reclamo mot
        inner join tipo_reclamo tip on tip.id = mot.tipo_reclamoid
        where tip.activo = 1
        order by mot.nombre
    '''
    filas = sql_select_fetchall(sql)
    return filas


def get_dict_causa_reclamo():
    sql= f'''
        select
            cau.id ,
            cau.nombre ,
            mot.id as mot_id ,
            tip.id as tip_id
        from causa_reclamo cau
        inner join motivo_reclamo mot on mot.id = cau.motivo_reclamoid
        inner join tipo_reclamo tip on tip.id = mot.tipo_reclamoid
        where tip.activo = 1
        order by cau.nombre

    '''
    filas = sql_select_fetchall(sql)
    return filas



def registrar_reclamo(
        nombres_razon, 
        direccion, 
        correo, telefono, 
        n_documento, 
        bien_contratado, 
        monto_reclamado, 
        fecha_recepcion, 
        sucursal_id, 
        descripcion, detalles, 
        pedido, 
        foto, 
        causa_reclamoid, 
        tipo_documentoid, 
        paquetetracking, 

        tipo_indemnizacionid = None, 
        relacion = None, 
        monto_indemnizado = None, 
        ubigeocodigo = None
    ):
    sql = f'''
        INSERT INTO reclamo (
            nombres_razon, direccion, correo, telefono, n_documento, monto_indemnizado, bien_contratado, monto_reclamado, relacion, fecha_recepcion, sucursal_id, descripcion, detalles, pedido, foto, causa_reclamoid, tipo_indemnizacionid, paquetetracking, ubigeocodigo, tipo_documentoid
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    sql_execute(sql, (
        nombres_razon, direccion, correo, telefono, n_documento, monto_indemnizado, bien_contratado, monto_reclamado, relacion, fecha_recepcion, sucursal_id, descripcion, detalles, pedido, foto, causa_reclamoid, tipo_indemnizacionid, paquetetracking, ubigeocodigo, tipo_documentoid
    ))

    