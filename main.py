from flask import Flask, render_template, request, redirect, make_response, url_for , g,jsonify,json  #, after_this_request, flash, jsonify, session
from controladores import bd as bd 
from controladores import permiso as permiso
from controladores import controlador_pagina as controlador_pagina
from controladores import controlador_detalle_reclamo as controlador_detalle_reclamo
from controladores import controlador_paquete as controlador_paquete
from controladores import controlador_tipo_pagina as controlador_tipo_pagina
from controladores import controlador_modulo as controlador_modulo
from controladores import controlador_empresa as controlador_empresa
from controladores import controlador_color as controlador_color
from controladores import controlador_marca as controlador_marca
from controladores import controlador_unidad as controlador_unidad
from controladores import controlador_tipo_unidad as controlador_tipo_unidad
from controladores import controlador_modelo as controlador_modelo
from controladores import controlador_ubigeo as controlador_ubigeo
from controladores import controlador_sucursal as controlador_sucursal
from controladores import controlador_tamanio_caja as controlador_tamanio_caja
from controladores import controlador_tipo_rol as controlador_tipo_rol
from controladores import controlador_contenido_paquete as controlador_contenido_paquete
from controladores import controlador_estado_encomienda as controlador_estado_encomienda
from controladores import controlador_tipo_documento as controlador_tipo_documento
from controladores import controlador_tipo_comprobante as controlador_tipo_comprobante
from controladores import controlador_empleado as controlador_empleado
from controladores import controlador_estado_reclamo as controlador_estado_reclamo
from controladores import controlador_metodo_pago as controlador_metodo_pago
from controladores import controlador_tipo_indemnizacion as controlador_tipo_indemnizacion
from controladores import controlador_tipo_reclamo as controlador_tipo_reclamo
from controladores import controlador_motivo_reclamo as controlador_motivo_reclamo
from controladores import controlador_causa_reclamo as controlador_causa_reclamo
from controladores import controlador_tipo_empaque as controlador_tipo_empaque
from controladores import controlador_tipo_recepcion as controlador_tipo_recepcion
from controladores import controlador_tarifa_ruta as controlador_tarifa_ruta
from controladores import controlador_tipo_cliente as controlador_tipo_cliente
from controladores import controlador_usuario as controlador_usuario
from controladores import controlador_cliente as controlador_cliente
from controladores import controlador_rol as controlador_rol
from controladores import controlador_articulo as controlador_articulo
from controladores import controlador_descuento as controlador_descuento
from controladores import controlador_descuento_articulo as controlador_descuento_articulo
from controladores import controlador_salida as controlador_salida
from controladores import controlador_reclamo as controlador_reclamo
from controladores import controlador_preguntas_frecuentes as controlador_pregunta_frecuente
<<<<<<< HEAD
from controladores import controlador_regla_cargo as controlador_regla_cargo

=======
from controladores import reporte_ingresos as reporte_ingresos
>>>>>>> 8cc40e7272df8f6b4fad232eae40ffa4f72304f4


import hashlib
import os
from werkzeug.utils import secure_filename
import re
import configuraciones
from functools import wraps
import inspect
# import json
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# import base64
# from datetime import datetime, date

app = Flask(__name__, template_folder='templates')

STATE_0              = configuraciones.STATE_0
STATE_1              = configuraciones.STATE_1
TITLE_STATE          = configuraciones.TITLE_STATE
HABILITAR_ICON_PAGES = configuraciones.HABILITAR_ICON_PAGES
ACT_STATE_0          = configuraciones.ACT_STATE_0
ACT_STATE_1          = configuraciones.ACT_STATE_1
NOMBRE_CRUD_PAGE     = configuraciones.NOMBRE_CRUD_PAGE
NOMBRE_ADMINPAGES_PAGE = configuraciones.NOMBRE_ADMINPAGES_PAGE 
NOMBRE_OPTIONS_COL   = configuraciones.NOMBRE_OPTIONS_COL
NOMBRE_BTN_INSERT    = configuraciones.NOMBRE_BTN_INSERT
NOMBRE_BTN_UPDATE    = configuraciones.NOMBRE_BTN_UPDATE
NOMBRE_BTN_DELETE    = configuraciones.NOMBRE_BTN_DELETE
NOMBRE_BTN_UNACTIVE  = configuraciones.NOMBRE_BTN_UNACTIVE
NOMBRE_BTN_LIST      = configuraciones.NOMBRE_BTN_LIST
NOMBRE_BTN_CONSULT   = configuraciones.NOMBRE_BTN_CONSULT
NOMBRE_BTN_SEARCH    = configuraciones.NOMBRE_BTN_SEARCH
ICON_PAGE_NOICON     = configuraciones.ICON_PAGE_NOICON 
ICON_PAGE_CRUD       = configuraciones.ICON_PAGE_CRUD 
ICON_PAGE_REPORT     = configuraciones.ICON_PAGE_REPORT 
ICON_PAGE_DASHBOARD  = configuraciones.ICON_PAGE_DASHBOARD 
ICON_PAGE_PANEL      = configuraciones.ICON_PAGE_PANEL 
ICON_LIST            = configuraciones.ICON_LIST
ICON_CONSULT         = configuraciones.ICON_CONSULT
ICON_SEARCH          = configuraciones.ICON_SEARCH
ICON_INSERT          = configuraciones.ICON_INSERT
ICON_UPDATE          = configuraciones.ICON_UPDATE
ICON_DELETE          = configuraciones.ICON_DELETE
ICON_ACTIVE          = configuraciones.ICON_ACTIVE
ICON_UNACTIVE        = configuraciones.ICON_UNACTIVE
ICON_UNLOCK          = configuraciones.ICON_UNLOCK

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


###########_ FUNCIONES _#############

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
                            p_elements = config_page.get('elements')
                            pages_report.append([ page , p_titulo , p_icon_page , p_elements ])
            
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

#Obtiene el ícono, si no hay, retorna uno por defecto
def get_icon_page(icon):
    if not icon or icon == '':
        return ICON_PAGE_CRUD 
    else:
        return icon 

# Convertir lista en tabla de 2 columnas
def extract_col_row(lista):
    columns = []
    rows = []

    for c , r in lista:
        columns.append( c )
        rows.append( r )

    return [columns , rows]

# Encriptar con hashlib
def encrypt_sha256_string(str):
    h = hashlib.new('sha256')
    h.update(bytes(str, encoding='utf-8'))
    encstr = h.hexdigest()
    return encstr

# Crear response para login
def resp_login( url_function , user_id , correo ):
    resp = make_response(redirect_url(url_function))
    resp.set_cookie('user_id', str(user_id))
    resp.set_cookie('correo', correo)
    return resp


def getDatosUsuario():
    user_id = request.cookies.get('user_id')
    correo = request.cookies.get('correo')
    usuario = controlador_usuario.get_usuario_por_id(user_id)
    if usuario and correo and usuario['correo'] == correo:
        return usuario
    else: 
        return None
    

def esSesionIniciada():
    if getDatosUsuario() :
        return True
    else:
        return False
    

# UPLOAD_FOLDER = 'static/uploads/empresa'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def guardar_imagen_bd(tabla,ad,archivo):
    if archivo and '.' in archivo.filename and archivo.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename_seguro = secure_filename(archivo.filename)
        # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # nombre_final = f"{timestamp}_{filename_seguro}"
        upload_folder = f'static/img/img_{tabla}'
        nombre_final = f"{ad}{filename_seguro}"
        print('IMG archivo:',nombre_final)
        ruta_completa = os.path.join(upload_folder, nombre_final)
        archivo.save(ruta_completa)
        return nombre_final
    return None



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
# EDQ
    "tipo_documento": {
        "active" : True ,
        "titulo": "tipos de documentos",
        "nombre_tabla": "tipo de documento",
        "controlador": controlador_tipo_documento,
        "icon_page": 'fa-solid fa-id-card',
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
    "tipo_comprobante": {
        "active" : True ,
        "titulo": "tipos de comprobantes",
        "nombre_tabla": "tipo de comprobante",
        "controlador": controlador_tipo_comprobante,
        "icon_page": 'fa-solid fa-file-lines',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',          'ID',              'ID',          'text',     True ,     False ,        None ],
            ['inicial',          'Inicial',    'Inicial',     'text',     True ,     True ,        None ],
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
    "tipo_indemnizacion": {
        "active": True,
        "titulo": "tipos de indemnización",
        "nombre_tabla": "tipo de indemnización",
        "controlador": controlador_tipo_indemnizacion,
        "icon_page": "fa-solid fa-hand-holding-dollar",
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active()],
        ],
        "fields_form": [
            #  ID/NAME     LABEL             PLACEHOLDER   TYPE     REQUIRED   ABLE/DISABLE   DATOS
            ['id',        'ID',             'ID',          'text',  True,      False,         None],
            ['nombre',    'Nombre',         'Nombre',      'text',  True,      True,          None],
            ['activo',    f'{TITLE_STATE}', 'Activo',      'p',     True,      False,         None],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": True,
        }
    },
    "estado_reclamo": {
        "active" : True ,
        "titulo": "estados de reclamos",
        "nombre_tabla": "estado de reclamo",
        "controlador": controlador_estado_reclamo,
        "icon_page": 'fa-solid fa-circle-exclamation',
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
    "reclamo": {
        "active": True,
        "id": "reclamo",
        "titulo": "Reclamos",
        "nombre_tabla": "reclamo",
        "controlador": controlador_reclamo,  # Asegúrate de importar esto arriba
        "icon_page": "fa-solid fa-file",  # Puedes cambiar el ícono
        "filters": [],
        "fields_form": [
            ['id', 'ID', 'ID', 'text', True, False, None],
            ['nombres_razon', 'Cliente', 'Cliente', 'text', True, True, None],
            ['direccion', 'Dirección', 'Dirección', 'text', True, True, None],
            ['correo', 'Correo', 'Correo', 'email', True, True, None],
            ['telefono', 'Teléfono', 'Teléfono', 'text', True, True, None],
            ['titulo_incidencia', 'Incidencia', 'Incidencia', 'text', True, True, None],
            ['monto_reclamado', 'Monto Reclamado', '0.00', 'number', True, True, None],
            ['fecha_recojo', 'Fecha de recojo', 'Fecha', 'date', True, True, None],
            ['estado_reclamoid', 'Estado', 'Estado', 'select', True, True, [lambda: controlador_estado_reclamo.get_options(), 'nombre']],
            ['sucursal_id', 'Sucursal', 'Sucursal', 'select', True, True, [lambda: controlador_sucursal.get_options(), 'direccion']]
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": False
        }
    },
    "pregunta_frecuente": {
        "active": True,
        "titulo": "preguntas frecuentes",
        "nombre_tabla": "pregunta frecuente",
        "controlador": controlador_pregunta_frecuente,
        "icon_page": 'fa-solid fa-circle-question',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active()],
        ],
        "fields_form": [
            #  ID/NAME          LABEL              PLACEHOLDER            TYPE      REQUIRED  ABLE/DISABLE  DATOS
            ['id',              'ID',              'ID',                  'text',     True,     False,       None],
            ['titulo',          'Título',          'Título',              'text',     True,     True,        None],
            ['descripcion',     'Descripción',     'Descripción',         'textarea', True,     True,        None],
            ['activo',          f'{TITLE_STATE}',  'Activo',              'p',        True,     False,       None],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": True,
        }
    },
  
# LEO
    "tamanio_caja": {
        "active" : True ,
        "titulo": "tamaños de cajas",
        "nombre_tabla": "tamaño de caja",
        "controlador": controlador_tamanio_caja,
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
    "contenido_paquete": {
        "active" : True ,
        "titulo": "contenido de paquetes",
        "nombre_tabla": "contenido de paquete",
        "controlador": controlador_contenido_paquete,
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
    "articulo": {
        "active" : True ,
        "titulo": "articulos para encomiendas",
        "nombre_tabla": "articulo para encomienda",
        "controlador": controlador_articulo,
        "icon_page": 'fa-solid fa-box-open',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',          'ID',              'ID',          'text',     True ,     False ,        None ],
            ['nombre',      'Nombre',          'Nombre',      'text',     True ,     True  ,        None ],
            ['precio',      'Precio',          'Precio',      'number',   True ,     True  ,        None ],
            ['stock',       'Stock',           'Stock',       'number',   True ,     True  ,        None ],
            ['dimensiones', 'Dimensiones',     'Dimensiones', 'text',     False ,     True  ,        None ],
            ['tamaño_cajaid','Tamaño Caja',    'Tamaño Caja', 'select',   False ,     True  ,        [lambda: controlador_tamanio_caja.get_options() , 'tam_nombre' ]  ],
            ['img',         'Imagen',          'Imagen',      'img',      True ,     True  ,        None ],
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
    "tipo_rol": {
        "active" : True ,
        "titulo": "tipos de roles",
        "nombre_tabla": "tipo de rol",
        "controlador": controlador_tipo_rol,
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
    
# FAB
    "motivo_reclamo": {
        "active" : True ,
        "titulo": "Motivo de reclamo",
        "nombre_tabla": "motivo_reclamo",
        "controlador": controlador_motivo_reclamo,
        "icon_page": '',
        "filters": [
            ['tipo_reclamoid', 'Tipo de reclamo', lambda: controlador_tipo_reclamo.get_options() ],
        ] ,
        "fields_form": [
    #            ID/NAME          LABEL               PLACEHOLDER      TYPE         REQUIRED   ABLE/DISABLE   DATOS
            ['id',            'ID',               'ID',            'text',      False ,    False,         True ],
            ['nombre',      'Nombre',          'Nombre',      'text',     True ,     True  ,        None ],
            ['descripcion', 'Descripción',     'descripcion', 'textarea', False,     True  ,        None ],
            ['tipo_reclamoid',  'Nombre de tipo de reclamo', 'Elegir tipo de reclamo', 'select',    True ,     True, [lambda: controlador_tipo_reclamo.get_options() , 'nom_tip' ] ],
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
    "causa_reclamo": {
        "active" : True ,
        "titulo": "Causa de reclamo",
        "nombre_tabla": "causa_reclamo",
        "controlador": controlador_causa_reclamo,
        "icon_page": '',
        "filters": [
            ['motivo_reclamoid', 'Motivo de reclamo', lambda: controlador_motivo_reclamo.get_options() ],
        ] ,
        "fields_form": [
#            ID/NAME          LABEL               PLACEHOLDER      TYPE         REQUIRED   ABLE/DISABLE   DATOS
            ['id',            'ID',               'ID',            'text',      False ,    False,         True ],
            ['nombre',      'Nombre',          'Nombre',      'text',     True ,     True  ,        None ],
            ['descripcion', 'Descripción',     'descripcion', 'textarea', False,     True  ,        None ],
            ['motivo_reclamoid',  'Nombre de motivo de reclamo', 'Elegir motivo de reclamo', 'select', True ,True, [lambda: controlador_motivo_reclamo.get_options() , 'nom_motivo' ] ],
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
    "tarifa_ruta": {
        "active" : True ,
        "titulo": "Tarifas de rutas",
        "nombre_tabla": "tarifa de una ruta",
        "controlador": controlador_tarifa_ruta,
        "icon_page": '',
        "filters": [
        ] ,
        "fields_form": [
#            ID/NAME          LABEL               PLACEHOLDER      TYPE         REQUIRED   ABLE/DISABLE   DATOS
            ['tarifa',      'Tarifa',          'Tarifa',      'decimal_2',     True ,     True  ,        None ],
            ['sucursal_origen_id',  'Sucursal de origen', 'Sucursal de origen', 'select', True ,True, [lambda: controlador_sucursal.get_options() , 'sucursal_origen' ] ],
            ['sucursal_destino_id',  'Sucursal de destino', 'Sucursal de destino', 'select', True ,True, [lambda: controlador_sucursal.get_options() , 'sucursal_destino' ] ],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": False  # Solo si tienes columna 'activo'
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
    #         ID/NAME         LABEL              PLACEHOLDER        TYPE       REQUIRED   ABLE/DISABLE   DATOS
            ['id',            'ID',              'ID',              'text',      True ,    False,      True ],
            ['activo',        f'{TITLE_STATE}',  'activo',          'p',         True ,    False,      None ],
            ['codigo_postal', 'Código Postal',   'Código Postal',   'text',      True ,    True,       'map' ],
            ['abreviatura',   'Abreviatura',     'Abreviatura',     'text',      True ,    True,       None ],
            ['ubigeocodigo',  'Ubigeo',          'Elegir ubigeo',   'select',    True ,    True,       [lambda: controlador_ubigeo.get_options(), 'ubigeo'] ],
            ['direccion',     'Dirección',       'Dirección',       'text',      True ,    True,       'map' ],
            ['teléfono',      'Teléfono',        'Teléfono',        'text',      False,    True,       None ],
            ['horario_l_v',   'Horario L-V',     'Ej: 9am - 6pm',   'text',      False,    True,       None ],
            ['latitud',       'Latitud',         'Latitud',         'decimal_6',    False,    True,       'map' ],
            ['horario_s_d',   'Horario S-D',     'Ej: 9am - 1pm',   'text',      False,    True,       None ],
            ['referencia',    'Referencia',      'Referencia',      'text',      False,    True,       None ],
            ['longitud',      'Longitud',        'Longitud',        'decimal_6',    False,    True,       'map' ],
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
    "tipo_reclamo": {
        "active" : True ,
        "titulo": "tipos de reclamos",
        "icon_page": 'fa-solid fa-book-open-reader',
        "nombre_tabla": "tipo de reclamo",
        "controlador": controlador_tipo_reclamo,
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
    
# JPD
    "metodo_pago": {
        "active": True,
        "titulo": "métodos de pago",
        "nombre_tabla": "método de pago",
        "controlador": controlador_metodo_pago,
        "icon_page": "fa-solid fa-money-bill-wave",
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active()],
        ],
        "fields_form": [
            #  ID/NAME     LABEL             PLACEHOLDER   TYPE     REQUIRED   ABLE/DISABLE   DATOS
            ['id',        'ID',             'ID',          'text',  True,      False,         None],
            ['nombre',    'Nombre',         'Nombre',      'text',  True,      True,          None],
            ['activo',    f'{TITLE_STATE}', 'Activo',      'p',     True,      False,         None],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": True,
        }
    },
    "empleado": {
        "active": True,
        "titulo": "empleados",
        "nombre_tabla": "empleado",
        "controlador": controlador_empleado,
        "icon_page": 'fa-solid fa-id-card',
        "filters": [
            # ['rolid', 'Rol', lambda: controlador_rol.get_options()],
        ],
        "fields_form": [
            ['usuarioid', 'ID', 'ID', 'text', False, False, True],
            ['nombre', 'Nombre', 'Nombre', 'text', True, True, True],
            ['apellidos', 'Apellidos', 'Apellidos', 'text', True, True, True],
            ['correo', 'Correo electrónico', 'Correo', 'email', True, True, True],
            ['rolid', 'Rol', 'Seleccionar rol', 'select', True, True, [lambda: controlador_rol.get_options(), 'nombre']],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": False
        }
    },
    "tipo_cliente": {
        "active" : True ,
        "titulo": "tipos de clientes",
        "nombre_tabla": "tipo de cliente",
        "controlador": controlador_tipo_cliente,
        "icon_page": 'fa-solid fa-layer-group',
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
    "usuario": {
        "active" : True ,
        "titulo": "Usuarios",
        "nombre_tabla": "usuario",
        "controlador": controlador_usuario,
        "icon_page": 'fa-solid fa-user',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',          'ID',              'ID',          'text',     True ,     False ,        None ],
            ['correo',      'correo',          'Correo',      'text',     True ,     True  ,        None ],
            ['contrasenia',      'contrasenia',          'Contraseña',      'password',     True ,     True  ,        None ],
            ['tipo_usuario',      'tipo_usuario',          'Tipo de usuario',      'text',     True ,     True  ,        None ],
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
    "cliente": {
        "active": True,
        "titulo": "clientes",
        "nombre_tabla": "cliente",
        "controlador": controlador_cliente,
        "icon_page": 'fa-solid fa-user',
        "filters": [
            ['tipo_documentoid', 'Tipo de documento', lambda: controlador_tipo_documento.get_options()],
            ['tipo_clienteid', 'Tipo de cliente', lambda: controlador_tipo_cliente.get_options()],
        ],
        "fields_form": [
            # ID/NAME           LABEL                    PLACEHOLDER          TYPE        REQUIRED  ENABLE      DATOS
            ['id',       'ID',                    'ID',                'text',     False,    False,      True ],
            ['nombre_siglas',   'Nombre o Siglas',       'Nombre',            'text',     True,     True,       True ],
            ['apellidos_razon', 'Apellidos/Razón Social','Apellidos o razón', 'text',     True,     True,       True ],
            ['correo',          'Correo',                'Correo electrónico','email',    True,     True,       True ],
            ['telefono',        'Teléfono',              'Teléfono',          'text',     False,    True,       True ],
            ['num_documento',   'N° Documento',          'Número doc.',       'text',     True,     True,       True ],
            ['tipo_documentoid','Tipo de Documento',     'Seleccionar',       'select',   True,     True,       [lambda: controlador_tipo_documento.get_options(), 'siglas'] ],
            ['tipo_clienteid',  'Tipo de Cliente',       'Seleccionar',       'select',   True,     True,       [lambda: controlador_tipo_cliente.get_options(), 'nombre'] ],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": False  # Solo si tienes columna 'activo'
        }
    },
    "rol": {
        "active": True,
        "titulo": "roles",
        "nombre_tabla": "rol",
        "controlador": controlador_rol,
        "icon_page": 'fa-solid fa-user-shield',
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active()],
            ['tipo_rolid', 'Tipo de Rol', lambda: controlador_tipo_rol.get_options()],
        ],
        "fields_form": [
            ['id', 'ID', 'ID', 'text', False, False, True],
            ['nombre', 'Nombre del Rol', 'Rol', 'text', True, True, True],
            ['descripcion', 'Descripción', 'Descripción del rol', 'textarea', False, True, None],
            ['activo', f'{TITLE_STATE}', 'activo', 'p', True, True, None],
            ['tipo_rolid', 'Tipo de Rol', 'Seleccionar', 'select', True, True, [lambda: controlador_tipo_rol.get_options(), 'nombre']],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": True
        }
    },

# FCV
    "tipo_unidad": {
        "active" : True ,
        "titulo": "tipos de unidades",
        "icon_page": 'fa-solid fa-truck-plane',
        "nombre_tabla": "tipo de unidad",
        "controlador": controlador_tipo_unidad,
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
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME   LABEL     PLACEHOLDER  TYPE     REQUIRED   ABLE/DISABLE   DATOS
            ['id',     'ID',     'ID',        'text',  True ,     False ,        None ],
            ['nombre', 'Nombre', 'Nombre',    'text',  True ,     True ,         None ],
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
    "modelo": {
        "active" : True ,
        "titulo": "modelos de unidades",
        "nombre_tabla": "modelo",
        "controlador": controlador_modelo,
        "icon_page": 'fa-solid fa-cogs',
        "filters": [
        ] ,
        "fields_form": [
#            ID/NAME            LABEL               PLACEHOLDER         TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',              'ID',               'ID',               'text',     False ,    False ,        None ],
            ['nombre',          'Nombre',           'Nombre',           'text',     True ,     True ,         None ],
            ['activo',      f'{TITLE_STATE}',  'Activo',      'p',        True ,     False ,        None ],
            ['marcaid',         'Marca',            'Marca',            'select',   True ,     None,          [lambda: controlador_marca.get_options_marca() , 'nom_mar'] ],
            ['tipo_unidadid',   'Tipo de Unidad',   'Tipo de Unidad',   'select',   True ,     None ,         [lambda: controlador_tipo_unidad.get_options() , 'nom_tip'] ],
            # ['marcaid',         'Marca',            'Marca',            'select',   True ,     None,          [controlador_marca.get_options_marca() , 'nom_mar'] ],
            # ['tipo_unidadid',   'Tipo de Unidad',   'Tipo de Unidad',   'select',   True ,     None ,         [controlador_tipo_unidad.get_options() , 'nom_tip'] ],
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
            ['modeloid', 'Modelo', lambda: controlador_modelo.get_options() ],
        ] ,
        "fields_form": [
#            ID/NAME          LABEL               PLACEHOLDER      TYPE         REQUIRED   ABLE/DISABLE   DATOS
            ['id',            'ID',               'ID',            'text',      False ,    False,         True ],
            ['modeloid',      'Nombre de Modelo', 'Elegir modelo', 'select',    True ,     True,          [lambda: controlador_modelo.get_options() , 'nom_modelo' ] ],
            ['estado',        'Estado',           'Elegir estado', 'select',    True ,    True,           [lambda: controlador_unidad.get_options_estado() , 'estado' ]  ],
            ['placa',         'Placa',            'Placa',         'text',      True ,     True,          True ],
            ['mtc',           'MTC',              'MTC',           'text',      True ,     True,          True ],
            ['tuc',           'TUC',              'TUC',           'text',      True ,     True,          True ],
            ['capacidad',     'Capacidad',        'Capacidad',     'number',    True ,     True,          True ],
            ['volumen',       'Volumen',          'Volumen',       'number',    True ,     True,          None ],
            ['descripcion', 'Descripción',    'Descripción', 'textarea',  False,     True,          None ],
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
    "tipo_empaque": {
        "active" : True ,
        "titulo": "tipos de empaques para paquetes",
        "icon_page": 'fa-solid fa-truck-plane',
        "nombre_tabla": "tipo de empaque",
        "controlador": controlador_tipo_empaque,
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',           'ID',               'ID',          'text',     True ,     False ,        None ],
            ['nombre',       'Nombre',           'Nombre',      'text',     True ,     True  ,        None ],
            ['activo',      f'{TITLE_STATE}',  'Activo',      'p',        True ,     False ,        None ],
            ['peso_maximo',  'Peso Máximo',      'Peso Máximo',      'number',     True ,     True  ,        None ],
            ['unidad_medida','Unidad de Medida', 'Unidad de Medida',      'text',     True ,     True  ,        None ],
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
    "tipo_recepcion": {
        "active" : True ,
        "titulo": "tipos de recepción de paquetes",
        "icon_page": 'fa-solid fa-truck-plane',
        "nombre_tabla": "tipo de recepción de paquete",
        "controlador": controlador_tipo_recepcion,
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
    "detalle_reclamo": {
        "active" : True ,
        "titulo": "detalles de estados de reclamo",
        "icon_page": 'fa-solid fa-file',
        "nombre_tabla": "detalle de un estado de reclamo",
        "controlador": controlador_detalle_reclamo,
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id', 'ID', 'ID', 'text', False, False, True],
            ['nombre', 'Nombre del Rol', 'Rol', 'text', True, True, True],
            ['descripcion', 'Descripción', 'Descripción del rol', 'textarea', False, True, None],
            ['activo', f'{TITLE_STATE}', 'activo', 'p', True, True, None],
            ['estado_reclamoid', 'Estado de reclamo', 'Seleccionar', 'select', True, True, [lambda: controlador_estado_reclamo.get_options(), 'est_nom' ]],
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

    # huh?
    "descuento": {
        "active" : True ,
        "titulo": "Descuentos",
        "icon_page": 'fa-solid fa-percent',
        "nombre_tabla": "Descuentos",
        "controlador": controlador_descuento,
        "filters": [
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['id',          'ID',              'ID',          'text',     True ,     False ,        None ],
            ['nombre',      'Nombre',          'Nombre',      'text',     True ,     True  ,        None ],
            ['descripcion', 'Descripcion',      'Descripcion','text',     True ,     True  ,  None ],
            ['fecha_inicio',   'Fecha de inicio',    'Fecha de inicio',      'date',     True ,     True  ,        None ],
            ['fecha_fin',   'Fecha de fin',    'Fecha de fin',      'date',     True ,     True  ,        None ],
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
    "descuento_articulo": {
        "active" : True ,
        "titulo": "Descuentos de artículos",
        "icon_page": 'fa-solid fa-percent',
        "nombre_tabla": "Descuentos",
        "controlador": controlador_descuento_articulo,
        "filters": [
            ['articuloid', 'Articulo', lambda: controlador_articulo.get_options() ],
                        ['descuentoid', 'Descuento', lambda: controlador_descuento.get_options()]
        ] ,
        "fields_form": [
#            ID/NAME       LABEL              PLACEHOLDER    TYPE        REQUIRED   ABLE/DISABLE   DATOS
            ['descuentoid', 'Descuento',    'Seleccione un descuento',    'select',     True ,     False ,         [lambda: controlador_descuento.get_options() , 'nom_descuento' ] ],
            ['articuloid', 'Articulo',    'Seleccione un articulo',    'select',     True ,     False ,         [lambda: controlador_articulo.get_options() , 'nom_articulo' ] ],
            ['cantidad_descuento',      'Cantidad descontada',          '30%',      'number',     True ,     True  ,        None ],
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

# ADICIONAL (NO CRUD)
    "modulo": {
        "active" : True ,
        # "titulo": "marcas de unidades",
        # "nombre_tabla": "marca",
        "controlador": controlador_modulo,
        # "icon_page": 'fa-solid fa-car-side',
        # "filters": [
        # ] ,
        "fields_form" : [
        #   ID/NAME    LABEL              PLACEHOLDER    TYPE       REQUIRED   ABLE/DISABLE   DATOS
            ['nombre', 'Nombre del módulo', 'Nombre',   'text',    True ,     True,          None ],
            ['activo', 'Actividad',         'Color',    'p',       True,      True,          None ],
            ['icono',  'Icono',             'Icono',    'icon',    True ,     True,          None ],
            ['color',  'Color',             'color',    'color',   True,      True,          None ],
            ['img',  'Imagen',             'Imagen',    'img',   True,      True,          None ],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": True ,
            "crud_consult": True ,
            "crud_insert": True ,
            "crud_update": True ,
            "crud_delete": True ,
            "crud_unactive": True ,
        },
        "no_crud" : 'administrar_paginas' ,
    },
    "pagina": {
        "active" : True ,
        # "titulo": "marcas de unidades",
        # "nombre_tabla": "marca",
        "controlador": controlador_pagina,
        # "icon_page": 'fa-solid fa-car-side',
        # "filters": [
        # ] ,
        "fields_form" : [
        #   ID/NAME    LABEL              PLACEHOLDER    TYPE       REQUIRED   ABLE/DISABLE   DATOS
            ['nombre', 'Nombre del módulo', 'Nombre',   'text',    True ,     True,          None ],
            ['activo', 'Actividad',         'Color',    'p',       True,      True,          None ],
            ['icono',  'Icono',             'Icono',    'icon',    True ,     True,          None ],
            ['color',  'Color',             'color',    'color',   True,      True,          None ],
            ['img',  'Imagen',             'Imagen',    'img',   True,      True,          None ],
        ],
        "crud_forms": {
            "crud_list": True ,
            "crud_search": True ,
            "crud_consult": True ,
            "crud_insert": True ,
            "crud_update": True ,
            "crud_delete": True ,
            "crud_unactive": True ,
        },
        "no_crud" : 'administrar_paginas' ,
    },

# _BORRAR
    "ubigeo" : {
        "active":True,
        "titulo":"Ubigeo",
        "nombre_tabla":"ubigeo",
        "controlador": controlador_ubigeo,
        "icon_page" : "ri-map-pin-line",
        "filters":[
            ['activo', f'{TITLE_STATE}', get_options_active() ],
        ],
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
    "tipo_paquete": {
        "active" : True ,
        "titulo": "tipos de paquetes",
        "nombre_tabla": "tipo de paquete",
        "controlador": controlador_contenido_paquete,
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
    }
    
}


REPORTES = {
    "lista_unidades": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-truck' ,
        "titulo": "Listado de unidades",
        "table" : controlador_unidad.get_report_test(),
        "filters": [
            ['modeloid', 'Modelo', lambda: controlador_modelo.get_options() ],
        ] ,
        
    },
    "lista_empleados": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-clipboard-user' ,
        "titulo": "Listado de empleados",
        "table" : controlador_empleado.get_report_test(),
        "filters": [
            ['rol_id', 'Rol', lambda: controlador_rol.get_options() ],
        ] ,
        
    },
    "ventas_periodo": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-sack-dollar' ,
        "titulo": "Ventas",
        "table" : controlador_cliente.get_reporte_ventas(),
        "filters": [
            # ['rol_id', 'Rol', lambda: controlador_rol.get_options() , 'select' ],
            ['fecha', 'Fecha', None, 'interval_date' ], 
            # ['fecha', 'Fecha', None, 'date' ],
        ] ,
    },
    "paquete_estado_fecha": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-box' ,
        "titulo": "Listado de paquetes por estado actual y fecha",
        "table" : controlador_paquete.get_report_test(),
        "filters": [
            ['fecha', 'Fecha', None, 'interval_date' ],
        ] ,
    },
    "listado_general_empleados_rol": {
        "active": True,
        "icon_page": "fa-solid fa-user-tie",
        "titulo": "Listado de empleados por rol",
        "table": controlador_empleado.get_report_test(),
        "filters": [
            ['rol_id', 'Rol', lambda: controlador_rol.get_options()],
        ],
    },

    "ingresos_periodo": {
        "active": True,
        "icon_page": "fa-solid fa-coins",  # Puedes cambiar este ícono si quieres otro
        "titulo": "Reporte de ingresos por periodo",
        "table": reporte_ingresos.get_ingresos_diarios(),
        "filters": [],  # No se requiere filtro por ahora
    },

    "reporte_usuarios": {
        "active": True,
        "icon_page": "fa-solid fa-users",
        "titulo": "Reporte de Usuarios",
        "table": controlador_usuario.get_report_usuarios(),
        "filters": [
            ['tipo_usuario', 'Tipo de Usuario', lambda: controlador_usuario.get_options()],
            ['activo', 'Estado', lambda: [(1, "Activo"), (0, "Inactivo")]],
        ],
    },     
    "articulos_mas_vendidos": {
        "active": True,
        "icon_page": "fa-solid fa-boxes-stacked",
        "titulo": "Artículos Más Vendidos",
        "table": controlador_articulo.get_report_mas_vendidos(),  # referencia a función sin paréntesis
        "filters": [
            ['fecha', 'Fecha', None, 'interval_date'],  # filtro rango de fechas
        ],
    },
    "articulos_reposicion": {
        "active": True,
        "icon_page": "fa-solid fa-boxes-stacked",
        "titulo": "Artículos que Necesitan Reposición",
        "table": controlador_articulo.get_report_reposicion(),  # función sin paréntesis
        "filters": [
            ['stock_minimo', 'Stock Mínimo', lambda: controlador_articulo.get_stock_minimo_options(), 'select'],
        ],
    },
    "horarios_sucursal": {
        "active": True,
        "icon_page": "fa-solid fa-clock",
        "titulo": "Reporte de horarios de sucursales",
        "table": controlador_sucursal.get_report_horario(), 
        "filters": [
            # ['stock_min', 'Stock Mínimo', None, 'number'],
        ],
    }

}


GRAFICOS = {
    # LINEA
    "ingresos_periodo": {
        "active": False,
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
            "series": lambda: [{
                "name": 'Ingresos',
                "data": extract_col_row(ingresos_periodo())[1]
            }],
            "xaxis": lambda: {
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
        "active" : False ,
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
            "series": lambda: [{
                "name": 'Ingresos',
                "data": extract_col_row(articulos_mas_vendidos())[1]
            }],
            "xaxis": lambda: {
                "categories": extract_col_row(articulos_mas_vendidos())[0]
            },
            "colors": [' var(--color15) ']
        }
    },
    # BARRA HORIZONTAL
    "top_envios": {
        "active" : False ,
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
        "active" : False ,
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
        "active" : False ,
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
}


MENU_ADMIN = {
    'administracion' : {
        'active': True ,
        'name' : 'Administración',
        'icon_page' : 'fa-solid fa-user-tie',
        'dashboard' : True,
        'cruds' :     [ 'tipo_unidad' , 'marca' , 'modelo' , 'unidad' , 'sucursal','ubigeo','tarifa_ruta'],
        'reports' :   [ 
            'lista_unidades' , 
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
        'cruds' :     [ 'estado_encomienda','tipo_paquete', 'tipo_cliente', 'cliente' ],
        'reports' :   [ 
            'envios_tipo' , 
            'entregado_pendiente' ,
            'top_envios' , 
            ],
    },
    'atencion' : {
        'name' : 'Atención al Cliente',
        'active': True ,
        'icon_page' : 'fa-solid fa-circle-question',
        'dashboard' : True,
        'cruds' :     [ 'tipo_indemnizacion','tipo_reclamo','motivo_reclamo','causa_reclamo','estado_reclamo','reclamo','pregunta_frecuente' ],
        'reports' :   [ ],
    },
    'ventas' : {
        'name' : 'Ventas',
        'active': True ,
        'icon_page' : 'fa-solid fa-file-invoice-dollar',
        'dashboard' : True,
        'cruds' :     ['tamaño_caja', 'metodo_pago', 'tipo_comprobante','descuento','descuento_articulo' ],
        'reports' :   [ 'articulos_mas_vendidos'  ],
    },
    'seguridad' : {
        'name' : 'Seguridad',
        'active': True,
        'icon_page' : 'fa-solid fa-shield-halved',
        'dashboard' : True,
        'cruds' :     [  ],
        'dashboard' : False,
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


TRANSACCIONES = {
    "salida": {
        "active" : True ,
        "titulo": "salidas",
        "nombre_tabla": "salida",
        "controlador": controlador_salida,
        "icon_page": 'fa-solid fa-van-shuttle',
        "filters": [
            
        ] ,
       "fields_form" : [
            ['id',          'ID',            'ID',             'text',   True,   False,   None],
            ['nom_conductor','Conductor',    'Nombre del conductor', 'text', True, False,   None],
            ['placa',       'Placa de unidad','Placa de unidad', 'text',   True,   True,    None],
            ['destino',     'Destino',       'Destino',         'text',   True,   True,    None],
            ['fecha',       'Fecha',         'YYYY-MM-DD',      'date',   True,   True,    None],
            ['hora',        'Hora',          'HH:MM',           'time',   True,   True,    None],
            ['capacidad',   'Capacidad',     'Capacidad en kg', 'number', True,  False,   None],
            ['estado',      'Estado',        'Estado actual',   'text',   True,   False,   None],
       ],

        "crud_forms": {
            "crud_list": True ,
            "crud_search": False ,
            "crud_consult": True ,
            "crud_insert": True ,
            "crud_update": True ,
            "crud_delete": True ,
            "crud_unactive": False ,
        }
    },
    
}


###########_ REDIRECT _#############

@app.route("/")
def main_page():
    # return redirect(url_for('index'))
    return redirect_url('index')


def main_empleado_page():
    # return redirect(url_for('panel'))
    return redirect_url('panel')


def main_cliente_page():
    # return redirect(url_for('panel'))
    return redirect_url('perfil')


def redirect_login():
    # return redirect(url_for('panel'))
    return redirect_url('login')


def redirect_url(url):
    return redirect(url_for(url))


def redirect_crud(tabla):
    return redirect(url_for('crud_generico', tabla = tabla))


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


def validar_empleado():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user_id = request.cookies.get('user_id')
                correo = request.cookies.get('correo')
                usuario = controlador_usuario.get_usuario_empleado_por_id(user_id)

                if usuario and usuario['correo'] == correo and usuario['tipo_usuario'] == 'E' :
                    page = f(*args, **kwargs)

                    if page:
     
                        return page

                    else:
                        return rdrct_error( main_empleado_page() , 'Esta pagina no existe') 
                return rdrct_error(redirect_url('login') , 'LOGIN_INVALIDO') 
            except Exception as e:
                return rdrct_error(redirect_url('login') , e) 
        return wrapper
    return decorator


def validar_cliente():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                user_id = request.cookies.get('user_id')
                correo = request.cookies.get('correo')
                usuario = controlador_usuario.get_usuario_cliente_por_id(user_id)
                if usuario and usuario['correo'] == correo and usuario['tipo_usuario'] == 'C' :
                    page = f(*args, **kwargs)
                    if page:
                        return page
                    else:
                        return rdrct_error( main_cliente_page() , 'Esta pagina no existe') 
                return rdrct_error(redirect_url('login') , 'LOGIN_INVALIDO') 
            except Exception as e:
                return rdrct_error(redirect_url('login') , e) 
        return wrapper
    return decorator


###########_ CONTEXT_PROCESSOR _#############

@app.context_processor
def inject_cur_modulo_id():
    try:
        path = request.path  
        parts = path.strip('/').split('=')
        key = parts[-1] 
        page = parts[0]
        if page == 'dashboard':
            dataPage = permiso.get_modulo_key(key)
            if dataPage:
                return dict(cur_modulo_id=dataPage['id'])
        else:
            dataPage = permiso.get_pagina_key(key)
            if dataPage:
                return dict(cur_modulo_id=dataPage['moduloid'])
        return dict(cur_modulo_id=None)
    except Exception as e:
        return dict(cur_modulo_id=None)


@app.context_processor
def inject_globals():
    listar_pages_admin = listar_admin_pages()
    modulos = permiso.get_lista_modulos()
    tipos_paginas = permiso.get_lista_tipo_paginas()
    menu_paginas = permiso.get_paginas()
    options_pagination_crud , selected_option_crud = get_options_pagination_crud()
    cookie_error = request.cookies.get('error')
    user_id = request.cookies.get('user_id')
    main_information = controlador_empresa.get_information()
    datosUsuario = getDatosUsuario()
    if datosUsuario:
        tipoUsuario = getDatosUsuario()['tipo_usuario']
        if tipoUsuario == 'E':
            datosUsuario = controlador_usuario.get_usuario_empleado_por_id(user_id)
        elif tipoUsuario == 'C':
            datosUsuario = controlador_usuario.get_usuario_cliente_por_id(user_id)
        else:
            datosUsuario = None
    else:
        tipoUsuario = None

    return dict(
        # todo el sistema
        URL_IMG_LOGO           = f'/static/img/img_empresa/{controlador_empresa.get_logo()}' ,
        # URL_IMG_LOGO           = f'/static/img/img_empresa/logo.png' ,
        main_information = main_information ,
        cookie_error = cookie_error,
        datosUsuario = datosUsuario ,
        tipoUsuario = tipoUsuario ,

        # paginas empleado
        options_pagination_crud = options_pagination_crud ,
        selected_option_crud = selected_option_crud ,
        modulos= modulos ,
        tipos_paginas = tipos_paginas ,
        menu_paginas = menu_paginas ,

        # paginas cliente


        # constantes
        MENU_ADMIN             = MENU_ADMIN,
        HABILITAR_ICON_PAGES   = HABILITAR_ICON_PAGES,
        SYSTEM_NAME            = main_information['nombre'],
        STATE_0                = STATE_0,   
        STATE_1                = STATE_1,
        ACT_STATE_0            = ACT_STATE_0,
        ACT_STATE_1            = ACT_STATE_1,
        NOMBRE_CRUD_PAGE       = NOMBRE_CRUD_PAGE,
        NOMBRE_ADMINPAGES_PAGE = NOMBRE_ADMINPAGES_PAGE ,
        NOMBRE_OPTIONS_COL     = NOMBRE_OPTIONS_COL,
        NOMBRE_BTN_INSERT      = NOMBRE_BTN_INSERT,
        NOMBRE_BTN_UPDATE      = NOMBRE_BTN_UPDATE,
        NOMBRE_BTN_DELETE      = NOMBRE_BTN_DELETE,
        NOMBRE_BTN_UNACTIVE    = NOMBRE_BTN_UNACTIVE,
        NOMBRE_BTN_LIST        = NOMBRE_BTN_LIST,
        NOMBRE_BTN_CONSULT     = NOMBRE_BTN_CONSULT,
        NOMBRE_BTN_SEARCH      = NOMBRE_BTN_SEARCH,
        ICON_PAGE_CRUD         = ICON_PAGE_CRUD ,
        ICON_PAGE_REPORT       = ICON_PAGE_REPORT ,
        ICON_PAGE_DASHBOARD    = ICON_PAGE_DASHBOARD ,
        ICON_PAGE_PANEL        = ICON_PAGE_PANEL ,
        ICON_LIST              = ICON_LIST     ,
        ICON_CONSULT           = ICON_CONSULT  ,
        ICON_SEARCH            = ICON_SEARCH   ,
        ICON_INSERT            = ICON_INSERT   ,
        ICON_UPDATE            = ICON_UPDATE   ,
        ICON_DELETE            = ICON_DELETE   ,
        ICON_ACTIVE            = ICON_ACTIVE   ,
        ICON_UNACTIVE          = ICON_UNACTIVE ,
        ICON_UNLOCK            = ICON_UNLOCK   ,
        ICON_PAGE_NOICON       = f'{ICON_PAGE_NOICON} d_i' ,
    )


###########_ PAGES _#############

paginas_simples = [ 
    "index" , 
    'sign_up', 
    'tracking',
    'seguimiento',
    'recuperar_contrasenia',
    'libro_reclamaciones',
    'mis_envios',
    'NoRecibimos',
    'pagina_reclamo',
    'seguimiento_reclamo',
    'Metodo_pago',
    'perfil',
    'prueba_seguimiento',
    'cajas',
    'cajas_prueba',
    'articulos',
    'sobre_nosotros',
    'TerminosCondiciones',
    'salidas_programadas', #para eliminar
    'mapa_curds',
    'salida_informacion',
    'cambiar_contrasenia',
    'programacion_devolucion',
]


for pagina in paginas_simples:
    app.add_url_rule(
        f"/{pagina}",  # URL
        pagina,        # Nombre de la función
        lambda p=pagina: render_template(f"{p}.html")  # Renderiza la plantilla
    )


@app.route("/login")
def login():
    user_id = request.cookies.get('user_id')
    correo = request.cookies.get('correo')
    usuario = controlador_usuario.get_usuario_por_id(user_id)
    if usuario and correo and usuario['correo'] == correo :
        if usuario['tipo_usuario'] == 'E':
            return main_empleado_page()
        elif usuario['tipo_usuario'] == 'C' :
            return main_cliente_page()
    # else:
    return render_template('login.html')


@app.route("/logout")
def logout():
    try:
        resp = make_response(redirect_login())
        resp.delete_cookie('user_id')
        resp.delete_cookie('correo')
        return resp
    except Exception as e:
        return rdrct_error(redirect_login(),e)


##################_ CLIENTE PAGE _################## 

@app.route("/faq")
def Faq():
    return render_template('Faq.html')


@app.route("/contactanos")
def contac():
    return render_template('contactanos.html')

@app.route("/api/cajas")
def api_cajas():
    filas = controlador_articulo.get_table_with_discount()
    # print(filas)
    productSizes = {}

    for fila in filas:
        if not fila['activo'] or not fila['tamaño_cajaid']:
            continue

        key = fila['tam_nombre'].lower()
        nombre = fila['nom_articulo']
        precio = float(fila['precio'])
        img = fila['img']

        if key not in productSizes:
            productSizes[key] = {
                "name_product":nombre,
                "price": precio,
                "dimensions": fila['dimensiones'],
                "image": img,
                "discounts": []  
            }

        if fila['cantidad_descuento'] and fila['nom_descuento']:
            productSizes[key]["discounts"].append({
                "name": fila['nom_descuento'],  
                "value": float(fila['cantidad_descuento'])
            })
    return jsonify(productSizes)


@app.route("/api/articulos")
def api_articulos():
    filas = controlador_articulo.get_table_with_discount()
    articulos = {}

    for fila in filas:
        if not fila['activo']:
            continue

        key = fila['nom_articulo'].lower()
        if key not in articulos:
            articulos[key] = {
                "name_product": fila['nom_articulo'],
                "price": float(fila['precio']),
                "stock": fila['stock'],
                "dimensions": fila['dimensiones'] or '',
                "image": fila['img'] or '',
                "size_name": fila['tam_nombre'] or '',
                "discounts": []
            }
        if fila['cantidad_descuento'] and fila['nom_descuento']:
            articulos[key]["discounts"].append({
                "name": fila['nom_descuento'],
                "value": float(fila['cantidad_descuento'])
            })

    return jsonify(articulos)




@app.route("/carrito")
def carrito():
    return render_template('carrito.html')


@app.route("/cotizador")
def cotizador():
    departamentos = controlador_ubigeo.get_options_departamento()
    provincias = controlador_ubigeo.get_options_provincia()
    distritos = controlador_ubigeo.get_options_distrito()
    return render_template(
        'cotizador.html' ,
        departamentos = departamentos,
        provincias = provincias,
        distritos = distritos,
    )


##############erliz rutas####


@app.route('/tipos-envio')
def tipos_envio():
    return render_template('tipos_envio.html')

@app.route('/registro-envio')
def registro_envio():
    return render_template('registro_envio.html')

@app.route('/resumen_envio')
def mostrar_resumen():
    return render_template('resumen_envio.html') 

@app.route('/pagoenvio')
def mostrar_pagoenvio():
    return render_template('pago_envio.html') 


#########

@app.route('/envio_masivo')
def envio_masivo():
    nombre_doc = controlador_tipo_documento.get_options()
    nombre_rep = controlador_tipo_recepcion.get_options()
    rutas_tarifas = controlador_tarifa_ruta.get_sucursales_origen_destino()
    articulos = controlador_contenido_paquete.get_options()
    empaque = controlador_tipo_empaque.get_options()
    condiciones = controlador_regla_cargo.get_condiciones_tarifa()
    tarifas = controlador_tarifa_ruta.get_tarifas_ruta_dict()
    return render_template('envio_masivo.html', 
                           nombre_doc=nombre_doc,
                           nombre_rep=nombre_rep,
                           rutasTarifas=json.dumps(rutas_tarifas), 
                           tarifas = json.dumps(tarifas),
                           empaque=empaque, 
                           articulos=articulos,
                           condiciones=condiciones)
    
    
    
    
    

################# Sucursales ######################

@app.route("/sucursales")
def sucursales():
    departamentos = controlador_ubigeo.get_options_departamento()
    provincias = controlador_ubigeo.get_options_provincia()
    distritos = controlador_ubigeo.get_options_distrito()
    agencias = controlador_sucursal.get_agencias_data()

    return render_template(
        'sucursales.html',
        departamentos=departamentos,
        provincias=provincias,
        distritos=distritos,
        agencias=agencias
    )


##################_ METHOD POST GENERALES _################## 


@app.route("/procesar_login", methods=["POST"])
def procesar_login():
    try:
        correo = request.form["email"]
        password = request.form["password"]
        usuario = controlador_usuario.get_usuario_por_correo(correo)
        encpassword = encrypt_sha256_string(password)
        # print(encpassword)
        # print(usuario)

        if usuario and encpassword == usuario['contrasenia']:
            resp = resp_login(
                'login',
                usuario['id'] ,
                usuario['correo'] 
            )
            # controlador_usuario.actualizar_token(username, token)
            return resp
        else:
            return rdrct_error(redirect_url('login') ,'LOGIN_INVALIDO')
    except Exception as e:
        return rdrct_error(redirect_url('login')  , e)


##################_ PAGINAS EMPLEADO _################## 


@app.route("/panel")
@validar_empleado()
def panel():
    return render_template('panel.html')


@app.route("/dashboard=<module_name>")
@validar_empleado()
def dashboard(module_name):
    modulo = permiso.get_modulo_key(module_name)
    tipos_pag = permiso.get_tipos_pagina_moduloid(modulo['id'])
    return render_template(
        'dashboard.html' , 
        module_name = module_name , 
        modulo = modulo ,
        REPORTES = REPORTES ,
        tipos_pag = tipos_pag ,
        )


@app.route("/crud=<tabla>")
# @validar_empleado()
def crud_generico(tabla):
    config = CONTROLADORES.get(tabla)
    if config:
        active = config["active"]
        no_crud = config.get('no_crud')
        if active is True and (no_crud is None or no_crud is False):
            icon_page_crud = get_icon_page(config.get("icon_page"))
            titulo = config["titulo"]
            controlador = config["controlador"]
            nombre_tabla = config["nombre_tabla"]
            filters = config["filters"]
            fields_form = config["fields_form"]

            existe_activo = controlador.exists_Activo()
            columnas , filas = controlador.get_table()
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
                # value_search   = value_search,
                columnas       = columnas ,
                key_columns    = list(columnas.keys()) ,
                table_columns  = table_columns ,
                # info_columns   = info_columns,
                crud_list      = crud_list,
                crud_search    = crud_search,
                crud_consult   = crud_consult,
                crud_insert    = crud_insert,
                crud_update    = crud_update,
                crud_delete    = crud_delete,
                crud_unactive  = crud_unactive,
            )


@app.route("/reporte=<report_name>")
@validar_empleado()
def reporte(report_name):
    config = REPORTES.get(report_name)
    if config:
        active = config["active"]
        if active is True:
            titulo = config["titulo"]
            icon_page_crud = get_icon_page(config.get("icon_page"))
            filters = config["filters"]
            columnas , filas = config["table"]
            table_columns  = list(filas[0].keys()) if filas else []
            
            return render_template(
                "CRUD.html" ,
                icon_page_crud = icon_page_crud ,
                titulo         = titulo ,
                filas          = filas ,
                filters        = filters,
                columnas       = columnas ,
                key_columns    = list(columnas.keys()) ,
                table_columns  = table_columns ,
                crud_search    = True,
                # crud_consult   = True,
                # crud_insert    = True,
                # crud_update    = True,
                # crud_delete    = True,
                # crud_unactive  = True,
                esReporte      = True ,
            )


@app.route("/transaccion=<tabla>")
@validar_empleado()
def crud_transaccion(tabla):
    config = TRANSACCIONES.get(tabla)
    if config:
        active = config["active"]
        if active is True :
            icon_page_crud = get_icon_page(config.get("icon_page"))
            titulo = config["titulo"]
            controlador = config["controlador"]
            nombre_tabla = config["nombre_tabla"]
            filters = config["filters"]
            fields_form = config["fields_form"]

            existe_activo = controlador.exists_Activo()
            columnas , filas = controlador.get_table()
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
                "CRUD_prueba.html" ,
                tabla          = tabla ,
                nombre_tabla   = nombre_tabla ,
                icon_page_crud = icon_page_crud ,
                titulo         = titulo ,
                filas          = filas ,
                primary_key    = primary_key ,
                filters        = filters,
                fields_form    = fields_form ,
                columnas       = columnas ,
                key_columns    = list(columnas.keys()) ,
                table_columns  = table_columns ,
                crud_list      = crud_list,
                crud_search    = crud_search,
                crud_consult   = crud_consult,
                crud_insert    = crud_insert,
                crud_update    = crud_update,
                crud_delete    = crud_delete,
                crud_unactive  = crud_unactive,
                esTransaccion = True
            )

    
@app.route("/seguimiento_empleado_prueba=<placa>")
@validar_empleado()
def seguimiento_empleado_prueba(placa):
    return render_template('seguimiento_empleado_prueba.html', placa=placa)


@app.route("/administrar_paginas")
@validar_empleado()
def administrar_paginas():
    modulos = permiso.get_lista_modulos()
    paginas = permiso.get_paginas()
    roles = permiso.get_lista_roles()
    tipos_rol = permiso.get_lista_tipo_roles()
    cants_mod = permiso.get_cants_modulos()

    fields_form_modulo = [
    #   ID/NAME    LABEL              PLACEHOLDER    TYPE       REQUIRED   ABLE/DISABLE   DATOS
        ['nombre', 'Nombre del módulo', 'Nombre',   'text',    True ,     True,          None ],
        ['activo', 'Actividad',         'Color',    'p',       True,      True,          None ],
        ['icono',  'Icono',             'Icono',    'icon',    True ,     True,          None ],
        ['color',  'Color',             'color',    'color',   True,      True,          None ],
        ['img',  'Imagen',             'Imagen',    'img',   True,      True,          None ],
    ]

    fields_form_page = [
#        ID/NAME          LABEL               PLACEHOLDER    TYPE    REQUIRED   ABLE/DISABLE   DATOS
        ['titulo',         'Nombre del módulo', 'Nombre',        'text',    True ,   True   ,      None ],
        ['activo',         'Actividad',         'Color',         'p',       True,    True   ,      None ],
        ['icono',         'Icono',             'Icono',             'icon',    False ,   True   ,      None ],
        ['moduloid',       'Módulo',           'Módulo',          'select',  True ,   None   ,   [lambda: controlador_modulo.get_options() , 'nom_modulo'] ], 
        # ['tipo_paginaid',  'Tipo de página',   'Tipo de página',    'select',  True ,   None   ,   [lambda: controlador_tipo_pagina.get_options() , 'nom_tipo'] ],
    ]
    

    return render_template(
        'administrar_paginas.html' ,
        modulos = modulos ,
        paginas = paginas , 
        roles = roles ,
        tipos_rol = tipos_rol ,
        cants_mod = cants_mod ,
        fields_form_modulo = fields_form_modulo ,
        fields_form_page = fields_form_page  ,
 
        )


@app.route("/permiso_rol=<int:rolid>")
@validar_empleado()
def permiso_rol(rolid):
    modulos = permiso.get_lista_modulos()
    paginas = permiso.get_paginas_permiso_rol(rolid)
    roles = permiso.get_lista_roles()
    tipos_rol = permiso.get_lista_tipo_roles()
    cants_mod = permiso.get_cants_modulos()

    info_rol = permiso.get_info_rol(rolid)

    return render_template(
        'administrar_paginas.html' ,
        modulos = modulos ,
        paginas = paginas , 
        roles = roles ,
        tipos_rol = tipos_rol ,
        rolid = rolid ,
        info_rol = info_rol ,
        cants_mod = cants_mod ,
        cur_modulo_id = permiso.get_pagina_key('administrar_paginas')['moduloid'] ,
        )


@app.route("/informacion_empresa")
@validar_empleado()
def informacion_empresa():
    information = controlador_empresa.get_data()
    
    return render_template(
        'informacion_empresa.html' ,
        information = information ,
        )


##################_ PAGINAS EMPLEADO METHOD POST _################## 

@app.route("/insert_row=<tabla>", methods=["POST"])
# @validar_empleado()
# @validar_error_crud()
def crud_insert(tabla):
    # try:
        config = CONTROLADORES.get(tabla)
        if not config:
            return "Tabla no soportada", 404

        active = config["active"]
        no_crud = config.get('no_crud')

        if active is False:
            return "Tabla no soportada", 404

        controlador = config["controlador"]
        firma = inspect.signature(controlador.insert_row)

        valores = []
        for nombre, parametro in firma.parameters.items():
            if nombre in request.files:
                archivo = request.files[nombre]
                if archivo.filename != "":
                    nuevo_nombre = guardar_imagen_bd(tabla , '' , archivo)
                    valores.append(nuevo_nombre)
                else:
                    # Si no se selecciona una nueva imagen, mantener la actual
                    valores.append(request.form.get(f"{nombre}_actual"))
            else:
                valor = request.form.get(nombre)
                valores.append(valor)

        controlador.insert_row( *valores )

        if no_crud :
            return redirect(url_for(no_crud))
        else:
            return redirect(url_for('crud_generico', tabla = tabla))
    # except Exception as e:
    #     return f"No se aceptan carácteres especiales", 400


@app.route("/update_row=<tabla>", methods=["POST"])
# @validar_empleado()
# @validar_error_crud()
def crud_update(tabla):
    # try:
        config = CONTROLADORES.get(tabla)
        if not config:
            return "Tabla no soportada", 404

        active = config["active"]
        no_crud = config.get('no_crud')

        # no_crud = config["no_crud"]

        if active is False:
            return "Tabla no soportada", 404

        controlador = config["controlador"]
        firma = inspect.signature(controlador.update_row)

        valores = []
        for nombre, parametro in firma.parameters.items():
            if nombre in request.files:
                archivo = request.files[nombre]
                # print(archivo)
                if archivo.filename != "":
                    # print(nombre)
                    nuevo_nombre = guardar_imagen_bd(tabla,'' ,archivo)
                    valores.append(nuevo_nombre)
                else:
                    # Si no se selecciona una nueva imagen, mantener la actual
                    valores.append(request.form.get(f"{nombre}_actual"))
            else:
                valor = request.form.get(nombre)
                valores.append(valor)

        controlador.update_row( *valores )
        if no_crud :
            return redirect(url_for(no_crud))
        else:
            return redirect(url_for('crud_generico', tabla = tabla))
    # except Exception as e:
    #     return f"No se aceptan carácteres especiales", 400


@app.route("/delete_row=<tabla>", methods=["POST"])
# @validar_empleado()
# @validar_error_crud()
def crud_delete(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]
    no_crud = config.get('no_crud')

    if active is False:
        return "Tabla no soportada", 404

    controlador = config["controlador"]
    primary_key = controlador.get_primary_key()

    if isinstance(primary_key, list):
        valores_pk = [request.form.get(pk) for pk in primary_key]
        controlador.delete_row(*valores_pk)
    else:
        controlador.delete_row(request.form.get(primary_key))

    if no_crud :
        return redirect(url_for(no_crud))
    else:
        return redirect(url_for('crud_generico', tabla = tabla))


@app.route("/unactive_row=<tabla>", methods=["POST"])
# @validar_empleado()
# @validar_error_crud()
def crud_unactive(tabla):
    config = CONTROLADORES.get(tabla)
    if not config:
        return "Tabla no soportada", 404

    active = config["active"]
    no_crud = config.get('no_crud')

    if active is False:
        return "Tabla no soportada", 404

    controlador = config["controlador"]
    existe_activo = controlador.exists_Activo()
    primary_key = controlador.get_primary_key()

    if existe_activo:
        if isinstance(primary_key, list):
            valores_pk = [request.form.get(pk) for pk in primary_key]
            controlador.unactive_row(*valores_pk)
        else:
            controlador.unactive_row(request.form.get(primary_key))

    if no_crud :
        return redirect(url_for(no_crud))
    else:
        return redirect(url_for('crud_generico', tabla = tabla))


@app.route("/update_empresa", methods=["POST"])
@validar_empleado()
@validar_error_crud()
def update_empresa():
    controlador = controlador_empresa
    firma = inspect.signature(controlador.update_row)

    valores = []
    for nombre, parametro in firma.parameters.items():
        if nombre in request.files:
            archivo = request.files[nombre]
            if archivo.filename != "":
                nuevo_nombre = guardar_imagen_bd('empresa' ,'',archivo)
                valores.append(nuevo_nombre)
            else:
                valores.append(request.form.get(f"{nombre}_actual"))
        else:
            valor = request.form.get(nombre)
            valores.append(valor)

    controlador.update_row(*valores)
    return redirect(url_for('informacion_empresa'))



##################_ METHOD POST AJAX _################## 

@app.route('/actualizar_permiso', methods=['POST'])
def actualizar_permiso():
    data = request.get_json()
    paginaid = data.get('paginaid')
    column = data.get('column')
    rolid = data.get('rolid')

    try:
        permiso.change_permiso_pagina(column , paginaid , rolid)
        rpta_column = permiso.consult_permiso_rol(paginaid , rolid)[column]
        return jsonify({'success': True , 'rpta' : rpta_column})
    except Exception as e:
        print("Error al actualizar permiso:", e)
        return jsonify({'success': False, 'error': str(e)})


@app.route('/actualizar_permiso_modulo', methods=['POST'])
def actualizar_permiso_modulo():
    data = request.get_json()
    moduloid = data.get('moduloid')
    column = data.get('column')
    rolid = data.get('rolid')

    try:
        permiso.change_permiso_modulo(column , moduloid , rolid)
        # rpta_column = permiso.consult_permiso_rol(moduloid , rolid)[column]
        return jsonify({'success': True })
    except Exception as e:
        print("Error al actualizar permiso:", e)
        return jsonify({'success': False, 'error': str(e)})




# @app.route('/actualizar_comentario', methods=['POST'])
# def actualizar_comentario():
#     data = request.get_json()
#     id = data.get('id')
#     comentario = data.get('comentario')
#     try:
#         controlador_evaluacion.actualizar_comentario_det_id(comentario , id)
#         return jsonify({'success': True})
#     except Exception as e:
#         print("Error al actualizar comentario:", e)
#         return jsonify({'success': False, 'error': str(e)})





###################################CARRITO###########################
# @app.route('/agregar_carrito', methods = ['POST'])
# def agregar_carrito():
    

# @app.route('/seguimiento_empleado')
# def seguimiento_empleado():
#     vehicle_id = request.args.get('vehicle_id')
#     return render_template('seguimiento.html', selected_vehicle_id=vehicle_id)




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

    for color in ['-base' , '-sec' , '-thr' , '-contrast']:
        text = f'--color{color}'
        html += f'''
        <div class="color_block">
        <p>{text}</p> 
        <div style="height: 100%; width: 100%; background-color: var({text})"></div>
        </div>
    '''
        
    for color in ['light-color' , 'dark-color' ]:
        text = f'--{color}'
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
    
    html += '''
        <input type="color" name="" id="">
    '''

    return html




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=True)



##################_ _ARCHIVADO_ _################## 



# @app.route("/grafico=<report_name>")
# # @validar_admin()
# def grafico(report_name):
#     config = REPORTES.get(report_name)
#     if not config:
#         return "Reporte no encontrado", 404

#     active = config["active"]

#     if active is False:
#         return "Reporte no encontrado", 404
        
#     titulo = 'Reporte de ' + config.get("titulo")
#     elements = config.get("elements")
#     e_graph = elements.get('graph')
#     e_table = elements.get('table')
#     e_counter = elements.get('counter')
#     icon_page = get_icon_page(config.get("icon_page"))

#     graph = config.get("graph")
#     if graph:
#         if callable(graph.get("series")):
#             graph["series"] = graph["series"]()
#         if callable(graph.get("xaxis")):
#             graph["xaxis"] = graph["xaxis"]()

#     table = config.get("table")
#     columnas = None
#     filas = None
#     if table is not None and e_table is True:
#         columnas , filas = table

#     counter = config.get("counter")

#     return render_template(
#         "REPORTE.html" ,
#         titulo = titulo ,
#         elements = elements ,
#         e_graph = e_graph,
#         e_table = e_table,
#         e_counter = e_counter,
#         graph = graph ,
#         table = table ,
#         columnas = columnas,
#         filas = filas,
#         counter = counter ,
#         icon_page = icon_page,
#     )


