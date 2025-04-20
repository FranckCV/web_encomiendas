from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# from functools import wraps
import hashlib
import base64
from datetime import datetime, date
from controladores import bd as bd
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

# id/name , label , placeholder , type/element_html , required , list

CONTROLADORES = {
    "marca": {
        "active" : True ,
        "titulo": "Marcas",
        "nombre_tabla": "marca",
        "controlador": controlador_marca,
        "fields_insert": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
        ],
        "fields_update": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
        ],
        "fields_consult": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
        ],
        "crud_forms": {
            "crud_list":     True ,
            "crud_search":   False ,
            "crud_consult":  False ,
            "crud_insert":   True ,
            "crud_update":   False ,
            "crud_delete":   False ,
            "crud_unactive": False ,
        }
    },
    "unidad": {
        "active" : True ,
        "titulo": "Unidades",
        "nombre_tabla": "unidad",
        "controlador": controlador_unidad,
        "fields_insert": [
            ['placa', 'Placa', 'Placa', 'text', True , None ],
            ['capacidad', 'capacidad', 'capacidad', 'text', True , None ],
            ['volumen', 'volumen', 'volumen', 'text', True , None ],
            ['observaciones', 'observaciones', 'observaciones', 'text', False , None ],
            ['activo', 'activo', 'activo', 'text', True , None ],
            ['modeloid', 'modeloid', 'modeloid', 'text', True , None ],
        ],
        "fields_update": [
            ['nombre', 'Nombre', 'Nombre', 'text', True],
        ],
        "fields_consult": [
            ['nombre', 'Nombre', 'Nombre', 'text', True],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": False ,
            "crud_consult": False ,
            "crud_insert": True ,
            "crud_update": False ,
            "crud_delete": False ,
            "crud_unactive": False ,
        }
    },
    "modelo": {
        "active" : True ,
        "titulo": "Modelos",
        "nombre_tabla": "modelo",
        "controlador": controlador_modelo,
        "fields_insert": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
            ['marcaid', 'Marca', 'Marca', 'select', True , controlador_marca.get_options_marca() ],
            ['tipo_unidadid', 'Tipo de Unidad', 'Tipo de Unidad', 'select', True , controlador_tipo_unidad.get_options() ],
        ],
        "fields_update": [
            ['nombre', 'Nombre', 'Nombre', 'text', True],
        ],
        "fields_consult": [
            ['nombre', 'Nombre', 'Nombre', 'text', True],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": False ,
            "crud_consult": False ,
            "crud_insert": True ,
            "crud_update": False ,
            "crud_delete": False ,
            "crud_unactive": False ,
        }
    },
    "tipo_unidad": {
        "active" : True ,
        "titulo": "Tipos de Unidad",
        "nombre_tabla": "tipo de unidad",
        "controlador": controlador_tipo_unidad,
        "fields_insert": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
            ['descripcion', 'descripcion', 'descripcion', 'textarea', True , None ],
            ['activo', 'Activo', 'Activo', 'text', True , None ],
        ],
        "fields_update": [
            ['nombre', 'Nombre', 'Nombre', 'text', True],
        ],
        "fields_consult": [
            ['nombre', 'Nombre', 'Nombre', 'text', True],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": False ,
            "crud_consult": False ,
            "crud_insert": True ,
            "crud_update": False ,
            "crud_delete": False ,
            "crud_unactive": False ,
        }
    },

}


def listar_cruds():
    table_names = list(CONTROLADORES.keys())
    pages = []
    for tabla in table_names:
        config = CONTROLADORES.get(tabla)
        active = config["active"]
        if active is True:
            titulo = config["titulo"]
            pages.append([ tabla , titulo ])
    return pages


@app.context_processor
def inject_globals():
    lista_paginas_crud = listar_cruds()

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

@app.route("/crud=<tabla>")
def crud_generico(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]

    if active is False:
        return "Tabla no soportada", 404

    titulo = config["titulo"]
    controlador = config["controlador"]
    nombre_tabla = config["nombre_tabla"]
    fields_insert = config["fields_insert"]
    fields_update = config["fields_update"]
    fields_consult = config["fields_consult"]

    CRUD_FORMS = config["crud_forms"]
    crud_list = CRUD_FORMS.get("crud_list")
    crud_search = CRUD_FORMS.get("crud_search")
    crud_consult = CRUD_FORMS.get("crud_consult")
    crud_insert = CRUD_FORMS.get("crud_insert")
    crud_update = CRUD_FORMS.get("crud_update")
    crud_delete = CRUD_FORMS.get("crud_delete")
    crud_unactive = CRUD_FORMS.get("crud_unactive")

    resultados = controlador.table_fetchall()
    columnas , filas = controlador.get_table()
    info_columns = controlador.get_info_columns()

    return render_template(
        "listado.html" ,
        tabla = tabla ,
        nombre_tabla = nombre_tabla ,
        titulo = titulo ,
        columnas = columnas ,
        filas = filas ,
        resultados = resultados,
        fields_insert = fields_insert ,
        fields_update = fields_update ,
        fields_consult = fields_consult ,
        bd_columns = list(resultados[0].keys()) if resultados else [] ,
        table_columns = list(filas[0].keys()) if filas else [] ,
        info_columns = info_columns,
        crud_list     = crud_list,
        crud_search   = crud_search,
        crud_consult  = crud_consult,
        crud_insert   = crud_insert,
        crud_update   = crud_update,
        crud_delete   = crud_delete,
        crud_unactive = crud_unactive,
    )






##################_ METHOD POST _################## 


@app.route(f"/{FUNC_INSERT}=<tabla>", methods=["POST"])
def crud_insert(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]

    if active is False:
        return "Tabla no soportada", 404

    controlador = config["controlador"]
    fields = config["fields_insert"]

    valores = []
    for campo in fields:
        nombre = campo[0] 
        requerido = campo[4]
        valor = request.form.get(nombre)
        if requerido and not valor:
            return f"Campo {nombre} es obligatorio", 400
        valores.append(valor)

    controlador.insert_row( *valores )

    return redirect(url_for('crud_generico', tabla = tabla))


@app.route(f"/{FUNC_DELETE}=<tabla>", methods=["POST"])
def crud_delete(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]

    if active is False:
        return "Tabla no soportada", 404

    controlador = config["controlador"]

    controlador.delete_row( request.form["id"] )

    return redirect(url_for('crud_generico', tabla = tabla))


@app.route(f"/{FUNC_UPDATE}=<tabla>", methods=["POST"])
def crud_update(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]

    if active is False:
        return "Tabla no soportada", 404

    controlador = config["controlador"]
    fields = config["fields_update"]

    valores = []
    for campo in fields:
        nombre = campo[0] 
        requerido = campo[4]
        valor = request.form.get(nombre)
        if requerido and not valor:
            return f"Campo {nombre} es obligatorio", 400
        valores.append(valor)

    controlador.update_row( *valores )

    return redirect(url_for('crud_generico', tabla = tabla))








if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)



##################_ _ARCHIVADO_ _################## 
