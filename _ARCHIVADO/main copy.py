from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# from functools import wraps
import hashlib
import base64
from datetime import datetime, date
from controladores import controlador_color as controlador_color
from controladores import controlador_marca as controlador_marca
from controladores import controlador_unidad as controlador_unidad
from controladores import controlador_tipo_unidad as controlador_tipo_unidad
from controladores import controlador_modelo as controlador_modelo

app = Flask(__name__, template_folder='templates')

# NOMBRE_CRUD_PAGE = 'Mantenimiento de'
FUNCIONES_CRUD = 'crud'
NOMBRE_CRUD_PAGE = 'Gestionar'
NOMBRE_OPTIONS_COL = 'Acciones'

NOMBRE_BTN_INSERT   = 'Agregar'
NOMBRE_BTN_UPDATE   = 'Editar'
NOMBRE_BTN_DELETE   = 'Eliminar'
NOMBRE_BTN_UNACTIVE = 'Activar/Desactivar'
NOMBRE_BTN_LIST     = 'Listar'
NOMBRE_BTN_CONSULT  = 'Consultar'
NOMBRE_BTN_SEARCH   = 'Buscar'

FUNC_INSERT   = 'insert'
FUNC_UPDATE   = 'update'
FUNC_DELETE   = 'delete'
FUNC_UNACTIVE = 'unactive'
FUNC_LIST     = 'crud'
FUNC_CONSULT  = 'ver'
FUNC_SEARCH   = 'search'

def listar_cruds():
    funciones = [nombre for nombre, obj in globals().items()
        if callable(obj) and nombre.startswith(FUNCIONES_CRUD)]
    
    # for name in funciones:
    #     pal = name.split(FUNCIONES_CRUD)
    #     print(pal)

    return funciones


@app.context_processor
def inject_globals():
    lista_paginas_crud =listar_cruds()
    return dict(
        lista_paginas_crud = lista_paginas_crud ,

        NOMBRE_CRUD_PAGE    = NOMBRE_CRUD_PAGE,
        NOMBRE_OPTIONS_COL  = NOMBRE_OPTIONS_COL,
        NOMBRE_BTN_INSERT   = NOMBRE_BTN_INSERT,
        NOMBRE_BTN_UPDATE   = NOMBRE_BTN_UPDATE,
        NOMBRE_BTN_DELETE   = NOMBRE_BTN_DELETE,
        NOMBRE_BTN_UNACTIVE = NOMBRE_BTN_UNACTIVE,
        NOMBRE_BTN_LIST     = NOMBRE_BTN_LIST,
        NOMBRE_BTN_CONSULT  = NOMBRE_BTN_CONSULT,
        NOMBRE_BTN_SEARCH   = NOMBRE_BTN_SEARCH,

    )

paginas_simples = [ "index" ]

for pagina in paginas_simples:
    app.add_url_rule(
        f"/{pagina}",  # URL
        pagina,        # Nombre de la función
        lambda p=pagina: render_template(f"{p}.html")  # Renderiza la plantilla
    )


@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

##################_ CRUD PAGE _################## 

# @app.route("/lista")
# def listad():
#     titulo = 'Marcas'
#     nombre_tabla = 'marca'
#     resultados = controlador_marca.table_fetchall()
#     columnas , filas = controlador_marca.get_table()
#     bd_columns = list(filas[0].keys()) if filas else []
#     # print(bd_columns)

#     form_campos = [
#         # ID / name , label , placeholder , type , required , filter
#         [ 'nombre' , 'Nombre' , 'Nombre' , 'text' , True ] ,
#     ]
    
#     return render_template(
#         "index.html" ,
#         resultados = resultados ,
#         filas = filas ,
#         columnas = columnas ,
#         bd_columns = bd_columns ,
#     )


@app.route("/crud_unidad")
def crud_unidad():
    titulo = 'Unidades'
    nombre_tabla = 'unidad'
    resultados = controlador_unidad.table_fetchall()
    columnas , filas = controlador_unidad.get_table()

    form_campos = [
        # ID / name , label , placeholder , type , required , filter
        [ 'nombre' , 'Nombre' , 'Nombre' , 'text' , True ] ,
    ]
    
    bd_columns = list(filas[0].keys()) if filas else []
    form_list     = [ False , f'{FUNC_LIST}_{nombre_tabla}' ]
    form_insert   = [ True ,  f'{FUNC_INSERT}_{nombre_tabla}' ]
    form_consult  = [ True , f'{FUNC_CONSULT}_{nombre_tabla}' ]
    form_update   = [ True , f'{FUNC_UPDATE}_{nombre_tabla}' ]
    form_unactive = [ True , f'{FUNC_UNACTIVE}_{nombre_tabla}' ]
    form_delete   = [ True , f'{FUNC_DELETE}_{nombre_tabla}' ]
    form_search   = [ False , f'{FUNC_SEARCH}_{nombre_tabla}' ]

    return render_template(
        "listado.html" ,
        titulo = titulo ,
        bd_columns = bd_columns ,
        columnas = columnas ,
        filas = filas ,
        resultados = resultados,
        nombre_tabla = nombre_tabla ,
        form_campos   = form_campos ,
        form_list     = form_list,
        form_search   = form_search,
        form_consult  = form_consult,
        form_insert   = form_insert,
        form_update   = form_update,
        form_delete   = form_delete,
        form_unactive = form_unactive,
    )



CONTROLADORES = {
    "marca": {
        "titulo": "Marcas",
        "controlador": controlador_marca,
        "form_campos": [
            ['nombre', 'Nombre', 'Nombre', 'text', True],
        ],
        "crud_forms": {
            "crud_list": True ,
        }
    },
}


@app.route("/crud=<tabla>")
def crud_generico(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    titulo = config["titulo"]
    controlador = config["controlador"]
    form_campos = config["form_campos"]

    CRUD_FORMS = config["crud_forms"]
    act_list = CRUD_FORMS.get("crud_list")
    print(act_list)

    resultados = controlador.table_fetchall()
    columnas , filas = controlador.get_table()

    return render_template(
        "listado.html" ,
        nombre_tabla = tabla ,
        titulo = titulo ,
        columnas = columnas ,
        filas = filas ,
        resultados = resultados,
        form_campos = form_campos ,
        bd_columns = list(filas[0].keys()) if filas else [] ,
        form_list     = [True , f'{FUNC_LIST}_{tabla}'],
        form_insert   = [True , f'{FUNC_INSERT}_{tabla}'],
        form_consult  = [True , f'{FUNC_CONSULT}_{tabla}'],
        form_update   = [True , f'{FUNC_UPDATE}_{tabla}'],
        form_delete   = [True , f'{FUNC_DELETE}_{tabla}'],
        form_unactive = [True , f'{FUNC_UNACTIVE}_{tabla}'],
        form_search   = [True , f'{FUNC_SEARCH}_{tabla}'],
    )






##################_ METHOD POST _################## 

@app.route(f"/{FUNC_UPDATE}=<tabla>", methods=["POST"])
def crud_update(tabla):
    id = request.form["id"]
    nombre = request.form["nombre"]

    controlador_marca.update_row( id , nombre )
    return redirect(f"/{FUNCIONES_CRUD}_"+"marca")


@app.route(f"/{FUNC_INSERT}=<tabla>", methods=["POST"])
def crud_insert(tabla):
    nombre = request.form["nombre"]

    controlador_marca.insert_row(nombre)
    return redirect(url_for(crud_generico(tabla)))



@app.route(f"/{FUNC_UPDATE}_"+"marca", methods=["POST"])
def update_marca():
    id = request.form["id"]
    nombre = request.form["nombre"]

    controlador_marca.update_row( id , nombre )
    return redirect(f"/{FUNCIONES_CRUD}_"+"marca")


@app.route(f"/{FUNC_INSERT}_"+"marca", methods=["POST"])
def insert_marca():
    nombre = request.form["nombre"]

    controlador_marca.insert_row(nombre)
    return redirect(f"/{FUNCIONES_CRUD}_"+"marca")



@app.route(f"/{FUNC_UPDATE}_"+"unidad", methods=["POST"])
def update_unidad():
    id = request.form["id"]
    nombre = request.form["nombre"]

    controlador_marca.update_row( id , nombre )
    return redirect(f"/{FUNCIONES_CRUD}_"+"unidad")


@app.route(f"/{FUNC_INSERT}_"+"unidad", methods=["POST"])
def insert_unidad():
    nombre = request.form["nombre"]

    controlador_marca.insert_row(nombre)
    return redirect(f"/{FUNCIONES_CRUD}_"+"unidad")





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)



##################_ _ARCHIVADO_ _################## 

# @app.route("/crud_modelo")
# def crud_modelo():
#     titulo = 'Modelos'
#     nombre_tabla = 'modelo'
#     columnas , resultados = controlador_modelo.get_table_modelo()

#     campos_form = [
#         [ 'nombre' , 'Nombre' , 'Nombre' , 'text' , True ] ,
#         [ 'id_nom' , 'nombre' , 'palceholder' , 'tipo' , True ] ,
#         [ 'id_nom' , 'nombre' , 'palceholder' , 'tipo' , True ] ,
#     ]

#     form_insert    = [ True , f'{FUNC_INSERT}_{nombre_tabla}' ]
#     form_update    = [ False , '' ]
#     form_delete    = [ False , '' ]
#     form_search    = [ False , '' ]
#     form_list      = [ False , '' ]
#     form_unaactive = [ False , '' ]
#     form_consult   = [ False , '' ]

#     return render_template(
#         "listado.html" ,
#         titulo = titulo ,
#         columnas = columnas ,
#         resultados = resultados,
#         nombre_tabla = nombre_tabla ,
#         campos_form = campos_form ,
#         form_list      = form_list,
#         form_search    = form_search,
#         form_consult   = form_consult,
#         form_insert    = form_insert,
#         form_update    = form_update,
#         form_delete    = form_delete,
#         form_unaactive = form_unaactive,
#     )


# @app.route("/crud_tipo_unidad")
# def crud_tipo_unidad():
#     titulo = 'Tipos de unidades'
#     nombre_tabla = 'tipo de unidad'
#     columnas , resultados = controlador_tipo_unidad.get_table_tipo_unidad()

#     form_insert    = [ False , f'{FUNC_INSERT}_{nombre_tabla}' ]
#     form_update    = [ False , '' ]
#     form_delete    = [ False , '' ]
#     form_search    = [ False , '' ]
#     form_list      = [ False , '' ]
#     form_unaactive = [ False , '' ]
#     form_consult   = [ False , '' ]

#     return render_template(
#         "listado.html" ,
#         titulo = titulo ,
#         columnas = columnas ,
#         resultados = resultados,
#         nombre_tabla = nombre_tabla ,
#         form_list      = form_list,
#         form_search    = form_search,
#         form_consult   = form_consult,
#         form_insert    = form_insert,
#         form_update    = form_update,
#         form_delete    = form_delete,
#         form_unaactive = form_unaactive,
#     )


# @app.route("/crud_unidad")
# def crud_unidad():
#     titulo = 'Unidades'
#     nombre_tabla = 'unidad'
#     columnas , resultados = controlador_unidad.get_table()

#     form_insert    = [ False , f'{FUNC_INSERT}_{nombre_tabla}' ]
#     form_update    = [ False , '' ]
#     form_delete    = [ False , '' ]
#     form_search    = [ False , '' ]
#     form_list      = [ False , '' ]
#     form_unaactive = [ False , '' ]
#     form_consult   = [ False , '' ]

#     return render_template(
#         "listado.html" ,
#         titulo = titulo ,
#         columnas = columnas ,
#         resultados = resultados,
#         nombre_tabla = nombre_tabla ,
#         form_list      = form_list,
#         form_search    = form_search,
#         form_consult   = form_consult,
#         form_insert    = form_insert,
#         form_update    = form_update,
#         form_delete    = form_delete,
#         form_unaactive = form_unaactive,
#     )


# @app.route("/crud_color")
# def crud_color():
#     titulo = 'Colores'
#     nombre_tabla = 'color'
#     columnas , resultados = controlador_color.get_table_colores()

#     form_insert    = [ False , f'{FUNC_INSERT}_{nombre_tabla}' ]
#     form_update    = [ False , '' ]
#     form_delete    = [ False , '' ]
#     form_search    = [ False , '' ]
#     form_list      = [ False , '' ]
#     form_unaactive = [ False , '' ]
#     form_consult   = [ False , '' ]

#     return render_template(
#         "listado.html" ,
#         titulo = titulo ,
#         columnas = columnas ,
#         resultados = resultados,
#         nombre_tabla = nombre_tabla ,
#         form_list      = form_list,
#         form_search    = form_search,
#         form_consult   = form_consult,
#         form_insert    = form_insert,
#         form_update    = form_update,
#         form_delete    = form_delete,
#         form_unaactive = form_unaactive,
#     )


# @app.route("/guardar_modelo", methods=["POST"])
# def insert_modelo():
#     nombre = request.form["nombre"]
#     abrev = request.form["abrev"]
#     cred = request.form["cred"]
#     ciclo = request.form["ciclo"]
#     colorid = request.form["colorid"]
#     controlador_modelo.insertar_curso(nombre,abrev,cred,ciclo,colorid)

#     return redirect(f"/{FUNCIONES_CRUD}_modelo")




