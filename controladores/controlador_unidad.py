from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ MANTENER IGUAL - SOLO CAMBIAR table_name _#####

table_name = 'unidad'

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
            ud.* ,
            mo.nombre as nom_modelo
        from {table_name} ud
        left join modelo mo on ud.modeloid = mo.id
    '''
    resultados = sql_select_fetchall(sql)
    
    return resultados


def get_table():
    sql= f'''
        select 
            ud.id ,
            ud.placa,
            ud.mtc,
            ud.tuc,
            ud.capacidad ,
            ud.volumen ,
            ud.descripcion ,
            ud.estado ,
            ud.modeloid ,

            mo.nombre as nom_modelo ,
            tip.id ,
            tip.nombre as nom_tipounidad ,
            mar.nombre as nom_marca,
            mar.id
        from {table_name} ud
        inner join modelo mo on ud.modeloid = mo.id
        inner join tipo_unidad tip on mo.tipo_unidadid = tip.id
        inner join marca mar on mo.marcaid = mar.id
        
    '''
    
    columnas = {
        'id':['ID' , 0.5] , 
        'placa' : ['Placa' , 1.5]  , 
        'mtc' : ['MTC' , 1.5]  , 
        'tuc' : ['TUC' , 1.5]  , 
        'estado' : ['Estado' , 1]  , 
        'nom_tipounidad' : ['Tipo de unidad' , 1.5] ,
        'nom_modelo' : ['Modelo' , 1.5] ,
        'nom_marca' :     ['Marca' , 1.5] ,
        # 'capacidad' : ['Capacidad (kg)' , 1 ] , 
        # 'volumen' : ['Volumen (m³)' , 1 ] ,
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CAMBIAR PARAMETROS Y SQL INTERNO _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( placa , mtc , tuc , capacidad , volumen , modeloid , estado , descripcion):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( placa , mtc , tuc , capacidad , volumen , modeloid , estado , descripcion )
        VALUES 
            ( %s , %s , %s , %s , %s , %s , %s , %s )
    '''
    sql_execute(sql,( placa , mtc , tuc , float(capacidad) , float(volumen) , modeloid , estado , descripcion ))


def update_row( id , placa , mtc , tuc , capacidad , volumen , modeloid , estado , descripcion):
    sql = f'''
        Update {table_name} set 
            placa = %s , 
            mtc = %s , 
            tuc = %s , 
            capacidad = %s ,
            volumen = %s ,
            modeloid = %s,
            estado = %s ,
            descripcion = %s 
        where id = {id}
    '''
    sql_execute(sql,( placa , mtc , tuc , float(capacidad) , float(volumen) , modeloid , estado , descripcion ))



#####_ ADICIONALES _#####



def get_report_test():
    sql= f'''
        select 
            ud.id ,
            ud.placa,
            ud.estado ,
            ud.modeloid ,
            mo.nombre as nom_modelo ,
            tip.id as tip_id,
            tip.nombre as nom_tipounidad ,
            mar.nombre as nom_marca,
            mar.id as mar_id
        from {table_name} ud
        inner join modelo mo on ud.modeloid = mo.id
        inner join tipo_unidad tip on mo.tipo_unidadid = tip.id
        inner join marca mar on mo.marcaid = mar.id
        
    '''
    
    columnas = {
        'id'            : ['ID' , 0.5] , 
        'placa'         : ['Placa' , 1.5]  , 
        'nom_modelo'    : ['Modelo' , 1.5] ,
        'nom_tipounidad': ['Tipo de unidad' , 1.5] ,
        'nom_marca'     : ['Marca' , 1.5] ,
        # 'activo'        : ['Actividad', 1 ] ,
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas



def get_options_estado():
    lista= [
        [ 'D' , 'Disponible' ],
        [ 'C' , 'En curso' ],
        [ 'M' , 'En mantenimiento' ],
        [ 'N' , 'No disponible' ],
    ]

    return lista