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

def get_table():
    sql = f'''
        SELECT id, nombres_razon, direccion, correo, telefono, n_documento,
               monto_indemnizado, bien_contratado, monto_reclamado,
               relacion, fecha_recepcion, sucursal_id, descripcion,
               detalles, pedido, foto,
               causa_reclamoid, tipo_indemnizacionid, paquetetracking,
               ubigeocodigo, tipo_documentoid
        FROM {table_name}
    '''

    columnas = {
        'id': ['ID', 0.5],
        'nombres_razon': ['Cliente', 1.5],
        'direccion': ['Dirección', 1.5],
        'correo': ['Correo', 1.2],
        'telefono': ['Teléfono', 1.2],
        'monto_reclamado': ['Monto Reclamado', 1],
        'fecha_recepcion': ['Fecha', 1],
        'tipo_documentoid': ['Tipo Documento', 1],
        'sucursal_id': ['Sucursal', 1],
    }

    try:
        filas = sql_select_fetchall(sql)
    except Exception as e:
        print("❌ Error en get_table reclamo:", e)
        filas = []

    return columnas, filas

def insert_row(form):
    if not form:
        raise ValueError("❌ Formulario vacío.")

    form = dict(form)  # Convierte ImmutableMultiDict a dict

    campos = [
        "nombres_razon", "direccion", "correo", "telefono", "n_documento",
        "monto_indemnizado", "bien_contratado", "monto_reclamado",
        "relacion", "fecha_recepcion", "sucursal_id", "descripcion",
        "detalles", "pedido", "foto", "causa_reclamoid", "tipo_indemnizacionid",
        "paquetetracking", "ubigeocodigo", "tipo_documentoid"
    ]

    valores = []
    for campo in campos:
        valor = form.get(campo)
        if valor == '':
            valor = None
        valores.append(valor)

    if any(v is None for v in valores):
        raise ValueError("❌ Algunos campos requeridos están vacíos o mal nombrados")

    sql = f'''
        INSERT INTO {table_name} (
            {', '.join(campos)}
        ) VALUES ({', '.join(['%s'] * len(valores))})
    '''

    sql_execute(sql, valores)
    return True

def update_row(id, *args):
    campos = [
        "nombres_razon", "direccion", "correo", "telefono", "n_documento",
        "monto_indemnizado", "bien_contratado", "monto_reclamado",
        "relacion", "fecha_recepcion", "sucursal_id", "descripcion",
        "detalles", "pedido", "foto", "causa_reclamoid", "tipo_indemnizacionid",
        "paquetetracking", "ubigeocodigo", "tipo_documentoid"
    ]

    if len(args) != len(campos):
        raise ValueError("❌ Número incorrecto de argumentos para update")

    sql = f'''
        UPDATE {table_name} SET
            {', '.join([f"{campo} = %s" for campo in campos])}
        WHERE id = %s
    '''

    sql_execute(sql, (*args, id))
    return True

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
