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
    sql = f"DELETE FROM {table_name} WHERE id = %s"
    sql_execute(sql, (id,))

def unactive_row(id):
    unactive_row_table(table_name, id)

def get_by_id(id):
    sql = f"SELECT * FROM {table_name} WHERE id = %s"
    return sql_select_fetchone(sql, (id,))

def get_table():
    sql = f"SELECT * FROM {table_name}"
    columnas = {
        "id": ["ID", 0.3],
        "nombres_razon": ["Nombres/Razón social", 2.5],
        "direccion": ["Dirección", 2.5],
        "correo": ["Correo", 2],
        "telefono": ["Teléfono", 1],
        "n_documento": ["N° Documento", 1.5],
        "monto_indemnizado": ["Indemnización", 1.5],
        "bien_contratado": ["Bien contratado", 2.5],
        "monto_reclamado": ["Monto reclamado", 1.5],
        "relacion": ["Relación", 1],
        "fecha_recepcion": ["Recepción", 1.5],
        "fecha_recojo": ["Recojo", 1.5],
        "descripcion": ["Descripción", 2.5],
        "detalles": ["Detalles", 2.5],
        "pedido": ["Pedido", 2],
        "foto": ["Foto", 1],
        "sucursal_id": ["Sucursal", 1],
        "causa_reclamoid": ["Causa", 1],
        "tipo_indemnizacionid": ["Tipo indemnización", 1.5],
        "paquetetracking": ["N° Tracking", 1.5],
        "ubigeocodigo": ["Ubigeo", 1],
        "tipo_documentoid": ["Tipo Documento", 1]
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas

def insert_row(nombres_razon, direccion, correo, telefono, n_documento,
               monto_indemnizado, bien_contratado, monto_reclamado,
               relacion, fecha_recepcion, sucursal_id, descripcion,
               detalles, pedido, foto, causa_reclamoid, tipo_indemnizacionid,
               paquetetracking, ubigeocodigo, tipo_documentoid):

    sql = f'''
        INSERT INTO {table_name} (
            nombres_razon, direccion, correo, telefono, n_documento,
            monto_indemnizado, bien_contratado, monto_reclamado,
            relacion, fecha_recepcion, sucursal_id, descripcion,
            detalles, pedido, foto, causa_reclamoid, tipo_indemnizacionid,
            paquetetracking, ubigeocodigo, tipo_documentoid
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    '''
    sql_execute(sql, (
        nombres_razon, direccion, correo, telefono, n_documento,
        monto_indemnizado, bien_contratado, monto_reclamado,
        relacion, fecha_recepcion, sucursal_id, descripcion,
        detalles, pedido, foto, causa_reclamoid, tipo_indemnizacionid,
        paquetetracking, ubigeocodigo, tipo_documentoid
    ))

def update_row(id, nombres_razon, direccion, correo, telefono, n_documento,
               monto_indemnizado, bien_contratado, monto_reclamado,
               relacion, fecha_recepcion, sucursal_id, descripcion,
               detalles, pedido, foto, causa_reclamoid, tipo_indemnizacionid,
               paquetetracking, ubigeocodigo, tipo_documentoid):

    sql = f'''
        UPDATE {table_name} SET
            nombres_razon = %s,
            direccion = %s,
            correo = %s,
            telefono = %s,
            n_documento = %s,
            monto_indemnizado = %s,
            bien_contratado = %s,
            monto_reclamado = %s,
            relacion = %s,
            fecha_recepcion = %s,
            sucursal_id = %s,
            descripcion = %s,
            detalles = %s,
            pedido = %s,
            foto = %s,
            causa_reclamoid = %s,
            tipo_indemnizacionid = %s,
            paquetetracking = %s,
            ubigeocodigo = %s,
            tipo_documentoid = %s
        WHERE id = %s
    '''
    sql_execute(sql, (
        nombres_razon, direccion, correo, telefono, n_documento,
        monto_indemnizado, bien_contratado, monto_reclamado,
        relacion, fecha_recepcion, sucursal_id, descripcion,
        detalles, pedido, foto, causa_reclamoid, tipo_indemnizacionid,
        paquetetracking, ubigeocodigo, tipo_documentoid, id
    ))
# Clase usada por main.py
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

    def insert_row(self, form):
        return insert_row(form)

    def update_row(self, id, *args):
        return update_row(id, *args)


####pagina reclamo

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

    

