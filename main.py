from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for , after_this_request
from controladores import bd as bd
from controladores import controlador_color as controlador_color
from controladores import controlador_marca as controlador_marca
from controladores import controlador_unidad as controlador_unidad
from controladores import controlador_tipo_unidad as controlador_tipo_unidad
from controladores import controlador_modelo as controlador_modelo
from configuraciones import NOMBRE_BTN_UPDATE , NOMBRE_BTN_UNACTIVE , ACT_STATE_0 , ACT_STATE_1 , FUNCIONES_CRUD , NOMBRE_BTN_CONSULT , NOMBRE_BTN_DELETE , NOMBRE_BTN_INSERT , NOMBRE_BTN_LIST , NOMBRE_BTN_SEARCH , NOMBRE_CRUD_PAGE , NOMBRE_OPTIONS_COL , STATE_0 , STATE_1 , TITLE_STATE , ICON_PAGE_CRUD
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# from functools import wraps
# import hashlib
# import base64
# from datetime import datetime, date

app = Flask(__name__, template_folder='templates')


def get_icon_page(icon):
    if not icon or icon == '':
        return ICON_PAGE_CRUD 
    else:
        return icon 


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



def listar_admin_pages():
    menu_keys = list(MENU_ADMIN.keys())
    # print(menu_keys)
    modules = []
    for module in menu_keys:
        pages_crud = []
        pages_report = []
        config = MENU_ADMIN.get(module)
        active = config["active"]
        if active is True:
            name = config.get("name")
            icon_module = get_icon_page(config.get("icon_page"))
            dashboard = config.get("dashboard")
            cruds = config.get("cruds")
            reports = config.get("reports")
            
            if cruds != [] and cruds is not None:
                for page in cruds:
                    config_page = CONTROLADORES.get(page)
                    if config_page:
                        p_active = config_page.get('active')
                        if p_active is True:
                            p_titulo = config_page.get('titulo')
                            p_icon_page = get_icon_page(config_page.get('icon_page'))
                            pages_crud.append([ page , p_titulo , p_icon_page ])
            
            if reports != [] and reports is not None:
                for page in reports:
                    if page is not None or page != '' :
                        pages_report.append( page )
            
            modules.append([ name , icon_module , dashboard , pages_crud , pages_report])
    return modules


def get_options_active():
    lista = [
        [ 0 , STATE_0 ],
        [ 1 , STATE_1 ],
    ]
    return lista


def get_options_pagination_crud():
    lista = [ 5 , 10 , 15 , 20 , 25  ]
    selected_option_crud = 5
    return lista , selected_option_crud


CONTROLADORES = {
    "tipo_unidad": {
        "active" : True ,
        "titulo": "tipos de unidades",
        "nombre_tabla": "tipo de unidad",
        "controlador": controlador_tipo_unidad,
        "main_column": 'nombre',
        "filters": [
            ['activo', f'Actividad', get_options_active() ],
        ] ,
        "fields_insert": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
            ['descripcion', 'Descripción', 'descripcion', 'textarea', False , None ],
        ],
        "fields_update": [
            ['nombre', 'Nombre', 'Nombre', 'text', True],
            ['descripcion', 'Descripción', 'descripcion', 'textarea', False , None ],
        ],
        "fields_consult": [
            ['id', 'ID:', 'Nombre', 'text', True],
            ['nombre', 'Nombre', 'Nombre', 'text', True],
            ['activo', f'{TITLE_STATE}', 'Nombre', 'p', True],
            ['descripcion', 'Descripción', 'Nombre', 'textarea', True],
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
        "fields_insert": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
        ],
        "fields_update": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
        ],
        "fields_consult": [
            ['nombre', 'Nombre', 'Nombre', 'text', True , None ],
        ],
        "field_search": [ 
            ['mar.nombre' , ], 
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
    "modelo": {
        "active" : True ,
        "titulo": "modelos de unidades",
        "nombre_tabla": "modelo",
        "controlador": controlador_modelo,
        "main_column": 'nom_mod',
        "filters": [] ,
        "fields_insert": [
            ['', 'ID', 'ID', 'text', False , False ],
            ['nombre', 'Nombre', 'Nombre', 'text', True , True ],
            ['marcaid', 'Marca', 'Marca', 'select', True , controlador_marca.get_options_marca() ],
            ['tipo_unidadid', 'Tipo de Unidad', 'Tipo de Unidad', 'select', True , controlador_tipo_unidad.get_options() ],
        ],
        "fields_update": [
            ['', 'ID', 'ID', 'text', False , False ],
            ['nombre', 'Nombre', 'Nombre', 'text', True , True],
            ['marcaid', 'Marca', 'Marca', 'select', True , controlador_marca.get_options_marca() ],
            ['tipo_unidadid', 'Tipo de Unidad', 'Tipo de Unidad', 'select', True , controlador_tipo_unidad.get_options() ],
        ],
        "fields_consult": [
            ['id', 'ID', 'Nombre', 'text', True],
            ['nom_mod', 'Nombre del Modelo', 'Nombre', 'text', True],
            ['nom_mar', 'Marca', 'Nombre', 'text', True],
            ['nom_tip', 'Tipo de Unidad', 'Nombre', 'text', True],
        ],
        "field_search": [ 
            [ 'mo.nombre' , 'mar.nombre' , 'tip.nombre' ], 
            'nombre, marca del modelo o tipo de unidad del modelo' , 
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
    "unidad": {
        "active" : True ,
        "titulo": "unidades",
        "nombre_tabla": "unidad",
        "controlador": controlador_unidad,
        "main_column": 'placa',
        "filters": [
            ['activo', f'Actividad', get_options_active() ],
            ['modeloid', 'Modelo', controlador_modelo.get_options() ],
        ] ,
        "fields_insert": [
            ['placa', 'Placa', 'Placa', 'text', True , True ],
            ['capacidad', 'Capacidad', 'Capacidad', 'text', True , True ],
            ['volumen', 'Volumen', 'Volumen', 'number', True , None ],
            ['modeloid', 'Modelo', 'Elegir modelo', 'select', True , controlador_modelo.get_options() ],
            ['observaciones', 'Observaciones', 'observaciones', 'textarea', False , None ],
        ],
        "fields_update": [
            ['placa', 'Placa', 'Placa', 'text', True , None ],
            ['capacidad', 'capacidad', 'capacidad', 'text', True , None ],
            ['volumen', 'volumen', 'volumen', 'text', True , None ],
            ['modeloid', 'Modelo', 'Elegir modelo', 'select', True , controlador_modelo.get_options() ],
            ['observaciones', 'observaciones', 'observaciones', 'textarea', False , None ],
        ],
        "fields_consult": [
            ['placa', 'Placa', 'Placa', 'text', True , None ],
            ['activo', f'{TITLE_STATE}', 'activo', 'p', True , None ],
            ['nom_modelo', 'Nombre del Modelo', 'modeloid', 'text', True , None ],
            ['capacidad', 'Capacidad', 'capacidad', 'text', True , None ],
            ['volumen', 'Volumen', 'volumen', 'text', True , None ],
            ['observaciones', 'Observaciones', 'observaciones', 'textarea', False , None ],
        ],
        "field_search": [ 
            # ['ud.placa' , 'mo.nombre' ], 
            ['placa' , 'nom_mod' ], 
            'placa o modelo de unidad' , 
            10
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


MENU_ADMIN = {
    'encomienda' : {
        'name' : 'Encomiendas',
        'active': True ,
        'icon_page' : '',
        'dashboard' : False,
        'cruds' :     [  ],
        'reports' :   [  ],
    },
    'administracion' : {
        'name' : 'Administración',
        'active': True ,
        'icon_page' : '',
        'dashboard' : False,
        'cruds' :     [ 'tipo_unidad' , 'marca' , 'modelo' , 'unidad' ],
        # 'reports' :   [ '' ],
    },
    'logistica' : {
        'name' : 'Logística',
        'active': True ,
        'icon_page' : '',
        'dashboard' : False,
        'cruds' :     [  ],
        'reports' :   [  ],
    },
    'ventas' : {
        'name' : 'Ventas',
        'active': True ,
        'icon_page' : '',
        'dashboard' : False,
        'cruds' :     [  ],
        'reports' :   [  ],
    },
    'personal' : {
        'name' : 'Personal',   
        'active': True ,
        'icon_page' : '',
        'dashboard' : False,
        'cruds' :     [  ],
        'reports' :   [  ],
    },
    'seguridad' : {
        'name' : 'Seguridad',
        'active': True ,
        'icon_page' : '',
        'dashboard' : False,
        'cruds' :     [  ],
        # 'reports' :   [ '' ],
    },
    'atencion' : {
        'name' : 'Atención al Cliente',
        'active': True ,
        'icon_page' : '',
        'dashboard' : False,
        'cruds' :     [  ],
        'reports' :   [  ],
    },
}


###########_ REDIRECT _#############

@app.route("/")
def main_page():
    return redirect(url_for('dashboard'))


@app.context_processor
def inject_globals():
    lista_paginas_crud = listar_paginas_crud()
    listar_pages_admin = listar_admin_pages()
    options_pagination_crud , selected_option_crud = get_options_pagination_crud()

    return dict(
        info_variables_crud = True,
        lista_paginas_crud = lista_paginas_crud ,
        listar_pages_admin = listar_pages_admin,
        options_pagination_crud = options_pagination_crud ,
        selected_option_crud = selected_option_crud ,

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


paginas_simples = [ "index" , 'login' , 'sign_up' , 'dashboard']

for pagina in paginas_simples:
    app.add_url_rule(
        f"/{pagina}",  # URL
        pagina,        # Nombre de la función
        lambda p=pagina: render_template(f"{p}.html")  # Renderiza la plantilla
    )


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

    titulo = config["titulo"]
    controlador = config["controlador"]
    nombre_tabla = config["nombre_tabla"]
    main_column = config["main_column"]
    filters = config["filters"]
    fields_insert = config["fields_insert"]
    fields_update = config["fields_update"]
    fields_consult = config["fields_consult"]
    field_search = config["field_search"]
    
    resultados = controlador.table_fetchall()
    existe_activo = controlador.exists_Activo()
    columnas , filas = controlador.get_table(field_search[0] , value_search)
    info_columns = controlador.get_info_columns()
    primary_key = controlador.get_primary_key()
    table_columns  = list(filas[0].keys()) if filas else []
    # print(filas)
    # print(table_columns)

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
        titulo         = titulo ,
        filas          = filas ,
        primary_key    = primary_key ,
        resultados     = resultados,
        filters        = filters,
        fields_insert  = fields_insert ,
        fields_update  = fields_update ,
        fields_consult = fields_consult ,
        field_search   = field_search ,
        value_search   = value_search,
        columnas       = columnas ,
        main_column    = main_column,
        key_columns    = list(columnas.keys()) ,
        # bd_columns     = list(resultados[0].keys()) if resultados else [] ,
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
def crud_insert(tabla):
    # try:
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
            if nombre != '' :
                valor = request.form.get(nombre)
                if requerido and not valor:
                    return f"Campo {nombre} es obligatorio", 400
                valores.append(str(valor))

        controlador.insert_row( *valores )

        return redirect(url_for('crud_generico', tabla = tabla))
    # except Exception as e:
    #     return f"No se aceptan carácteres especiales", 400


@app.route("/delete_row=<tabla>", methods=["POST"])
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


@app.route("/update_row=<tabla>", methods=["POST"])
def crud_update(tabla):
    # try:
        config = CONTROLADORES.get(tabla)
        if not config:
            return "Tabla no soportada", 404

        active = config["active"]

        if active is False:
            return "Tabla no soportada", 404

        controlador = config["controlador"]
        fields = config["fields_update"]
        primary_key = controlador.get_primary_key()

        valores = []
        valores.append(request.form.get(primary_key))
        for campo in fields:
            nombre = campo[0] 
            requerido = campo[4]
            if nombre != '' :
                valor = request.form.get(nombre)
                if requerido and not valor:
                    return f"Campo {nombre} es obligatorio", 400
                valores.append(valor)

        controlador.update_row( *valores )

        return redirect(url_for('crud_generico', tabla = tabla))
    # except Exception as e:
    #     return f"No se aceptan carácteres especiales", 400








if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)



##################_ _ARCHIVADO_ _################## 
