from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for , after_this_request
from controladores import bd as bd
from controladores import controlador_color as controlador_color
from controladores import controlador_marca as controlador_marca
from controladores import controlador_unidad as controlador_unidad
from controladores import controlador_tipo_unidad as controlador_tipo_unidad
from controladores import controlador_modelo as controlador_modelo
from controladores import controlador_ubigeo as controlador_ubigeo
from controladores import controlador_sucursal as controlador_sucursal
from controladores import controlador_tamaño_caja as controlador_tamaño_caja
from controladores import controlador_tipo_cargo as controlador_tipo_cargo
from controladores import controlador_tipo_paquete as controlador_tipo_paquete
from controladores import controlador_estado_encomienda as controlador_estado_encomienda



import configuraciones
from configuraciones import NOMBRE_BTN_UPDATE , NOMBRE_BTN_UNACTIVE , ACT_STATE_0 , ACT_STATE_1 , FUNCIONES_CRUD , NOMBRE_BTN_CONSULT , NOMBRE_BTN_DELETE , NOMBRE_BTN_INSERT , NOMBRE_BTN_LIST , NOMBRE_BTN_SEARCH , NOMBRE_CRUD_PAGE , NOMBRE_OPTIONS_COL , STATE_0 , STATE_1 , TITLE_STATE, ICON_PAGE_CRUD
from functools import wraps
import inspect
import json
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# import hashlib
# import base64
# from datetime import datetime, date

app = Flask(__name__, template_folder='templates')

SYSTEM_NAME = 'New Olva'

###########_ TEST FUNCIONES _#############

def ingresos_periodo():
    lista = [
        [ 'Enero' , 1520.22 ] , 
        [ 'Febrero' , 1920.21 ] ,
        [ 'Marzo' , 2223.89 ] ,
        [ 'Abril' , 3720.02 ] ,
        [ 'Mayo' , 5220.2 ] ,
    ]

    return lista


def articulos_mas_vendidos():
    lista = [
        [ 'Cajas' , 1520.22 ] , 
        [ 'Sobres' , 6920.21 ] ,
        [ 'Encomiendas' , 2223.89 ] ,
        [ 'Donativos Fabs' , 3720.02 ] ,
        [ 'Contrabando de Arduinos' , 5220.2 ] ,
    ]

    return lista

# ri-layout-grid-fill
# ri-function-line
# ri-layout-4-fill

def datos_usuario():
    lista = {
        'id': 1 ,
        'correo': 'correo@dom.com' ,
        '': 'Nombre Apepat Apemat' ,
        '': 'a' ,
        '': 'Cargo' ,
    }

    return lista


###########_ FUNCIONES _#############

def listar_paginas_crud():
    table_names = list(CONTROLADORES.keys()) #obtiene todas las claves de ese diccionario
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
                    config_page = REPORTES.get(page)
                    if config_page:
                        p_active = config_page.get('active')
                        if p_active is True:
                            p_titulo = config_page.get('titulo')
                            p_icon_page = get_icon_page(config_page.get('icon_page'))
                            pages_report.append([ page , p_titulo , p_icon_page ])
            
            modules.append([ name , icon_module , dashboard , pages_crud , pages_report , module])
    return modules


#Opciones para activar o desacticar
def get_options_active():
    lista = [
        [ 0 , STATE_0 ],
        [ 1 , STATE_1 ],
    ]
    return lista

#Opciones de paginación 
def get_options_pagination_crud():
    lista = [ 5 , 10 , 15 , 20 , 25  ]
    selected_option_crud = 20
    return lista , selected_option_crud

#Manejo de errores
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

#Obtiene el ícono, si no hay, retorna uno por defecto
def get_icon_page(icon):
    if not icon or icon == '':
        return ICON_PAGE_CRUD 
    else:
        return icon 


def extract_col_row(lista):
    columns = []
    rows = []

    for c , r in lista:
        columns.append( c )
        rows.append( r )

    return [columns , rows]



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
        "icon_page": 'fa-solid fa-truck-plane',
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
        "icon_page": 'fa-solid fa-car-side',
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
        "icon_page": 'fa-solid fa-cogs',
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
        "icon_page": 'fa-solid fa-truck-fast',
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
    "ubigeo" : {
        "active":True,
        "titulo":"Ubigeo",
        "nombre_tabla":"ubigeo",
        "controlador": controlador_ubigeo,
        "icon_page" : "ri-map-pin-line",
        "filters":[],
        "fields_form": [
#            ID/NAME   LABEL     PLACEHOLDER   TYPE     REQUIRED   ABLE/DISABLE   DATOS
            ['codigo','Código',     'Código',  'text',   True ,       False ,      None ],
            ['distrito', 'Distrito', 'Distrito',   'text',  True ,      True ,         None ],
            ['provincia', 'Provincia', 'Provincia',   'text',  True ,      True ,         None ],
            ['departamento', 'Departamento', 'Departamento',   'text',  True ,      True ,         None ],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": True ,
            "crud_consult": True ,
            "crud_insert": False ,
            "crud_update": False ,
            "crud_delete": False ,
            "crud_unactive": False ,
        }
    },
    "sucursal" : {
        "active":True,
        "titulo":"Sucursal",
        "nombre_tabla":"sucursal",
        "controlador": controlador_sucursal,
        "icon_page" : "ri-store-3-line",
        "filters":[
            ],
        "fields_form": [
        #         ID/NAME         LABEL             PLACEHOLDER        TYPE       REQUIRED   ABLE/DISABLE   DATOS
            ['id',            'ID',              'ID',              'text',      True ,    False,         True ],
            ['direccion',     'Dirección',       'Dirección',       'text',     True,       True,         None ],
            ['ubigeocodigo',  'Ubigeo',          'Elegir ubigeo',   'select',     True,       True,         [controlador_ubigeo.get_options() , 'ubigeo' ] ],
            ['horario_l_v',   'Horario L-V',     'Ej: 9am - 6pm',   'text',     False,      True,         None ],
            ['horario_s_d',   'Horario S-D',     'Ej: 9am - 1pm',   'text',     False,      True,         None ],
            ['latitud',       'Latitud',         'Latitud',         'text',   False,      True,         None ],
            ['longitud',      'Longitud',        'Longitud',        'text',   False,      True,         None ],
            ['teléfono',      'Teléfono',        'Teléfono',        'text',     False,      True,         None ],
            ['referencia',    'Referencia',      'Referencia',      'text',     False,      True,         None ],
            ['activo',        f'{TITLE_STATE}',  'activo',          'p',         True ,     False,          None ],
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
    "tamaño_caja": {
        "active" : True ,
        "titulo": "tamaños de cajas",
        "nombre_tabla": "tamaño de caja",
        "controlador": controlador_tamaño_caja,
        "icon_page": 'fa-solid fa-box-open',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',          'ID',              'ID',          'text',     True ,     False ,        None ],
            ['nombre',      'Nombre',          'Nombre',      'text',     True ,     True  ,        None ],
            ['activo',      f'{TITLE_STATE}',  'Activo',      'p',        True ,     False ,        None ],
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
    "estado_encomienda": {
        "active" : True ,
        "titulo": "estados de encomiendas",
        "nombre_tabla": "estado de encomienda",
        "controlador": controlador_estado_encomienda,
        "icon_page": 'fa-solid fa-boxes-packing',
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
    "tipo_cargo": {
        "active" : True ,
        "titulo": "tipos de cargos",
        "nombre_tabla": "tipo de cargo",
        "controlador": controlador_tipo_cargo,
        "icon_page": 'ri-file-user-fill',
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
    "tipo_paquete": {
        "active" : True ,
        "titulo": "tipos de paquetes",
        "nombre_tabla": "tipo de paquete",
        "controlador": controlador_tipo_paquete,
        "icon_page": 'ri-box-3-fill',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',          'ID',              'ID',          'text',     True ,     False ,        None ],
            ['nombre',      'Nombre',          'Nombre',      'text',     True ,     True  ,        None ],
            ['activo',      f'{TITLE_STATE}',  'Activo',      'p',        True ,     False ,        None ],
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


REPORTES = {
    # LINEA
    "ingresos_periodo": {
        "active": True,
        'icon_page' : 'fa-solid fa-dollar-sign' ,
        "titulo": "ingresos por mes",
        "elements": {
            "graph": True,
            "table": False,
            "counter": False,
        },
        "graph": {
            "chart": {
                "type": 'line',
                "zoom": {
                    "enabled": True
                }
            },
            "series": [{
                "name": 'Ingresos',
                "data": extract_col_row(ingresos_periodo())[1]
            }],
            "xaxis": {
                "categories": extract_col_row(ingresos_periodo())[0]
            },
            "colors": [' var(--color1) '],
            "stroke": {
                "curve": 'smooth'
            },
            "markers": {
                "size": 5
            }
        },
    },
    # BARRA VERTICAL
    "articulos_mas_vendidos": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-dollar-sign' ,
        "titulo": "artículos más vendidos",
        "elements": {
            "graph": True,
            "table": False,
            "counter": False,
        },
        "graph" : {
            "chart": {
                "type": 'bar',
            },
            "series": [{
                "name": 'Ingresos',
                "data": extract_col_row(articulos_mas_vendidos())[1]
            }],
            "xaxis": {
                "categories": extract_col_row(articulos_mas_vendidos())[0]
            },
            "colors": [' var(--color15) ']
        }
    },
    # BARRA HORIZONTAL
    "top_envios": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-dollar-sign' ,
        "titulo": "top de envios de encomiendas",
        "elements": {
            "graph": True,
            "table": False,
            "counter": False,
        },
        "graph" : {
            "chart": {
                "type": 'bar',
            },
            "series": [{
                "name": 'Envíos',
                "data": [400, 350, 300, 200] 
            }],
            "xaxis": {
                "categories": ['Sucursal A', 'Sucursal B', 'Sucursal C', 'Sucursal D']
            },
            "plotOptions": {
                "bar": {
                    "horizontal": True,
                }
            },
            "colors": [' var(--color5) ']
        }
    },
    # PASTEL
    "envios_tipo": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-dollar-sign' ,
        "titulo": "envios por tipo de articulo",
        "elements": {
            "graph": True,
            "table": False,
            "counter": False,
        },
        "graph" : {
            "chart": {
                "type": 'pie',
                "height": 500,
                "toolbar": {
                    "show": True
                }
            },
            "series": [55, 30, 15],
            "labels": ['Cajas', 'Sobres', 'Otros'],
            "colors": [' var(--color8) ', ' var(--color11) ', ' var(--color-sec) '],
            "responsive": [{
                "breakpoint": 200,
                "options": {
                    "chart": {
                        "width": 100
                    },
                    "legend": {
                        "position": 'bottom'
                    }
                }
            }]
        }
    },
    # DONUT
    "entregado_pendiente": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-dollar-sign' ,
        "titulo": "encomiendas entregadas vs pendientes",
        "elements": {
            "graph": True,
            "table": False,
            "counter": False,
        },
        "graph" : {
            "chart": {
                "type": 'donut',
                "height": 500,
                "toolbar": {
                    "show": True,
                }
            },
            "series": [70, 30] ,
            "labels": ['Entregadas', 'Pendientes'],
            "colors": [' var(--color3) ', ' var(--color-sec) '],
            "responsive": [{
                "breakpoint": 480,
                "options": {
                    "chart": {
                        "height": 100,
                    },
                    "legend": {
                        "position": 'bottom'
                    }
                }
            }]
        },
    },
    # LISTADO
    "lista_unidades": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-dollar-sign' ,
        "titulo": "unidades",
        "elements" : {
            'graph'  : False ,
            'table'  : True,
            'counter': False ,
        } ,
        "table" : controlador_unidad.get_report_test(),
    },
}


MENU_ADMIN = {
    'administracion' : {
        'name' : 'Administración',
        'active': True ,
        'icon_page' : 'fa-solid fa-user-tie',
        'dashboard' : True,
        'cruds' :     [ 'tipo_unidad' , 'marca' , 'modelo' , 'unidad' , 'sucursal'],
        'reports' :   [ 
            'ingresos_periodo' , 
            ''
        ],
    },
    'logistica' : {
        'name' : 'Logística',
        'active': True ,
        'icon_page' : 'fa-solid fa-truck-front',
        'dashboard' : True,
        'cruds' :     [ 'ubigeo' ],
        'reports' :   [ 'lista_unidades' ],
    },
    'encomienda' : {
        'name' : 'Encomiendas',
        'active': True ,
        'icon_page' : 'fa-solid fa-box',
        'dashboard' : True,
        'cruds' :     [ 'estado_encomienda','tipo_paquete' ],
        'reports' :   [ 'top_envios' , 'envios_tipo' , 'entregado_pendiente' ],
    },
    'atencion' : {
        'name' : 'Atención al Cliente',
        'active': True ,
        'icon_page' : 'fa-solid fa-circle-question',
        'dashboard' : True,
        'cruds' :     [  ],
        'reports' :   [ ],
    },
    'ventas' : {
        'name' : 'Ventas',
        'active': True ,
        'icon_page' : 'fa-solid fa-file-invoice-dollar',
        'dashboard' : True,
        'cruds' :     ['tamaño_caja' ],
        'reports' :   [ 'articulos_mas_vendidos'  ],
    },
    'seguridad' : {
        'name' : 'Seguridad',
        'active': True ,
        'icon_page' : 'fa-solid fa-shield-halved',
        'dashboard' : True,
        'cruds' :     [  ],
        'reports' :   [  ],
    },
    'personal' : {
        'name' : 'Personal',   
        'active': True ,
        'icon_page' : 'fa-solid fa-briefcase',
        'dashboard' : True,
        'cruds' :     [ 'tipo_cargo' ],
        'reports' :   [  ],
    },
}


###########_ REDIRECT _#############

@app.route("/")
def main_page():
    return redirect(url_for('index'))


def admin_page():
    return redirect(url_for('panel'))


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
    listar_pages_admin = listar_admin_pages()
    options_pagination_crud , selected_option_crud = get_options_pagination_crud()
    cookie_error = request.cookies.get('error')
    info_variables_crud = False
    HABILITAR_ICON_PAGES = True
    modulo_actual = ''

    return dict(
        info_variables_crud = info_variables_crud,
        lista_paginas_crud = lista_paginas_crud ,
        listar_pages_admin = listar_pages_admin,
        options_pagination_crud = options_pagination_crud ,
        selected_option_crud = selected_option_crud ,
        cookie_error = cookie_error,
        modulo_actual = modulo_actual ,

        MENU_ADMIN = MENU_ADMIN,
        HABILITAR_ICON_PAGES = HABILITAR_ICON_PAGES,
        SYSTEM_NAME = SYSTEM_NAME,
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
        ICON_PAGE_CRUD      = configuraciones.ICON_PAGE_CRUD ,
        ICON_PAGE_REPORT    = configuraciones.ICON_PAGE_REPORT ,
        ICON_PAGE_DASHBOARD = configuraciones.ICON_PAGE_DASHBOARD ,
    )


paginas_simples = [ 
    "index" , 
    'login' , 
    'sign_up', 
    'sucursales' ,
    'tracking',
    'seguimiento'
]

for pagina in paginas_simples:
    app.add_url_rule(
        f"/{pagina}",  # URL
        pagina,        # Nombre de la función
        lambda p=pagina: render_template(f"{p}.html")  # Renderiza la plantilla
    )



@app.route("/panel")
def panel():
    return render_template('panel.html')



##################_ ADMIN PAGE _################## 

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
    filters = config["filters"]
    fields_form = config["fields_form"]

    existe_activo = controlador.exists_Activo()
    columnas , filas = controlador.get_table()
    info_columns = controlador.get_info_columns()
    primary_key = controlador.get_primary_key()
    table_columns  = list(filas[0].keys()) if filas else []
    
    CRUD_FORMS = config["crud_forms"]
    crud_list = CRUD_FORMS.get("crud_list")
    crud_search = CRUD_FORMS.get("crud_search")
    crud_consult = CRUD_FORMS.get("crud_consult")
    crud_insert = CRUD_FORMS.get("crud_insert")
    crud_update = CRUD_FORMS.get("crud_update")
    crud_delete = CRUD_FORMS.get("crud_delete")
    crud_unactive = CRUD_FORMS.get("crud_unactive") and existe_activo


    return render_template(
        "CRUD.html" ,
        tabla          = tabla ,
        nombre_tabla   = nombre_tabla ,
        icon_page_crud = icon_page_crud ,
        titulo         = titulo ,
        filas          = filas ,
        primary_key    = primary_key ,
        filters        = filters,
        fields_form    = fields_form ,
        value_search   = value_search,
        columnas       = columnas ,
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


@app.route("/dashboard=<module_name>")
def dashboard(module_name):
    info_modulo = MENU_ADMIN.get(module_name)

    for page in listar_admin_pages():
        if module_name == page[5] and page[2] is True:
            modulo = page

    return render_template(
        'dashboard.html' , 
        module_name = module_name , 
        modulo = modulo ,
        info_modulo = info_modulo,
        )


@app.route("/reporte=<report_name>")
def reporte(report_name):
    config = REPORTES.get(report_name)
    if not config:
        return "Reporte no encontrado", 404

    active = config["active"]

    if active is False:
        return "Reporte no encontrado", 404
        
    titulo = 'Reporte de ' + config.get("titulo")
    elements = config.get("elements")
    e_graph = elements.get('graph')
    e_table = elements.get('table')
    e_counter = elements.get('counter')
    icon_page = get_icon_page(config.get("icon_page"))
    graph = config.get("graph")
    table = config.get("table")
    columnas = None
    filas = None
    if table is not None and e_table is True:
        columnas , filas = table

    counter = config.get("counter")

    return render_template(
        "REPORTE.html" ,
        titulo = titulo ,
        elements = elements ,
        e_graph = e_graph,
        e_table = e_table,
        e_counter = e_counter,
        graph = graph ,
        table = table ,
        columnas = columnas,
        filas = filas,
        counter = counter ,
        icon_page = icon_page,
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

<<<<<<< HEAD
########################################################################
@app.route("/dashboard=<modulo>")
def dashboard(modulo):
    return render_template('dashboard.html')
    # return f'Aca hay un dashboard del modulo de {modulo}'


@app.route("/reporte=<report_name>")
def reporte(report_name):
    config = REPORTES.get(report_name)
    if not config:
        return "Reporte no encontrado", 404

    active = config["active"]

    if active is False:
        return "Reporte no encontrado", 404
        
    titulo = 'Reporte de ' + config.get("titulo")
    elements = config.get("elements")
    icon_page = get_icon_page(config.get("icon_page"))
    graph = config.get("graph")
    table = config.get("table")
    counter = config.get("counter")

    return render_template(
        "REPORTE.html" ,
        titulo = titulo ,
        elements = elements ,
        graph = graph ,
        table = table ,
        counter = counter ,
        icon_page = icon_page,
    )




@app.route("/panel")
def panel():

    return render_template('panel.html')

@app.route("/faq")
def Faq():

    return render_template('Faq.html')

@app.route("/contactanos")
def contac():

    return render_template('contactanos.html')

@app.route("/cajas")
def cajas():

    return render_template('cajas.html')

@app.route("/articulos")
def articulos():

    return render_template('articulos.html')



=======
>>>>>>> e505fbdd8f4474cec7ea33dc7c562817bb53350b






@app.route("/colores")
def colores():
    html = '''
    <link rel="stylesheet" href="../static/css/common_styles/common_style.css" />
    <style>
        body {
            display: flex;
            flex-wrap: wrap;
            margin: 0;
            gap: 0;
            align-content: flex-start;
            background: grey;
        }
        .color_block {
            border: 1px solid black;
            display: flex;
            flex-direction: column;
            height: 100px;
            width:  9.85vw;
            font-size: 15px;
        }
    </style>    
'''
    for color in ['-base' , '-sec' , '-contrast']:
        text = f'--color{color}'
        html += f'''
        <div class="color_block">
        <p>{text}</p> 
        <div style="height: 100%; width: 100%; background-color: var({text})"></div>
        </div>
    '''
    for color in range(25):
        text = f'--color{color}'
        html += f'''
        <div class="color_block">
        <p>{text}</p> 
        <div style="height: 100%; width: 100%; background-color: var({text})"></div>
        </div>
    '''
    return html




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)



##################_ _ARCHIVADO_ _################## 
