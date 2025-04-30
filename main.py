from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for , after_this_request
from controladores import bd as bd
from controladores import controlador_color as controlador_color
from controladores import controlador_marca as controlador_marca
from controladores import controlador_unidad as controlador_unidad
from controladores import controlador_tipo_unidad as controlador_tipo_unidad
from controladores import controlador_modelo as controlador_modelo
from configuraciones import NOMBRE_BTN_UPDATE , NOMBRE_BTN_UNACTIVE , ACT_STATE_0 , ACT_STATE_1 , FUNCIONES_CRUD , NOMBRE_BTN_CONSULT , NOMBRE_BTN_DELETE , NOMBRE_BTN_INSERT , NOMBRE_BTN_LIST , NOMBRE_BTN_SEARCH , NOMBRE_CRUD_PAGE , NOMBRE_OPTIONS_COL , STATE_0 , STATE_1 , TITLE_STATE, ICON_PAGE_CRUD
from functools import wraps
import inspect
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# import hashlib
# import base64
# from datetime import datetime, date

app = Flask(__name__, template_folder='templates')


###########_ FUNCIONES _#############

def listar_paginas_crud():
    table_names = list(CONTROLADORES.keys())
    pages = []
    for tabla in table_names:
        config = CONTROLADORES.get(tabla)
        active = config["active"]
        if active is True:
            titulo = config["titulo"]
            icon_page = config.get("icon_page")
            pages.append([ tabla , titulo , get_icon_page(icon_page) ])
    return pages


def get_options_active():
    lista = [
        [ 0 , STATE_0 ],
        [ 1 , STATE_1 ],
    ]
    return lista


def get_options_pagination_crud():
    lista = [ 5 , 10 , 15 , 20 , 25  ]
    selected_option_crud = 20
    return lista , selected_option_crud


def rdrct_error(resp_redirect , e):
    resp = make_response(resp_redirect)
    error_message = str(e)

    for clave in ERRORES:
        if clave in error_message:
            msg = ERRORES[clave]
            break 
    else:
        msg =  'ERROR DESCONOCIDO ENCONTRADO: '+error_message

    resp.set_cookie('error', msg , max_age=30)
    return resp 


def get_icon_page(icon):
    if not icon or icon == '':
        return ICON_PAGE_CRUD 
    else:
        return icon 


###########_ DICCIONARIOS _#############

ERRORES = {
    "'NoneType' object is not subscriptable" : "Inicie sesión con su cuenta correspondiente",
    "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again." : "El enlace al que intentó ingresar no existe." ,
    "NO_EXISTE_USERNAME" : "El nombre de usuario ingresado ya fue tomado por otro usuario" ,
    "NO_EXISTE_EMAIL" : "El correo electronico ingresado ya fue tomado por otro usuario" ,
    "LOGIN_INVALIDO" : 'Credenciales inválidas. Intente de nuevo' ,
    "foreign key constraint fails" : 'No es posible eliminar dicha fila' ,
}



CONTROLADORES = {
    "tipo_unidad": {
        "active" : True ,
        "titulo": "tipos de unidades",
        "nombre_tabla": "tipo de unidad",
        "controlador": controlador_tipo_unidad,
        "main_column": 'nombre',
        "icon_page": 'fa-solid fa-truck-moving',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',          'ID',              'ID',          'text',     True ,     False ,        None ],
            ['nombre',      'Nombre',          'Nombre',      'text',     True ,     True  ,        None ],
            ['activo',      f'{TITLE_STATE}',  'Activo',      'p',        True ,     False ,        None ],
            ['descripcion', 'Descripción',     'descripcion', 'textarea', False,     True  ,        None ],
        ],
        "field_search": [ 
            ['nombre' , ], 
            'nombre' , 
            150
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": True ,
            "crud_consult": True ,
            "crud_insert": True ,
            "crud_update": True ,
            "crud_delete": True ,
            "crud_unactive": True ,
        }
    },
    "marca": {
        "active" : True ,
        "titulo": "marcas de unidades",
        "nombre_tabla": "marca",
        "controlador": controlador_marca,
        "main_column": 'nombre',
        "filters": [] ,
        "fields_form": [
#            ID/NAME   LABEL     PLACEHOLDER  TYPE     REQUIRED   ABLE/DISABLE   DATOS
            ['id',     'ID',     'ID',        'text',  True ,     False ,        None ],
            ['nombre', 'Nombre', 'Nombre',    'text',  True ,     True ,         None ],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": True ,
            "crud_consult": True ,
            "crud_insert": True ,
            "crud_update": True ,
            "crud_delete": True ,
            "crud_unactive": True ,
        }
    },
    "modelo": {
        "active" : True ,
        "titulo": "modelos de unidades",
        "nombre_tabla": "modelo",
        "controlador": controlador_modelo,
        "main_column": 'nom_mod',
        "filters": [] ,
        "fields_form": [
#            ID/NAME            LABEL               PLACEHOLDER         TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',              'ID',               'ID',               'text',     False ,    False ,        None ],
            ['nombre',          'Nombre',           'Nombre',           'text',     True ,     True ,         None ],
            ['marcaid',         'Marca',            'Marca',            'select',   True ,     None,          [controlador_marca.get_options_marca() , 'nom_mar'] ],
            ['tipo_unidadid',   'Tipo de Unidad',   'Tipo de Unidad',   'select',   True ,     None ,         [controlador_tipo_unidad.get_options() , 'nom_tip'] ],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": True ,
            "crud_consult": True ,
            "crud_insert": True ,
            "crud_update": True ,
            "crud_delete": True ,
            "crud_unactive": True ,
        }
    },
    "unidad": {
        "active" : True ,
        "titulo": "unidades",
        "nombre_tabla": "unidad",
        "controlador": controlador_unidad,
        "main_column": 'placa',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
            ['modeloid', 'Modelo', controlador_modelo.get_options() ],
        ] ,
        "fields_form": [
#            ID/NAME          LABEL               PLACEHOLDER      TYPE         REQUIRED   ABLE/DISABLE   DATOS
            ['id',            'ID',               'ID',            'text',      False ,    False,         True ],
            ['placa',         'Placa',            'Placa',         'text',      True ,     True,          True ],
            ['activo',        f'{TITLE_STATE}',   'activo',        'p',         True ,     True,          None ],
            ['capacidad',     'Capacidad',        'Capacidad',     'number',    True ,     True,          True ],
            ['volumen',       'Volumen',          'Volumen',       'number',    True ,     True,          None ],
            ['modeloid',      'Nombre de Modelo', 'Elegir modelo', 'select',    True ,     True,          [controlador_modelo.get_options() , 'nom_modelo' ] ],
            ['observaciones', 'Observaciones',    'observaciones', 'textarea',  False,     True,          None ],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": True ,
            "crud_consult": True ,
            "crud_insert": True ,
            "crud_update": True ,
            "crud_delete": True ,
            "crud_unactive": True ,
        }
    },
}

###########_ REDIRECT _#############

def redirect_url(url):
    return redirect(url_for(url))


def redirect_crud(tabla):
    return redirect(url_for('crud_generico', tabla = tabla))


###########_ DECORADORES _#############

def validar_error_crud():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                tabla = kwargs.get('tabla') or args[0] 
                return rdrct_error(redirect_crud(tabla) , e) 
        return wrapper
    return decorator


###########_ PAGES _#############

@app.context_processor
def inject_globals():
    lista_paginas_crud = listar_paginas_crud()
    options_pagination_crud , selected_option_crud = get_options_pagination_crud()
    cookie_error = request.cookies.get('error')
    info_variables_crud = False
    HABILITAR_ICON_PAGES = True

    # print(request)

    return dict(
        info_variables_crud = info_variables_crud,
        lista_paginas_crud = lista_paginas_crud ,
        options_pagination_crud = options_pagination_crud ,
        selected_option_crud = selected_option_crud ,
        cookie_error = cookie_error,

        HABILITAR_ICON_PAGES = HABILITAR_ICON_PAGES,
        STATE_0 = STATE_0,   
        STATE_1 = STATE_1,
        ACT_STATE_0 = ACT_STATE_0,
        ACT_STATE_1 = ACT_STATE_1,
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


paginas_simples = [ "index" , 'login' , 'sign_up' , 'dashboard', 'agencias']

for pagina in paginas_simples:
    app.add_url_rule(
        f"/{pagina}",  # URL
        pagina,        # Nombre de la función
        lambda p=pagina: render_template(f"{p}.html")  # Renderiza la plantilla
    )


@app.route("/")
def main_page():
    return redirect(url_for('dashboard'))


##################_ CRUD PAGE _################## 

@app.route("/crud=<tabla>")
def crud_generico(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]

    if active is False:
        return "Tabla no soportada", 404
    
    value_search = request.args.get("value_search")

    icon_page_crud = get_icon_page(config.get("icon_page"))
    titulo = config["titulo"]
    controlador = config["controlador"]
    nombre_tabla = config["nombre_tabla"]
    main_column = config["main_column"]
    filters = config["filters"]
    fields_form = config["fields_form"]
    # fields_insert = config["fields_insert"]
    # fields_update = config["fields_update"]
    # fields_consult = config["fields_consult"]
    
    # resultados = controlador.table_fetchall()
    existe_activo = controlador.exists_Activo()
    columnas , filas = controlador.get_table()
    info_columns = controlador.get_info_columns()
    primary_key = controlador.get_primary_key()
    table_columns  = list(filas[0].keys()) if filas else []
    
    # firma = inspect.signature(controlador.insert_row)

    # for nombre_parametro, parametro in firma.parameters.items():
    #     print(nombre_parametro)

    CRUD_FORMS = config["crud_forms"]
    crud_list = CRUD_FORMS.get("crud_list")
    crud_search = CRUD_FORMS.get("crud_search")
    crud_consult = CRUD_FORMS.get("crud_consult")
    crud_insert = CRUD_FORMS.get("crud_insert")
    crud_update = CRUD_FORMS.get("crud_update")
    crud_delete = CRUD_FORMS.get("crud_delete")
    crud_unactive = CRUD_FORMS.get("crud_unactive") and existe_activo

    return render_template(
        "listado.html" ,
        tabla          = tabla ,
        nombre_tabla   = nombre_tabla ,
        icon_page_crud = icon_page_crud ,
        titulo         = titulo ,
        filas          = filas ,
        primary_key    = primary_key ,
        # resultados     = resultados,
        filters        = filters,
        fields_form    = fields_form ,
        # fields_insert  = fields_insert ,
        # fields_update  = fields_update ,
        # fields_consult = fields_consult ,
        value_search   = value_search,
        columnas       = columnas ,
        main_column    = main_column,
        key_columns    = list(columnas.keys()) ,
        table_columns  = table_columns ,
        info_columns   = info_columns,
        crud_list      = crud_list,
        crud_search    = crud_search,
        crud_consult   = crud_consult,
        crud_insert    = crud_insert,
        crud_update    = crud_update,
        crud_delete    = crud_delete,
        crud_unactive  = crud_unactive,
    )


##################_ METHOD POST _################## 

@app.route("/insert_row=<tabla>", methods=["POST"])
@validar_error_crud()
def crud_insert(tabla):
    # try:
        config = CONTROLADORES.get(tabla)
        if not config:
            return "Tabla no soportada", 404

        active = config["active"]

        if active is False:
            return "Tabla no soportada", 404

        controlador = config["controlador"]
        firma = inspect.signature(controlador.insert_row)

        valores = []
        for nombre, parametro in firma.parameters.items():
            valor = request.form.get(nombre)
            valores.append(valor)

        controlador.insert_row( *valores )

        return redirect(url_for('crud_generico', tabla = tabla))
    # except Exception as e:
    #     return f"No se aceptan carácteres especiales", 400


@app.route("/update_row=<tabla>", methods=["POST"])
@validar_error_crud()
def crud_update(tabla):
    # try:
        config = CONTROLADORES.get(tabla)
        if not config:
            return "Tabla no soportada", 404

        active = config["active"]

        if active is False:
            return "Tabla no soportada", 404

        controlador = config["controlador"]
        firma = inspect.signature(controlador.update_row)

        valores = []
        for nombre, parametro in firma.parameters.items():
            valor = request.form.get(nombre)
            valores.append(valor)

        controlador.update_row( *valores )

        return redirect(url_for('crud_generico', tabla = tabla))
    # except Exception as e:
    #     return f"No se aceptan carácteres especiales", 400


@app.route("/delete_row=<tabla>", methods=["POST"])
@validar_error_crud()
def crud_delete(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]

    if active is False:
        return "Tabla no soportada", 404

    controlador = config["controlador"]
    primary_key = controlador.get_primary_key()

    controlador.delete_row( request.form.get(primary_key) )

    return redirect(url_for('crud_generico', tabla = tabla))


@app.route("/unactive_row=<tabla>", methods=["POST"])
@validar_error_crud()
def crud_unactive(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]

    if active is False:
        return "Tabla no soportada", 404

    controlador = config["controlador"]
    existe_activo = controlador.exists_Activo()
    primary_key = controlador.get_primary_key()

    if existe_activo:
        controlador.unactive_row( request.form.get(primary_key) )

    return redirect(url_for('crud_generico', tabla = tabla))




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)



##################_ _ARCHIVADO_ _################## 
