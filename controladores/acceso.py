import controladores.bd as bd

def get_lista_modulos():
    sql= f'''
        select 
            mdl.id ,
            mdl.nombre ,
            mdl.icono ,
            mdl.key ,
            mdl.color ,
            mdl.activo ,
            count(pag.id) as cant
        from modulo mdl
        left join pagina pag on pag.moduloid = mdl.id
        group by mdl.id
        order by 2 asc 
    '''

    filas = bd.sql_select_fetchall(sql)
    
    return  filas


def get_paginas_crud():
    sql= f'''
        SELECT 
            pag.id , 
            pag.titulo , 
            pag.icono , 
            pag.activo, 
            pag.key , 
            pag.tipo_paginaid , 
            pag.moduloid 
        from pagina pag
        order by pag.titulo
    '''

    filas = bd.sql_select_fetchall(sql)
    
    return  filas


def get_lista_roles():
    sql= f'''
        select 
            rol.id ,
            rol.nombre ,
            rol.activo ,
            rol.tipo_rolid ,
            tip.id as id_tip,
            tip.nombre as nom_tip,
            tip.activo as act_tip
        from rol 
        left join tipo_rol tip on tip.id = rol.tipo_rolid
        where tip.activo = 1 and rol.activo = 1
    '''

    filas = bd.sql_select_fetchall(sql)
    
    return  filas


def get_lista_tipo_roles():
    sql= f'''
        select
            tip.id ,
            tip.nombre ,
            tip.activo
        from tipo_rol tip
        where activo = 1 and tip.id != 1
    '''

    filas = bd.sql_select_fetchall(sql)
    
    return  filas


def get_info_rol(rolid):
    sql= f'''
        select 
            rol.id ,
            rol.nombre ,
            rol.activo ,
            rol.tipo_rolid ,
            tip.id as id_tip,
            tip.nombre as nom_tip,
            tip.activo as act_tip
        from rol 
        left join tipo_rol tip on tip.id = rol.tipo_rolid
        where tip.activo = 1 and rol.activo = 1 and tip.id != 1 and rol.id = {rolid}
    '''

    a = bd.sql_select_fetchone(sql)
    
    return  a


# #####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####


# table_name = 'marca'

# def get_info_columns():
#     return bd.show_columns(table_name)


# def get_primary_key():
#     return bd.show_primary_key(table_name)


# def exists_Activo():
#     return bd.exists_column_Activo(table_name)


# def delete_row( id ):
#     bd.delete_row_table(table_name , id)


# #####_ CAMBIAR SQL y DICT INTERNO _#####

# def table_fetchall():
#     sql= f'''
#         select 
#             id ,
#             nombre
#         from {table_name}
#     '''
#     resultados = bd.sql_select_fetchall(sql)
    
#     return resultados


# def get_table():
#     sql= f'''
#         select 
#             mar.id ,
#             mar.nombre
#         from {table_name} mar
#     '''
#     columnas = {
#         'id': ['ID' , 0.5 ] , 
#         'nombre' : ['Nombre' , 9.5] , 
#         }
#     filas = bd.sql_select_fetchall(sql)
    
#     return columnas , filas


# ######_ CAMBIAR PARAMETROS Y SQL INTERNO _###### 

# def unactive_row( id ):
#     bd.unactive_row_table(table_name , id)


# def insert_row( nombre ):
#     sql = f'''
#         INSERT INTO 
#             {table_name} ( nombre )
#         VALUES 
#             ( %s )
#     '''
#     bd.sql_execute(sql,(nombre))


# def update_row( id , nombre ):
#     sql = f'''
#         update {table_name} set 
#         nombre = %s
#         where {get_primary_key()} = {id}
#     '''
#     bd.sql_execute(sql,(nombre))


# #####_ ADICIONALES _#####

# def get_options_marca():
#     sql= f'''
#         select 
#             id ,
#             nombre
#         from {table_name}
#         order by nombre asc
#     '''
#     filas = bd.sql_select_fetchall(sql)
    
#     lista = [(fila["id"], fila["nombre"]) for fila in filas]

#     return lista

