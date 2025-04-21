from controladores.bd import obtener_conexion , sql_select_fetchall , sql_select_fetchone , sql_execute , sql_execute_lastrowid , show_columns , show_primary_key , exists_column_Activo , unactive_row_table
import controladores.bd as bd
#####_ CRUD _#####

table_name = 'unidad'

def get_info_columns():
    return show_columns(table_name)


def get_primary_key():
    return show_primary_key(table_name)


def exists_Activo():
    return exists_column_Activo(table_name)


def table_fetchall():
    sql= f'''
        select 
            *
        from {table_name}
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
            mo.nombre as nom_modelo
        from {table_name} ud
        inner join modelo mo on ud.modeloid = mo.id
        order by ud.id desc
    '''
    columnas = [ 'ID' , 'Placa' , 'Capacidad (kg)' , 'Volumen (m³)' , 'Observaciones' , 'Actividad' , 'Modelo' ]
    filas = sql_select_fetchall(sql)
    
    return columnas , filas


def delete_row( id ):
    sql = f'''
        delete from {table_name}
        where id = {id}
    '''
    sql_execute(sql)


######_ CRUD ESPECIFICAS _###### 

def unactive_row( id ):
    unactive_row_table(table_name , id)


def insert_row( placa , capacidad ,volumen , observaciones , activo , modeloid ):
    sql = f'''
        INSERT INTO 
            {table_name} 
            ( placa , capacidad , volumen , observaciones , activo , modeloid )
        VALUES 
            ( '{placa}' , '{capacidad}' , '{volumen}' , '{observaciones}' , '{activo}' , '{modeloid}')
    '''
    sql_execute(sql)


def update_row( id , placa , capacidad ,volumen , observaciones , activo , modeloid ):
    sql = f'''
        Update {table_name} set 
        placa = '{placa}' , 
        capacidad = '{capacidad}' ,
        volumen = '{volumen}' ,
        observaciones = '{observaciones}' ,
        activo = {activo} ,
        modeloid = {modeloid} ,
        where id = {id}
    '''
    sql_execute(sql)



#####_ ADICIONALES _#####



