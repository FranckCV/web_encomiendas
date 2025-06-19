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
            mdl.img
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
            mdl.activo ,
            mdl.img
        from modulo mdl
        where mdl.key = %s
    '''
    filas = bd.sql_select_fetchone(sql,(key))
    return  filas if key else None


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
    return  filas if key else None


def get_permiso_pagina_key(key):
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
            pag.moduloid ,
            mdl.nombre as nom_modulo , 
            tip.nombre as nom_tipo
        from pagina pag
        inner join modulo mdl on mdl.id = pag.moduloid
        inner join tipo_pagina tip on tip.id = pag.tipo_paginaid
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


############################################################


def get_modulos_rol(rolid):
    sql= f'''
        SELECT 
            mdl.id,
            mdl.nombre,
            mdl.icono,
            mdl.key,
            mdl.color,
            mdl.activo,
            mdl.img,
            COUNT(CASE WHEN per.acceso = 1 THEN 1 END) AS cantidad_paginas_con_acceso
        FROM pagina pag
        INNER JOIN modulo mdl ON mdl.id = pag.moduloid
        LEFT JOIN permiso per ON per.paginaid = pag.id AND per.rolid = {rolid}
        WHERE pag.activo = 1
        GROUP BY mdl.id, mdl.nombre, mdl.icono, mdl.key, mdl.color, mdl.activo, mdl.img
        HAVING cantidad_paginas_con_acceso > 0
        ORDER BY mdl.nombre
    '''
    data = bd.sql_select_fetchall(sql)
    return  data


def get_tipo_paginas_rol(rolid):
    sql= f'''
        SELECT 
            tp.id,
            tp.nombre,
            m.id AS moduloid,
            m.nombre AS modulo,
            COUNT(CASE WHEN per.acceso = 1 THEN 1 END) AS cant
        FROM tipo_pagina tp
        CROSS JOIN modulo m
        LEFT JOIN pagina p ON p.tipo_paginaid = tp.id AND p.moduloid = m.id AND p.activo = 1
        LEFT JOIN permiso per ON per.paginaid = p.id AND per.rolid = {rolid}
        GROUP BY tp.id, tp.nombre, m.id, m.nombre
        HAVING cant > 0
        ORDER BY m.nombre, tp.nombre;

    '''
    data = bd.sql_select_fetchall(sql)
    return  data


def get_modulo_permiso_rol(rolid , moduloid):
    sql= f'''
        SELECT 
            pag.id as paginaid, 
            per.acceso ,
            per.search ,
            per.consult ,
            per.insert ,
            per.update ,
            per.delete ,
            per.unactive 
        FROM rol
        CROSS JOIN pagina pag 
        inner join modulo mdl on mdl.id = pag.moduloid
        inner join tipo_pagina tip on tip.id = pag.tipo_paginaid
        LEFT JOIN permiso per ON per.rolid = rol.id AND per.paginaid = pag.id
        WHERE rol.id = {rolid} and rol.activo = 1  and pag.moduloid = {moduloid} 
        order by pag.titulo
    '''
    data = bd.sql_select_fetchall(sql)
    return  data


def get_paginas_permiso_rol( rolid ):
    sql= f'''
        SELECT 
            pag.id , 
            pag.titulo , 
            pag.icono , 
            pag.activo, 
            pag.key , 
            pag.tipo_paginaid , 
            pag.moduloid ,
            mdl.nombre as nom_modulo , 
            tip.nombre as nom_tipo ,
            per.acceso ,
            per.search ,
            per.consult ,
            per.insert ,
            per.update ,
            per.delete ,
            per.unactive 
        FROM rol
        CROSS JOIN pagina pag 
        inner join modulo mdl on mdl.id = pag.moduloid
        inner join tipo_pagina tip on tip.id = pag.tipo_paginaid
        LEFT JOIN permiso per ON per.rolid = rol.id AND per.paginaid = pag.id
        WHERE rol.id = {rolid} and rol.activo = 1 and pag.activo = 1 
        order by pag.titulo
    '''
    data = bd.sql_select_fetchall(sql)
    return  data


def consult_permiso_rol( paginaid, rolid):
    sql= f'''
        SELECT 
            rol.* ,
            rol.activo as rol_activo ,
            per.* ,
            pag.* ,
            pag.activo as pag_activo 
        FROM rol
        CROSS JOIN pagina pag  
        LEFT JOIN permiso per ON per.rolid = rol.id AND per.paginaid = pag.id
        WHERE rol.id = {rolid} and pag.id = {paginaid} and rol.activo = 1 
    '''
    data = bd.sql_select_fetchone(sql)
    return  data


def nuevo_permiso_pagina_rol( paginaid , rolid):
    sql = f'''
        INSERT INTO `permiso`(`paginaid`, `rolid`, `acceso`, `search`, `consult`, `insert`, `update`, `delete`, `unactive`) VALUES 
        ( %s , %s , 0 , 0 , 0 , 0 , 0 , 0 , 0 )
    '''
    bd.sql_execute(sql, (paginaid , rolid))


def update_permiso_pagina(column , paginaid , rolid , value = None):
    sql = f'''
        update permiso set 
        `{column}` = {value if value is not None else f'NOT `{column}`' }
        where paginaid = {paginaid} and rolid = {rolid}
    '''
    bd.sql_execute(sql)


def change_permiso_pagina(column , paginaid , rolid , value = None):
    data = consult_permiso_rol( paginaid , rolid)
    if data['paginaid'] is not None and data['rolid'] is not None: 
        update_permiso_pagina(column , paginaid , rolid , value)
    else:
        nuevo_permiso_pagina_rol( paginaid , rolid)
        update_permiso_pagina(column , paginaid , rolid , value)


def change_permiso_modulo(column , moduloid , rolid , value = None):
    filas = get_paginas_moduloid(moduloid)
    for pagina in filas:
        change_permiso_pagina(column , pagina['id'] , rolid , value)
    

def validar_acceso(rolid , f_name , f_kwarg ):
    if f_name == 'panel' :
        return True
    elif f_name == 'modulo' :
        menu_modulos = get_modulos_rol(rolid)
        keys = [modulo['key'] for modulo in menu_modulos]
        if f_kwarg in keys:
            return True
        return None
    elif f_name == 'crud_generico' or f_name == 'reporte' or f_name == 'transaccion' or f_name == 'grafico' or f_name.startswith('crud_') :
        page = get_pagina_key(f_kwarg)
        if page:
            pag_id = page['id']
            permiso_rol = consult_permiso_rol(pag_id , rolid)
            if f_name.startswith('crud_') and f_name != 'crud_generico':
                for op in ['insert' , 'update' , 'delete' , 'unactive']:
                    if f_name == f'crud_{op}' and permiso_rol[op] == 1:
                        return True
            else:
                acceso = permiso_rol['acceso']
                return acceso if permiso_rol['pag_activo'] and permiso_rol['rol_activo'] else 0
        return None
    else :
        page = get_pagina_key(f_name)
        if page:
            pag_id = page['id']
            permiso_rol = consult_permiso_rol(pag_id , rolid)
            acceso = permiso_rol['acceso']
            return acceso if permiso_rol['pag_activo'] and permiso_rol['rol_activo'] else 0
        return None
    


def get_permiso_rol( paginaid, rolid ):
    sql= f'''
        SELECT 
            rol.* ,
            rol.activo as rol_activo ,
            per.* ,
            pag.* ,
            pag.activo as pag_activo 
        FROM rol
        CROSS JOIN pagina pag  
        LEFT JOIN permiso per ON per.rolid = rol.id AND per.paginaid = pag.id
        WHERE rol.id = {rolid} and pag.id = {paginaid} and rol.activo = 1 
    '''
    data = bd.sql_select_fetchone(sql)
    return  data



