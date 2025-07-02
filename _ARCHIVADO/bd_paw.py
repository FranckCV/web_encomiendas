import requests

def execute_bd_pythonanywhere(tipo , sql , args=None):
    res = requests.post("https://franckcv.pythonanywhere.com/api/sql", json={
        "tipo": tipo,
        "sql": sql ,
        "args": args ,
    })
    return res


def sql_select_fetchall(sql , args = None):
    try:
        resultados = execute_bd_pythonanywhere('fetchall' , sql , args)
        return resultados
    except Exception as e:
        return e


def sql_select_fetchone(sql , args = None):
    try:
        resultados = execute_bd_pythonanywhere('fetchone' , sql , args)
        return resultados
    except Exception as e:
        return e


def sql_execute(sql , args = None):
    try:
        resultados = execute_bd_pythonanywhere('execute' , sql , args)
        # return resultados
    except Exception as e:
        return e


def sql_execute_lastrowid(sql , args = None):
    try:
        resultados = execute_bd_pythonanywhere('execute_last_id' , sql , args)
        return resultados
    except Exception as e:
        return e


def show_columns(table_name):
    sql= f'''
        SHOW COLUMNS FROM 
        {table_name}
    '''
    columnas = sql_select_fetchall(sql)
    
    return columnas


def show_primary_key(tabla):
    keys = []
    for row in show_columns(tabla):
        if row['Key'] == 'PRI':
            keys.append(row['Field'])

    if len(keys) == 1:
        return keys[0]
    else:
        return keys


def find_column_table(column_name, tabla):
    for row in show_columns(tabla):
        # print(row)
        if row['Field'] == column_name:
            return row
    return None


def delete_row_table( table_name , id ):
    sql = f'''
        delete from {table_name}
        where {show_primary_key(table_name)} = {id}
    '''
    sql_execute(sql)


def exists_column_Activo(tabla):
    row = find_column_table('activo' , tabla)
    # print(row)
    return row is not None


def unactive_row_table(table , pk):
    sql = f'''
        update {table} set 
        activo = NOT activo
        where {show_primary_key(table)} = {pk}
    '''
    sql_execute(sql)
    # return 0
