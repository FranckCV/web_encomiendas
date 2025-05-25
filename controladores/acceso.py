import controladores.bd as bd

def get_lista_modulos():
    sql= f'''
        select 
            mdl.id ,
            mdl.nombre ,
            mdl.icono ,
            mdl.key ,
            mdl.color ,
            mdl.activo 
        from modulo mdl
        order by 2 asc 
    '''

    filas = bd.sql_select_fetchall(sql)
    return  filas


def get_modulo_key(key):
    sql= f'''
        select 
            mdl.id ,
            mdl.nombre ,
            mdl.icono ,
            mdl.key ,
            mdl.color ,
            mdl.activo 
        from modulo mdl
        where mdl.key = %s
    '''
    filas = bd.sql_select_fetchone(sql,(key))
    return  filas


def get_tipos_pagina_moduloid(id):
    sql= f'''
        select 
            tip.id ,
            tip.nombre ,
            pag.moduloid ,
            count(pag.id) as cant
        from tipo_pagina tip
        left join pagina pag on pag.tipo_paginaid = tip.id
        where pag.moduloid = %s
        group by tip.id  , pag.moduloid  
        order by 1 asc
    '''
    filas = bd.sql_select_fetchall(sql,(id))
    return  filas


def get_pagina_key(key):
    sql= f'''
        select 
            pag.id ,
            pag.titulo ,
            pag.icono ,
            pag.activo ,
            pag.key ,
            pag.tipo_paginaid , 
            pag.moduloid 
        from pagina pag
        where pag.key = %s
    '''
    filas = bd.sql_select_fetchone(sql,(key))
    return  filas


def get_lista_tipo_paginas():
    sql= f'''
        SELECT 
            tp.id ,
            tp.nombre ,
            m.id as moduloid,
            COUNT(p.id) AS cant
        FROM tipo_pagina tp
        CROSS JOIN modulo m
        LEFT JOIN pagina p ON p.tipo_paginaid = tp.id AND p.moduloid = m.id
        GROUP BY m.id, tp.id
    '''

    filas = bd.sql_select_fetchall(sql)
    return  filas


def get_paginas():
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


def get_paginas_moduloid(moduloid):
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
        where moduloid = {moduloid}
        order by pag.titulo
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
        order by rol.nombre

    '''

    filas = bd.sql_select_fetchall(sql)
    
    return  filas


def get_lista_tipo_roles():
    sql= f'''
        SELECT
            tip.id,
            tip.nombre,
            tip.activo,
            COUNT(rol.id) AS cant
        FROM tipo_rol tip
        LEFT JOIN rol ON rol.tipo_rolid = tip.id
        WHERE tip.activo = 1 AND tip.id != 1
        GROUP BY tip.id
        HAVING COUNT(rol.id) != 0;
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

def get_cants_modulos():
    sql= f'''
        SELECT 
            m.id ,
            m.nombre ,
            tp.id AS tip_id,
            tp.nombre AS tip_nombre,
            COUNT(p.id) AS cant
        FROM tipo_pagina tp
        CROSS JOIN modulo m
        LEFT JOIN pagina p ON p.tipo_paginaid = tp.id AND p.moduloid = m.id
        GROUP BY m.id, tp.id;
    '''

    filas = bd.sql_select_fetchall(sql)
    
    return  filas


def update_modulo( id , titulo , icono , color ):
    sql = f'''
        update modulo set 
            nombre = %s , 
            icono = %s , 
            color = %s
        where id = {id}
    '''
    bd.sql_execute(sql,( titulo , icono , color ))


def update_pagina( id , titulo , icono , moduloid ):
    sql = f'''
        update pagina set 
            titulo = %s , 
            icono = %s , 
            moduloid = %s
        where id = {id}
    '''
    bd.sql_execute(sql,( titulo , icono , moduloid ))


def unable_permiso_pagina(column , paginaid , rolid):
    sql = f'''
        update acceso set 
        {column} = NOT {column}
        where paginaid = {paginaid} and rolid = {rolid}
    '''
    bd.sql_execute(sql)
    # return 0



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

