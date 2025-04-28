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
            ud.capacidad ,
            ud.volumen ,
            ud.observaciones ,
            ud.activo ,
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
        'nom_modelo' : ['Modelo' , 1.5] ,
        'nom_tipounidad' : ['Tipo de unidad' , 1.5] ,
        'nom_marca' :     ['Marca' , 1.5] ,
        'capacidad' : ['Capacidad (kg)' , 1 ] , 
        'volumen' : ['Volumen (m³)' , 1 ] ,
        'activo' : ['Actividad', 1 ] ,
        }
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


######_ CAMBIAR PARAMETROS Y SQL INTERNO _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( placa , capacidad ,volumen  , modeloid , observaciones = None):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( placa , capacidad , volumen , observaciones , activo , modeloid )
        VALUES 
            ( '{placa}' , '{capacidad}' , '{volumen}' , '{observaciones}' , 1 , '{modeloid}')
    '''
    sql_execute(sql)


def update_row( id , placa , capacidad ,volumen , modeloid  , observaciones):
    sql = f'''
        Update {table_name} set 
        placa = '{placa}' , 
        capacidad = {capacidad} ,
        volumen = {volumen} ,
        observaciones = '{observaciones}' ,
        modeloid = {modeloid} 
        where id = {id}
    '''
    sql_execute(sql)



#####_ ADICIONALES _#####



