from controladores.bd import (
    obtener_conexion,
    sql_select_fetchall,
    sql_select_fetchone,
    sql_execute,
    sql_execute_lastrowid,
    show_columns,
    show_primary_key,
    exists_column_Activo,
    unactive_row_table
)

import controladores.bd as bd

#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'pregunta_frecuente'

def get_info_columns():
    return show_columns(table_name)

def get_primary_key():
    return show_primary_key(table_name)

def exists_Activo():
    return exists_column_Activo(table_name)

def delete_row(id):
    bd.delete_row_table(table_name, id)

#####_ CAMBIAR SQL y DICT INTERNO _#####

def table_fetchall():
    sql = f'''
        SELECT 
            id,
            titulo
        FROM {table_name}
    '''
    resultados = sql_select_fetchall(sql)
    return resultados

def get_table():
    sql = f'''
        SELECT 
            pf.id,
            pf.titulo,
            pf.descripcion,
            pf.activo
        FROM {table_name} pf
    '''
    columnas = {
        'id': ['ID', 0.5],
        'titulo': ['Título', 3],
        'descripcion': ['Descripción', 4],
        'activo': ['Actividad', 1]
    }
    filas = sql_select_fetchall(sql)
    return columnas, filas

######_ CAMBIAR PARAMETROS Y SQL INTERNO _######

def unactive_row(id):
    unactive_row_table(table_name, id)

def insert_row(titulo, descripcion):
    sql = f'''
        INSERT INTO 
            {table_name} (titulo, descripcion)
        VALUES 
            (%s, %s)
    '''
    sql_execute(sql, (titulo, descripcion))

def update_row(id, titulo, descripcion):
    sql = f'''
        UPDATE {table_name} SET 
            titulo = %s,
            descripcion = %s
        WHERE {get_primary_key()} = {id}
    '''
    sql_execute(sql, (titulo, descripcion))

#####_ ADICIONALES (si necesitas desplegar combos u opciones relacionadas) _#####

def get_options_preguntas():
    sql = f'''
        SELECT 
            id,
            titulo
        FROM {table_name}
        WHERE activo = 1
        ORDER BY titulo ASC
    '''
    filas = sql_select_fetchall(sql)
    lista = [(fila["id"], fila["titulo"]) for fila in filas]
    return lista
