from flask import Flask, render_template, request, redirect, make_response, url_for , g,jsonify,json,abort,session,current_app , send_file, flash , send_from_directory #, after_this_request, flash, jsonify, session
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
from controladores import controlador_regla_cargo as controlador_regla_cargo
from controladores import controlador_modalidad_pago as controlador_modalidad_pago
from controladores import reporte_ingresos as reporte_ingresos
from controladores import controlador_transaccion_venta as controlador_transaccion_venta
from controladores import controlador_detalle_venta as controlador_detalle_venta
from controladores import controlador_metodo_pago_venta as controlador_metodo_pago_venta
from controladores import controlador_articulo as controlador_articulo
from controladores import controlador_modalidad_pago as controlador_modalidad_pago
from controladores import controlador_encomienda as controlador_encomienda
from controladores import controlador_encomiendasss as  controlador_encomiendasss
from controladores import controlador_seguimiento as  controlador_seguimiento
from controladores import controlador_programacion_devolucion as controlador_programacion_devolucion
from controladores import controlador_seguimiento_reclamos as controlador_seguimiento_reclamos
from controladores import reporte_listar_enco 
from controladores import reporte_reclamo_causa
from controladores import reporte_UsoUnidades
from controladores import reporte_Viajes_por_Unidad
from controladores import reporte_encomiendas_rutas as reporte_encomiendas_rutas
# import BytesIO
from itsdangerous import URLSafeSerializer
from controladores.bd import sql_execute
import uuid, os, qrcode
from decimal import Decimal, ROUND_HALF_UP

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import hashlib
from werkzeug.utils import secure_filename
from werkzeug.routing import MapAdapter
# import re
import configuraciones
from functools import wraps
import inspect

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from flask_mail import Mail, Message
from correo import enviar_correo
from datetime import timedelta
from flask_socketio import SocketIO, emit
from time import sleep
import traceback
import socket
from num2words import num2words
import pdfkit
import os

from collections import defaultdict




app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

app.secret_key = 'es-un-secreto'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'fabianapm060126@gmail.com'
app.config['MAIL_PASSWORD'] = 'vagfqxdumpuboswj'
    

mail = Mail(app)


IGV_RATE = Decimal('0.18')

STATE_0                = configuraciones.STATE_0
STATE_1                = configuraciones.STATE_1
TITLE_STATE            = configuraciones.TITLE_STATE
HABILITAR_ICON_PAGES   = configuraciones.HABILITAR_ICON_PAGES
ACT_STATE_0            = configuraciones.ACT_STATE_0
ACT_STATE_1            = configuraciones.ACT_STATE_1
NOMBRE_CRUD_PAGE       = configuraciones.NOMBRE_CRUD_PAGE
NOMBRE_ADMINPAGES_PAGE = configuraciones.NOMBRE_ADMINPAGES_PAGE 
NOMBRE_OPTIONS_COL     = configuraciones.NOMBRE_OPTIONS_COL
NOMBRE_BTN_INSERT      = configuraciones.NOMBRE_BTN_INSERT
NOMBRE_BTN_UPDATE      = configuraciones.NOMBRE_BTN_UPDATE
NOMBRE_BTN_DELETE      = configuraciones.NOMBRE_BTN_DELETE
NOMBRE_BTN_UNACTIVE    = configuraciones.NOMBRE_BTN_UNACTIVE
NOMBRE_BTN_LIST        = configuraciones.NOMBRE_BTN_LIST
NOMBRE_BTN_CONSULT     = configuraciones.NOMBRE_BTN_CONSULT
NOMBRE_BTN_SEARCH      = configuraciones.NOMBRE_BTN_SEARCH
ICON_PAGE_NOICON       = configuraciones.ICON_PAGE_NOICON 
ICON_PAGE_CRUD         = configuraciones.ICON_PAGE_CRUD 
ICON_PAGE_REPORT       = configuraciones.ICON_PAGE_REPORT 
ICON_PAGE_DASHBOARD    = configuraciones.ICON_PAGE_DASHBOARD 
ICON_PAGE_PANEL        = configuraciones.ICON_PAGE_PANEL 
ICON_LIST              = configuraciones.ICON_LIST
ICON_CONSULT           = configuraciones.ICON_CONSULT
ICON_SEARCH            = configuraciones.ICON_SEARCH
ICON_INSERT            = configuraciones.ICON_INSERT
ICON_UPDATE            = configuraciones.ICON_UPDATE
ICON_DELETE            = configuraciones.ICON_DELETE
ICON_ACTIVE            = configuraciones.ICON_ACTIVE
ICON_UNACTIVE          = configuraciones.ICON_UNACTIVE
ICON_UNLOCK            = configuraciones.ICON_UNLOCK

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
def resp_login( correo , contrasenia ):
    usuario = controlador_usuario.get_usuario_por_correo(correo)
    encpassword = encrypt_sha256_string(contrasenia)
    if usuario and encpassword == usuario['contrasenia']:
        resp = make_response(redirect_url('login'))
        resp.set_cookie('user_id', str(usuario['id']))
        resp.set_cookie('correo', correo)
        return resp
    else:
        return rdrct_error(redirect_url('login') ,'LOGIN_INVALIDO')

# Crear response para register
def resp_register( correo, contrasenia , conf_contrasenia, telefono, num_documento, nombre_siglas, apellidos_razon, tipo_documentoid, tipo_clienteid ):
    econtrasenia = encrypt_sha256_string(contrasenia)
    econf_contrasenia = encrypt_sha256_string(conf_contrasenia)
    if econf_contrasenia == econtrasenia:
        if controlador_usuario.get_info_usuario_por_correo(correo) is None :
            client_id = controlador_cliente.register_client( correo, telefono, num_documento, nombre_siglas, apellidos_razon, tipo_documentoid, tipo_clienteid )
            user_id = controlador_usuario.register_user_client( correo , econtrasenia )
            # return redirect_url('sign_up')
            return resp_login( correo , contrasenia )
        else:
            return rdrct_error(redirect_url('sign_up') ,'Este correo ya fue registrado')
    else:
        return rdrct_error(redirect_url('sign_up') ,'Las contraseñas no coinciden')

# Extraer función de un enlace
def obtener_funcion_desde_url(app: Flask, url: str, method='GET'):
    adapter: MapAdapter = app.url_map.bind("localhost")
    try:
        endpoint, args = adapter.match(url, method=method)
        return endpoint  # nombre de la función de vista
    except Exception as e:
        return f"No se encontró ninguna función para la URL '{url}': {str(e)}"

# Registrar páginas simples en la app
def registrar_paginas_con_decorador(app, paginas, decorador):
    for pagina in paginas:
        # Aplicar el decorador manualmente a la función
        def vista(p=pagina):
            return render_template(f"{p}.html")

        # Decorar la vista y registrarla
        vista_decorada = decorador()(vista)
        app.add_url_rule(f"/{pagina}", pagina, vista_decorada)

# Datos de usuario que ha iniciado sesión
def getDatosUsuario():
    user_id = request.cookies.get('user_id') 
    correo = request.cookies.get('correo')
    if user_id and correo:
        usuario = controlador_usuario.get_usuario_por_id(user_id)
        if usuario and correo and usuario['correo'] == correo:
            return usuario
    # else: 
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
        ruta_completa = os.path.join(upload_folder, nombre_final)
        archivo.save(ruta_completa)
        return nombre_final
    return None


def texto_a_json(texto):
    import json
    try:
        return json.loads(texto)
    except json.JSONDecodeError as e:
        print("Error al convertir a JSON:", e)
        return None


###########_ DICCIONARIOS _#############

ERRORES = {
    "NO_EXISTE_USERNAME" : "El nombre de usuario ingresado ya fue tomado por otro usuario" ,
    "NO_EXISTE_EMAIL" : "El correo electronico ingresado ya fue tomado por otro usuario" ,
    "LOGIN_INVALIDO" : 'Credenciales inválidas. Intente de nuevo' ,
    "PAGINA_NO_EXISTE" : 'La página a la que intentó ingresar no existe' ,
    "'NoneType' object is not subscriptable" : "Inicie sesión con su cuenta correspondiente",
    "foreign key constraint fails" : 'No es posible eliminar dicha fila' ,
    "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again." : "El enlace al que intentó ingresar no existe." ,
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
    "controlador": controlador_reclamo,
    "icon_page": "fa-solid fa-file",
    "filters": [],
    "fields_form": [
        ['id', 'ID', 'ID', 'text', True, False, None],
        ['nombres_razon', 'Cliente', 'Cliente', 'text', True, True, None],
        ['direccion', 'Dirección', 'Dirección', 'text', True, True, None],
        ['correo', 'Correo', 'Correo', 'email', True, True, None],
        ['telefono', 'Teléfono', 'Teléfono', 'text', True, True, None],
        ['n_documento', 'N° Documento', '', 'text', True, True, None],
        ['bien_contratado', 'Bien Contratado', '', 'select', True, True, [lambda:controlador_reclamo.get_list_bien_contratado(), '']],
        ['monto_reclamado', 'Monto Reclamado', '0.00', 'number', True, True, None],
        ['monto_indemnizado', 'Monto Indemnizado', '0.00', 'number', True, True, None],
        ['relacion', 'Relación con el bien', '', 'text', True, True, None],
        ['fecha_recepcion', 'Fecha de recepción', '', 'date', True, True, None],
        ['descripcion', 'Descripción', '', 'textarea', True, True, None],
        ['detalles', 'Detalles adicionales', '', 'textarea', True, True, None],
        ['pedido', 'Pedido', '', 'text', True, True, None],
        ['foto', 'Foto del reclamo', '', 'img', False, True, None],
        ['sucursal_id', 'Sucursal', '', 'select', True, True, [lambda: controlador_sucursal.get_options(), 'direccion']],
        ['causa_reclamoid', 'Causa del Reclamo', '', 'select', True, True, [lambda: controlador_causa_reclamo.get_options(), 'nombre']],
        ['tipo_indemnizacionid', 'Tipo de Indemnización', '', 'select', True, True, [lambda: controlador_tipo_indemnizacion.get_options(), 'nombre']],
        ['paquetetracking', 'Tracking', '', 'text', True, True, None],
        ['ubigeocodigo', 'Ubigeo', '', 'select', True, True, [lambda: controlador_ubigeo.get_options(), 'codigo']],
        ['tipo_documentoid', 'Tipo Documento', '', 'select', True, True, [lambda: controlador_tipo_documento.get_options(), 'nombre']]
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
            ['tamaño_cajaid','Tamaño de Caja',    'Tamaño de Caja', 'select',   False ,     True  ,        [lambda: controlador_tamanio_caja.get_options() , 'tam_nombre' ]  ],
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
    "modalidad_pago": {
        "active" : True ,
        "titulo": "modalidad de pago",
        "icon_page": 'fa-solid fa-truck-plane',
        "nombre_tabla": "modalidad_pago",
        "controlador": controlador_modalidad_pago,
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
    
    # "paquete": {
    #     "active": True,
    #     "titulo": "Paquetes",
    #     "nombre_tabla": "paquete",
    #     "controlador": controlador_paquete,
    #     "icon_page": "fa-solid fa-box",
    #     "filters": [
    #     ],
    #     "fields_form": [
    #         #   ID/NAME                        LABEL                         PLACEHOLDER                TYPE       REQUIRED  ABLE   DATOS
    #         ['tracking',                      'Tracking',                   'Id',            'text',     False,    False, True],
    #         ['valor',                         'Valor (S/.)',                'Valor',                   'number',   True,     True,  None],
    #         ['peso',                          'Peso (kg)',                  'Peso',                    'number',   True,     True,  None],
    #         ['estado_pago',                   'Estado de pago',             '0 = Pagado, 1 = Pendiente','select',  True,     True,  [['0', 'Pagado'], ['1', 'Pendiente']]],
    #         ['nombres_contacto_destinatario', 'Nombres contacto',           'Nombres',                 'text',     True,     True,  None],
    #         ['apellidos_razon_destinatario',  'Apellidos o Razón Social',   'Apellidos o Razón',       'text',     True,     True,  None],
    #         ['num_documento_destinatario',    'N° Documento',               'Documento',               'text',     True,     True,  None],
    #         ['tipo_documento_destinatario_id','Tipo de Documento',          'Elegir tipo',             'select',   True,     True,  [lambda: controlador_tipo_documento.get_options(), 'tipo_documento']],
    #         ['tipo_empaqueid',                'Tipo de Empaque',            'Elegir tipo',             'select',   True,     True,  [lambda: controlador_tipo_empaque.get_options(), 'tipo_empaque']],
    #         ['contenido_paqueteid',           'Contenido del Paquete',      'Elegir contenido',        'select',   False,    True,  [lambda: controlador_contenido_paquete.get_options(), 'contenido_paquete']],
    #         ['tipo_recepcionid',              'Tipo de Recepción',          'Elegir recepción',        'select',   True,     True,  [lambda: controlador_tipo_recepcion.get_options(), 'tipo_recepcion']],
    #         ['modalidad_pagoid',              'Modalidad de Pago',          'Elegir modalidad',        'select',   True,     True,  [lambda: controlador_modalidad_pago.get_options(), 'modalidad_pago']],
    #         ['sucursal_destino_id',           'Sucursal Destino',           'Elegir sucursal',         'select',   True,     True,  [lambda: controlador_sucursal.get_options(), 'direccion_destino']],
    #         ['descripcion',                   'Descripción',                'Descripción del paquete', 'textarea', False,    True,  None],
    #     ],
    #     "crud_forms": {
    #         "crud_list": True,
    #         "crud_search": True,
    #         "crud_consult": True,
    #         "crud_insert": True,
    #         "crud_update": True,
    #         "crud_delete": True,
    #         "crud_unactive": True,
    #     }
    # }

    
}


REPORTES = {   
    # Administracion
    "horarios_sucursal": {
        "active": True,
        "icon_page": "fa-solid fa-clock",
        "titulo": "Reporte de horarios de sucursales",
        "table": controlador_sucursal.get_report_horario(), 
        "filters": [
            # ['stock_min', 'Stock Mínimo', None, 'number'],
        ],
    },
    "ingresos_periodo": {
        "active": True,
        "icon_page": "fa-solid fa-coins",  # Puedes cambiar este ícono si quieres otro
        "titulo": "Reporte de ingresos por periodo",
        "table": reporte_ingresos.get_ingresos_diarios(),
        "filters": [],  # No se requiere filtro por ahora
    },
    # Encomiendas
    "paquete_estado_fecha": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-box' ,
        "titulo": "Listado de paquetes por estado actual y fecha",
        "table" : controlador_paquete.get_report_test(),
        "filters": [
            ['fecha', 'Fecha', None, 'interval_date' ],
        ] ,
    },
    
    # Logistica

    # Personal
    "listado_general_empleados_rol": {
        "active": True,
        "icon_page": "fa-solid fa-user-tie",
        "titulo": "Listado de empleados por rol",
        "table": controlador_empleado.get_report_test(),
        "filters": [
            ['rol_id', 'Rol', lambda: controlador_rol.get_options()],
        ],
    },

    # Seguridad
    "reporte_usuarios": {
        "active": True,
        "icon_page": "fa-solid fa-users",
        "titulo": "Reporte de Usuarios",
        "table": controlador_usuario.get_report_usuarios(),
        "filters": [
            ['tipo_usuario', 'Tipo de Usuario', lambda: controlador_usuario.get_options_tipo_usuario()],
            ['activo', 'Estado', lambda: [(1, "Activo"), (0, "Inactivo")]],
        ],
    },     
    
    # Ventas
    "ventas_periodo": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-sack-dollar' ,   
        "titulo": "Ventas",
        "table" : controlador_articulo.get_reporte_ventas(),
        "filters": [
            ['fecha', 'Fecha', None, 'interval_date' ], 
        ] ,
    },
    "articulos_mas_vendidos": {
        "active": True,
        "icon_page": "fa-solid fa-boxes-stacked",
        "titulo": "Artículos Más Vendidos",
        "table": controlador_articulo.get_report_mas_vendidos(),  
        "filters": [
            ['fecha', 'Fecha', None, 'interval_date'],  # filtro rango de fechas
        ],
    },
    "articulos_reposicion": {
        "active": True,
        "icon_page": "fa-solid fa-boxes-stacked",
        "titulo": "Artículos que Necesitan Reposición",
        "table": controlador_articulo.get_report_reposicion(), 
        "filters": [
        ],
    },


    "lista_unidades": {
        "active" : True ,
        'icon_page' : 'fa-solid fa-truck' ,
        "titulo": "Listado de unidades",
        "table" : controlador_unidad.get_report_test(),
        "filters": [
            ['modeloid', 'Modelo', lambda: controlador_modelo.get_options() ],
        ] ,
        
    },
    "reporte_uso_unidades": {
        "active" : True,
        'icon_page': 'fa-solid fa-chart-line',
        "titulo": "Reporte de uso de unidades",
        "table" : reporte_UsoUnidades.get_reporte_uso_unidades(),
        "filters": []
    },
    "viajes_por_unidad": {
        "active": True,
        "icon_page": "fa-solid fa-truck-fast",
        "titulo": "Viajes por unidad",
        "table": reporte_Viajes_por_Unidad.get_reporte_viajes_por_unidad(),  # 👈 FUNCIÓN EJECUTADA
        "filters": []
    },

    "encomiendas_listar": {
        "active": True,
        "icon_page": "fa-solid fa-boxes-packing",
        "titulo": "Listado de encomiendas segun tipo de empaque ",
        "table": reporte_listar_enco.get_reporte_encomiendas_por_tipo(),
        "filters": []
    },

    "reporte_reclamos_tipo_causa_periodo": {
    "active": True,
    "icon_page": "fa-solid fa-clipboard-list",
    "titulo": "Reporte de reclamos por tipo, causa y periodo",
    "table": reporte_reclamo_causa.get_reporte_reclamos_tipo_causa_periodo(),  # ✅ con paréntesis
    "filters": []
},
"encomiendas_rutas_estado": {
    "active": True,
    "icon_page": "fa-solid fa-route",
    "titulo": "Listado de encomiendas asignadas a rutas específicas y su estado",
    "table": reporte_encomiendas_rutas.get_reporte_encomiendas_rutas_estado(),  # 👈 con paréntesis
    "filters": []
},
}


TRANSACCIONES = {
    "salida": {
        "active" : True ,
        "titulo": "salidas",
        "nombre_tabla": "salida",
        "controlador": controlador_salida,
        "icon_page": 'fa-solid fa-van-shuttle',
        "filters": [] ,
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
            "crud_search": True ,
            "crud_consult": False ,
            "crud_insert": False ,
            "crud_update": False ,
            "crud_delete": True , 
            "crud_unactive": False ,
        },
        "buttons": [
           # hay_parametros  icon         color              enlace_function      parametros   clase_html   modo(insert ,update , consult)
            [False,   f'{ICON_CONSULT}',   'var(--color-consult)',  'salida_informacion', {} , '' , 'consult'],
            [False,   f'{ICON_UPDATE}',   'var(--color-update)',  'salida_informacion', {} , '' ,'update'],
            [False,   f'fa-solid fa-location-dot',   'grey',  None , {} , 'btn-ver-mapa' , 'mapa'], 
            # [True,   f'fa-solid fa-location-dot',   'grey',  'seguimiento_empleado_prueba' , {"placa": "placa"}],
            # [False,   f'fa-solid fa-location-dot',   'grey',  None , {} , 'btn-ver-mapa',], 
        ],
        "options": [
        # mostrar_url       icon             color                  text           enlace_function    parametros  modo(insert ,update , consult)
            [False,   f'{ICON_INSERT}',   'var(--color-insert)',  'Programar', 'salida_informacion', {},         'insert'],
        ],
    },
    "transaccion_encomienda": {
        "active": True,
        "titulo": "Encomiendas",
        "nombre_tabla": "encomienda",
        "controlador": controlador_encomienda,
        "icon_page": "fa-solid fa-boxes-packing",
        "filters": [],
        "fields_form": [
            ['num_serie',           'N° Serie',           'Número de Serie',           'text',      True,  True,   None],
            ['masivo',              'Tipo de Envío',      'Tipo de Envío', 'select',    True,  True,   [lambda: controlador_encomienda.get_select_tipo_envio(), 'nombre']],
            ['recojo_casa',         'Recojo a Domicilio', 'Recojo de paquete',             'select',    True,  True,   [lambda: controlador_encomienda.get_select_recojo_casa(), 'nombre']],
            ['fecha',               'Fecha',              'Fecha',                     'date',      True,  True,   None],
            ['hora',                'Hora',               'Hora',                      'time',      True,  True,   None],
            ['id_sucursal_origen',  'Sucursal de origen', 'Sucursales de origen',                          'select',    True,  True,   [lambda: controlador_tarifa_ruta.get_options_select_sucursal_origen(), 'nombre']],
            ['clienteid',           'Cliente',            'Clientes',                          'select',    True,  True,   [lambda: controlador_cliente.get_select_cliente(), 'nombre']],

            ['monto_total',         'Monto Total',        'Monto total',             'decimal_2', True,  True,   None],
            ['direccion_recojo',    'Direccion de recojo',    'Direccion de recojo',            'text',    True,  True,   None],
            ['descripcion',         'Descripcion',            'Descripcion',        'textarea',    True,  True,   None],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": False
        },
        "buttons": [
           # hay_parametros  icon         color      enlace_function              parametros                       clase_html   modo(insert ,update , consult)
            [True, 'fa-solid fa-boxes', "#77D62E", 'transaccion', {"tabla": "::paquete", "pk_foreign": "num_serie"} , '' ,    'paquete'],
        ],
        "options": [
        ],
    },
    "paquete": {
        "active": True,
        "titulo": "Paquetes",
        "nombre_tabla": "paquete",
        "controlador": controlador_paquete,
        "icon_page": "fa-solid fa-boxes",
        "filters": [], 
        "fields_form": [
        #   ID/NAME                        LABEL                       PLACEHOLDER           TYPE       REQUIRED  ABLE   DATOS
            ['tracking',                       'Tracking',             'Tracking',             'text',   False,  True,   None],
            ['valor',                          'Valor',                'Valor',                'text',   False,  True,   None],
            ['peso',                           'Peso',                 'Peso',                 'text',   False,  True,   None],
            ['estado_pago',                    'Pago',                 'Pago',                 'text',   False,  True,   None],
            ['nombres_contacto_destinatario',  'Nombre destinatario',  'Nombre destinatario',  'text',   False,  True,   None],
            ['apellidos_razon_destinatario',   'Apellido/Razón',       'Apellido/Razón',       'text',   False,  True,   None],
            ['num_documento_destinatario',     'Doc. Identidad',       'Doc. Identidadaa',     'text',   False,  True,   None],
            ['tipo_documento',                 'Tipo Documento',       'Tipo Documento',       'text',   False,  True,   None],
            ['tipo_empaque',                   'Empaque',              'Empaque',              'text',   False,  True,   None],
            ['contenido_paquete',              'Contenido',            'Contenido',            'text',   False,  True,   None],
            ['tipo_recepcion',                 'Recepción',            'Recepción',            'text',   False,  True,   None],
            ['modalidad_pago',                 'Pago modalidad',       'Pago modalidad',       'text',   False,  True,   None],
            ['direccion_destino',              'Dirección destino',    'Dirección destino',    'text',   False,  True,   None],
            ['localidad',                      'Ubigeo destino',       'Ubigeo destino',       'text',   False,  True,   None],
            ['num_serie',                      'N° Serie',             'N° Serie',             'text',   False,  True,   None],
            ['fecha',                          'Fecha envío',          'Fecha envío',          'text',   False,  True,   None],
            ['hora',                           'Hora envío',           'Hora envío',           'text',   False,  True,   None],
            ['monto_total',                    'Total S/.',            'Total S/.',            'text',   False,  True,   None],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": True,
            "crud_consult": True,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": False
        },
        "buttons": [
        # hay_parametros  icon         color              enlace_function      parametros   clase_html   modo(insert ,update , consult)
            # [True, 'fa-solid fa-map-location-dot', "#9856EE", 'seguimiento_tracking', {"tracking": "tracking"} , '' , 'seguimiento'],
            [True, 'fa-solid fa-route', "#9856EE", 'transaccion',  {"tabla": "::seguimiento", "pk_foreign": "tracking"} , '' , 'seguimiento' , False],
            [True, 'fa-solid fa-qrcode', "#B8CBD7", 'ver_img_qr',  {"tracking": "tracking"} , '' , 'qr_code' , True],
        ],
        "options": [
        # mostrar_url       icon             color                  text                 enlace_function       parametros                    modo(insert ,update , consult)
            [True,   f'fa-solid fa-arrow-left',   "#3e5376",  'Volver a Encomiendas', 'transaccion' , {"tabla": "::transaccion_encomienda" } , 'encomiendas'],
        ],
    },
    "seguimiento": {
        "active": True,
        "titulo": "Seguimiento",
        "nombre_tabla": "seguimiento",
        "controlador": controlador_seguimiento,
        "icon_page": "fa-solid fa-route",
        "filters": [], 
        "fields_form": [
        #   ID/NAME                        LABEL                       PLACEHOLDER           TYPE       REQUIRED  ABLE   DATOS
            # ['nombre_det',  'Detalle de estado', 'Detalle de estado', 'select', True ,True, [lambda: controlador_estado_reclamo.get_options() , 'nombre_det' ] ],
        ],
        "crud_forms": {
            "crud_list": True,
            "crud_search": False,
            "crud_consult": False,
            "crud_insert": True,
            "crud_update": True,
            "crud_delete": True,
            "crud_unactive": False
        },
        "buttons": [],
        "options": [
            [True,   f'fa-solid fa-arrow-left',   "#3e5376",  'Volver a Encomiendas', 'transaccion' , {"tabla": "::paquete" }],
        ],
    }
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
                usuario = controlador_usuario.get_usuario_empleado_user_id(user_id)
                if usuario and usuario['correo'] == correo and usuario['tipo_usuario'] == 'E' :
                    page = f(*args, **kwargs)
                    if page:
                        f_name = f.__name__
                        l_kwarg = list(kwargs.values())
                        f_kwarg = l_kwarg[0] if l_kwarg else None
                        # print(f_name,' - ',f_kwarg) 
                        # try:
                        if request.method == 'GET':
                        # if (usuario['rolid'] == 1 and usuario['tipo_rolid'] == 1) or permiso.validar_acceso(usuario['rolid'] , f_name , f_kwarg ):
                            if permiso.validar_acceso(usuario['rolid'] , f_name , f_kwarg ):
                                return page
                            else:
                                return rdrct_error( main_empleado_page() , 'PAGINA_NO_EXISTE')
                        else: 
                            return page
                        # except Exception as e:
                        #     return rdrct_error( redirect_url('login') , e) 
                    # else:
                    return rdrct_error( main_empleado_page() , 'PAGINA_NO_EXISTE') 
                return rdrct_error( redirect_url('login') , 'LOGIN_INVALIDO') 
            except Exception as e:
                return rdrct_error( redirect_url('login') , e) 
        return wrapper
    return decorator

@app.route("/test_redirect")
def test_redirect():
    page = CONTROLADORES.get('modulo').get('no_crud')
    return redirect(url_for(page))

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
                        return rdrct_error( main_cliente_page() , 'PAGINA_NO_EXISTE') 
                return rdrct_error(redirect_url('login') , 'LOGIN_INVALIDO') 
            except Exception as e:
                return rdrct_error(redirect_url('login') , e) 
        return wrapper
    return decorator


###########_ CONTEXT_PROCESSOR _#############

@app.context_processor
def inject_cur_modulo_id():
    try:
        user_id = request.cookies.get('user_id')
        correo = request.cookies.get('correo')
        usuario = controlador_usuario.get_usuario_empleado_user_id(user_id)
        if  usuario :
            if usuario['correo'] == correo and usuario['tipo_usuario'] == 'E' :
                path = request.path
                parts = path.strip('/').split('=')
                key = parts[-1] 
                page = obtener_funcion_desde_url(app , path)
                if page == 'modulo':
                    dataPage = permiso.get_modulo_key(key)
                    if dataPage:
                        return dict(cur_modulo_id=dataPage['id'])
                else:
                    dataPage = permiso.get_pagina_key(key)
                    if dataPage:
                        if dataPage['tipo_paginaid'] == 2:
                            page_titulo = dataPage['titulo']
                            page_icono  = dataPage['icono']
                            return dict(
                                cur_modulo_id = dataPage['moduloid'] ,
                                page_titulo = page_titulo ,
                                page_icono = page_icono ,
                            )
                        else:
                            return dict(
                                cur_modulo_id = dataPage['moduloid'] ,
                            )
        return dict(cur_modulo_id=None)
    except Exception as e:
        return dict(cur_modulo_id=None)


@app.context_processor
def inject_globals():
    menu_modulos = []
    menu_tipos_paginas = []
    menu_paginas = []
    menu_rolid = None

    main_information = controlador_empresa.get_information()
    cookie_error = request.cookies.get('error')
    options_pagination_crud , selected_option_crud = get_options_pagination_crud()
    user_id = request.cookies.get('user_id')
    datosUsuario = getDatosUsuario()
    if datosUsuario:
        tipoUsuario = getDatosUsuario()['tipo_usuario']
        if tipoUsuario == 'E':
            datosUsuario = controlador_usuario.get_usuario_empleado_user_id(user_id)
            menu_rolid = datosUsuario['rolid']
            if menu_rolid:
                # if menu_rolid == 1 :
                #     menu_modulos = permiso.get_lista_modulos()
                #     menu_tipos_paginas = permiso.get_lista_tipo_paginas()
                #     menu_paginas = permiso.get_paginas()
                # else:
                    menu_modulos = permiso.get_modulos_rol(menu_rolid)
                    menu_tipos_paginas = permiso.get_tipo_paginas_rol(menu_rolid)
                    menu_paginas = permiso.get_paginas_permiso_rol(menu_rolid)
        elif tipoUsuario == 'C':
            datosUsuario = controlador_usuario.get_usuario_cliente_por_id(user_id)
        else:
            datosUsuario = None
    else:
        tipoUsuario = None

    return dict(
        # todo el sistema
        # URL_IMG_LOGO           = f'/static/img/img_empresa/logo.png' ,
        URL_IMG_LOGO           = f'/static/img/img_empresa/{controlador_empresa.get_logo()}' ,
        main_information = main_information ,
        cookie_error = cookie_error,
        datosUsuario = datosUsuario ,
        tipoUsuario = tipoUsuario ,

        # paginas empleado
        options_pagination_crud = options_pagination_crud ,
        selected_option_crud = selected_option_crud ,
        menu_modulos = menu_modulos ,
        menu_tipos_paginas = menu_tipos_paginas , 
        menu_paginas = menu_paginas ,
        menu_rolid = menu_rolid ,
        # paginas cliente


        # constantes
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

PAGINAS_SIMPLES = [ 
    "index" , 
    'pagina_test_rastreo' ,
    'tracking',
    'recuperar_contrasenia',
    'mis_envios',
    'NoRecibimos',
    'pagina_reclamo',
    # 'seguimiento_reclamo',
    'prueba_seguimiento',
    'cajas',
    'cajas_prueba',
    'sobre_nosotros',
    'TerminosCondiciones',
    'mapa_curds',
    # 'cambiar_contrasenia',
    'maestra_para_vb',
    # 'Faq'
]


for pagina in PAGINAS_SIMPLES:
    app.add_url_rule(
        f"/{pagina}",  # URL
        pagina,        # Nombre de la función
        lambda p=pagina: render_template(f"{p}.html")  # Renderiza la plantilla
    )


@app.route("/sign_up")
def sign_up():
    user_id = request.cookies.get('user_id')
    correo = request.cookies.get('correo')
    if user_id and correo: 
        usuario = controlador_usuario.get_usuario_por_id(user_id)
        if usuario and usuario['correo'] == correo :
            if usuario['tipo_usuario'] == 'E':
                return main_empleado_page()
            elif usuario['tipo_usuario'] == 'C' :
                return main_cliente_page()
            
    opts_tipo_documento = controlador_tipo_documento.get_options_dict()
    opts_tipo_cliente = controlador_tipo_cliente.get_options()

    render = render_template(
        'sign_up.html' , 
        opts_tipo_documento = opts_tipo_documento ,
        opts_tipo_cliente = opts_tipo_cliente ,
        )
    resp = make_response(render)
    resp.delete_cookie('user_id')
    resp.delete_cookie('correo')
    return resp


@app.route("/login")
def login():
    user_id = request.cookies.get('user_id')
    correo = request.cookies.get('correo')
    if user_id and correo: 
        usuario = controlador_usuario.get_usuario_por_id(user_id)
        if usuario and usuario['correo'] == correo :
            if usuario['tipo_usuario'] == 'E':
                return main_empleado_page()
            elif usuario['tipo_usuario'] == 'C' :
                return main_cliente_page()
    resp = make_response(render_template('login.html'))
    resp.delete_cookie('user_id')
    resp.delete_cookie('correo')
    return resp


@app.route("/logout")
def logout():
    try:
        resp = make_response(redirect_login())
        resp.delete_cookie('user_id')
        resp.delete_cookie('correo')
        return resp
    except Exception as e:
        return rdrct_error(redirect_login(),e)


@app.route("/libro_reclamaciones")
def libro_reclamaciones():
    opts_tipo_documento = controlador_tipo_documento.get_options_dict()
    departamentos = controlador_sucursal.get_options_departamento_sucursal()
    provincias = controlador_sucursal.get_options_provincia_sucursal()
    distritos = controlador_sucursal.get_options_distrito_sucursal()
    sucursales = controlador_sucursal.get_options_ubigeo_sucursal() 
    tipos_reclamo = controlador_reclamo.get_dict_tipo_reclamo()
    motivos_reclamo = controlador_reclamo.get_dict_motivo_reclamo()
    causas_reclamo = controlador_reclamo.get_dict_causa_reclamo()
    bienes_contratados = controlador_reclamo.get_list_bien_contratado()

    return render_template(
        'libro_reclamaciones.html' ,
        opts_tipo_documento = opts_tipo_documento ,

        departamentos = departamentos ,
        provincias = provincias ,
        distritos = distritos ,
        sucursales = sucursales ,

        tipos_reclamo =tipos_reclamo ,
        motivos_reclamo = motivos_reclamo ,
        causas_reclamo = causas_reclamo ,

        bienes_contratados = bienes_contratados ,
    )



@app.route("/registrar_reclamo", methods=["POST"])
def registrar_reclamo():
    # try:

        ahora = datetime.now()
        formateado = ahora.strftime("%Y_%m_%d_%H_%M_%S")

        firma = inspect.signature(controlador_reclamo.registrar_reclamo)

        valores = []
        for nombre, parametro in firma.parameters.items():
            if nombre in request.files:
                archivo = request.files[nombre]
                if archivo.filename != "":
                    nuevo_nombre = guardar_imagen_bd('reclamo' ,f'{formateado}_',archivo)
                    valores.append(nuevo_nombre)
                else:
                    valores.append(request.form.get(f"{nombre}_actual"))
            else:
                valor = request.form.get(nombre)
                valores.append(valor)

        controlador_reclamo.registrar_reclamo( *valores )
        return redirect(url_for('libro_reclamaciones'))


    # except Exception as e:
    #     return rdrct_error(redirect_url('main_page')  , e)


@app.route("/cotizador")
def cotizador():
    departamentos = controlador_tarifa_ruta.get_options_departamento_origen()
    provincias = controlador_tarifa_ruta.get_options_provincia_origen()
    distritos = controlador_tarifa_ruta.get_options_distrito_origen()
    sucursales = controlador_tarifa_ruta.get_options_sucursal_origen() 
    return render_template(
        'cotizador.html' ,
        departamentos = departamentos,
        provincias = provincias,
        distritos = distritos,
        sucursales = sucursales,
    )


@app.route("/api/calculate_tarifa", methods=["POST"])
def api_calculate_tarifa():
    try:
        data = request.get_json()
        origen_id = data.get("origen_id")
        destino_id = data.get("destino_id")
        valor = data.get('valor')
        includeRecojo = data.get('includeRecojo')
        peso = data.get('peso')

        if origen_id is None or destino_id is None or includeRecojo is None or peso is None:
            return jsonify({"error": f" {data} "}), 400

        tarifa = controlador_tarifa_ruta.get_tarifa_ids(origen_id, destino_id)
        regla_p = controlador_regla_cargo.get_regla_cargo_condicion( 'P' , peso )
        regla_v = controlador_regla_cargo.get_regla_cargo_condicion( 'V' , valor )

        tarifa_ruta = Decimal(str(tarifa['tarifa'])) if tarifa else Decimal('0')
        porcentaje_recojo = Decimal(str(controlador_empresa.get_porcentaje_recojo())) if includeRecojo == '1' else Decimal('0')
        porcentaje_peso = Decimal(str(regla_p['porcentaje'])) if regla_p else Decimal('0')
        porcentaje_valor = Decimal(str(regla_v['porcentaje'])) if regla_v else Decimal('0')

        respuesta = controlador_tarifa_ruta.calcularTarifaTotal( tarifa_ruta , peso , porcentaje_recojo , porcentaje_valor , porcentaje_peso )
        return jsonify(respuesta)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/datos_destino", methods=["GET"])
def api_sucursales_por_ubigeo():
    sucursal_id = request.args.get("sucursal_id")
    if not sucursal_id:
        return jsonify({"error": "ID de sucursal proporcionado"}), 400
  
    try:
        departamentos = controlador_tarifa_ruta.get_options_departamento_destino(sucursal_id)
        provincias = controlador_tarifa_ruta.get_options_provincia_destino(sucursal_id)
        distritos = controlador_tarifa_ruta.get_options_distrito_destino(sucursal_id)
        sucursales = controlador_tarifa_ruta.get_options_sucursal_destino(sucursal_id)
        return jsonify({
            "departamentos": departamentos ,
            "provincias": provincias ,
            "distritos": distritos ,
            "sucursales": sucursales ,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/api/Faq')
def api_Faq():
    columnas, filas = controlador_pregunta_frecuente.get_table()
    # Filtrar solo activas
    preguntas_activas = [f for f in filas if f['activo'] == 1]
    return jsonify(preguntas_activas)

@app.route('/api/marca/update', methods=['POST'])
def update_marca():
    try:
        # Obtener los datos del cuerpo de la solicitud en formato JSON
        data = request.get_json()

        # Extraer los valores de los parámetros necesarios
        id = data.get('id')
        nombre = data.get('nombre')

        # Validar que se reciban los datos correctos
        if not id or not nombre:
            return jsonify({'success': False, 'message': 'Faltan parámetros'}), 400
        
        # Actualizar la fila de la marca en la base de datos
        sql = f'''
            UPDATE marca 
            SET nombre = %s 
            WHERE id = %s
        '''
        bd.sql_execute(sql, (nombre, id))  

        # Ejecutar el SQL para actualizar la marca
        
        return jsonify({'success': True, 'message': 'Marca actualizada correctamente'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')


@app.route('/enviar-formulario', methods=['POST'])
def enviar_formulario():
    try:
        data = request.json  # esperamos JSON en el fetch del frontend
        
        nombre = data.get('nombreCompleto', '').strip()
        nro_documento = data.get('numeroDocumento', '').strip()
        correo = data.get('email', '').strip()
        telefono = data.get('telefono', '').strip()
        mensaje = data.get('mensaje', '').strip()
        tipo_documentoid = data.get('tipoDocumentoId')  # si manejas tipos de doc, o null
        tipo_clienteid = data.get('tipoClienteId')
        sucursalid = data.get('sucursalId')
        
        # Validaciones básicas
        if not (nombre and nro_documento and correo and telefono and mensaje and tipo_clienteid and sucursalid):
            return jsonify({'success': False}), 400  # Solo devolvemos un estado de error

        sql = '''
            INSERT INTO mensaje_contacto 
            (nombre, nro_documento, correo, telefono, mensaje, tipo_documentoid, tipo_clienteid, sucursalid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        sql_execute(sql, (nombre, nro_documento, correo, telefono, mensaje, tipo_documentoid, tipo_clienteid, sucursalid))
        
        return jsonify({'success': True})  # Solo devolvemos un estado de éxito sin mensaje
    except Exception as e:
        return jsonify({'success': False}), 500  # Solo devolvemos un estado de error


@app.route('/api/tipo_cliente')
def api_tipo_cliente():
    from controladores import controlador_tipo_cliente
    opciones = controlador_tipo_cliente.get_options()
    # convertir lista de tuplas a lista de dicts
    data = [{'id': o[0], 'nombre': o[1]} for o in opciones]
    return jsonify(data)


@app.route('/api/sucursales_simple')
def api_sucursales_simple():
    # from controladores import controlador_sucursal
    opciones = controlador_sucursal.get_ubigeo_sucursal()
    data = [{'id': o['id'], 'direccion': o['direccion_completa']} for o in opciones]
    return jsonify(data)


@app.route('/api/tipo_documento')
def api_tipo_documento():
    from controladores import controlador_tipo_documento
    opciones = controlador_tipo_documento.get_options()
    data = [{'id': o[0], 'nombre': o[1]} for o in opciones]
    return jsonify(data)


@app.route("/api/cajas")
def api_cajas():
    filas = controlador_articulo.get_table_cajas()
    productSizes = {}

    for fila in filas:
        if not fila['activo'] :
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
                "image": f"/static/img/img_articulo/{(fila['img'] or '')}",
                "size_name": fila['tam_nombre'] or '',
                "id": fila['articuloid'] ,
                "discounts": [] 
            }

        if fila['cantidad_descuento'] and fila['nom_descuento']:
            productSizes[key]['discounts'].append({
                "name": fila['nom_descuento'],  
                "value": float(fila['cantidad_descuento'])
            })
    return jsonify(productSizes)


@app.route("/articulos")
def articulos():
    return render_template('articulos.html')


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
                "id": fila['articuloid'],
                "name_product": fila['nom_articulo'],
                "price": float(fila['precio']),
                "stock": fila['stock'],
                "dimensions": fila['dimensiones'] or '',
                "image": f"/static/img/img_articulo/{fila['img'] or ''}",
                "size_name": fila['tam_nombre'] or '',
                "discounts": [],
                "cantidad_precio_unitario_2": None,
                "precio_unitario_2": None,
                "cantidad_precio_unitario_3": None,
                "precio_unitario_3": None
            }

        if fila['cantidad_descuento'] and fila['volumen']:
            articulos[key]["discounts"].append({
                "name": fila['nom_descuento'],
                "value": float(fila['cantidad_descuento']),
                "volumen": int(fila['volumen'])
            })

    for articulo in articulos.values():
        ordenados = sorted(articulo['discounts'], key=lambda x: x['volumen'])
        if len(ordenados) >= 1:
            articulo["cantidad_precio_unitario_2"] = ordenados[0]["volumen"]
            articulo["precio_unitario_2"] = ordenados[0]["value"]
        if len(ordenados) >= 2:
            articulo["cantidad_precio_unitario_3"] = ordenados[1]["volumen"]
            articulo["precio_unitario_3"] = ordenados[1]["value"]

    return jsonify(articulos)


@app.route("/carrito")
def carrito():
    return render_template('carrito.html')

@app.route("/obtener-carrito", methods=["GET"])
def obtener_carrito():
    clientecorreo = request.cookies.get('correo')
    if not clientecorreo:
        return jsonify({"error": "No se encontró la cookie de correo"}), 400

    cliente = controlador_cliente.get_cliente_por_correo(clientecorreo)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    clienteid = cliente.get("id")
    if not clienteid:
        return jsonify({"error": "Cliente sin ID válido"}), 400

    datos = controlador_transaccion_venta.obtener_carrito_cliente(clienteid)
    if isinstance(datos, Exception):
        return jsonify({"error": str(datos)}), 500

    return jsonify(datos)

@app.route("/registrar-item-carrito", methods=["POST"])
def registrar_item_carrito():
    data = request.get_json()
    # print(f"{data}")
    # for i in range (1,3):
    #     print(f"{i}. {data}")
    articuloid = data.get("articuloid")
    cantidad = data.get("cantidad")
    tipo_comprobanteid = 2  # Provisionalmente fijo

    # clienteid = request.cookies.get("idlogin")
    # clienteid = data.get("clienteid", 1)
    clientecorreo = request.cookies.get('correo')
    if not clientecorreo:
        return jsonify({"error": "No se encontró la cookie de correo"}), 400

    cliente = controlador_cliente.get_cliente_por_correo(clientecorreo)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    clienteid = cliente.get("id")
    if not clienteid:
        return jsonify({"error": "Cliente sin ID válido"}), 400

    try:
        num_serie = controlador_transaccion_venta.registrar_detalle_venta(
            clienteid=int(clienteid),
            tipo_comprobanteid=tipo_comprobanteid,
            articuloid=int(articuloid),
            cantidad=int(cantidad)
        )
        return jsonify({"mensaje": "Item registrado en carrito", "num_serie": num_serie}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/agregar-item-carrito", methods=["POST"])
def registrar_item_carrito_json():
    data = request.get_json()

    articuloid = data.get("articuloid")
    cantidad = data.get("cantidad")
    clienteid = data.get("clienteid")
    tipo_comprobanteid = 2  # Provisionalmente fijo

    if not clienteid:
        return jsonify({"error": "clienteid no proporcionado en el JSON"}), 400

    try:
        num_serie = controlador_transaccion_venta.registrar_detalle_venta(
            clienteid=int(clienteid),
            tipo_comprobanteid=tipo_comprobanteid,
            articuloid=int(articuloid),
            cantidad=int(cantidad)
        )
        return jsonify({"mensaje": "Item registrado en carrito", "num_serie": num_serie}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/eliminar-item-carrito", methods=["POST"])
def eliminar_item_carrito():
    data = request.get_json()
    # clienteid = data.get("clienteid")
    articuloid = data.get("articuloid")

    clientecorreo = request.cookies.get('correo')
    if not clientecorreo:
        return jsonify({"error": "No se encontró la cookie de correo"}), 400

    cliente = controlador_cliente.get_cliente_por_correo(clientecorreo)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    clienteid = cliente.get("id")
    if not clienteid:
        return jsonify({"error": "Cliente sin ID válido"}), 400

    transaccion = controlador_transaccion_venta.obtener_transaccion_provisional(clienteid)
    if not transaccion:
        return jsonify({"error": "No hay transacción activa"}), 404

    num_serie = transaccion["num_serie"]
    controlador_transaccion_venta.eliminar_detalle_venta(articuloid, num_serie)
    controlador_transaccion_venta.actualizar_monto_total(num_serie)

    return jsonify({"success": True})


@app.route("/vaciar-carrito", methods=["POST"])
def vaciar_carrito():
    data = request.get_json()
    # clienteid = data.get("clienteid")
    clientecorreo = request.cookies.get('correo')
    if not clientecorreo:
        return jsonify({"error": "No se encontró la cookie de correo"}), 400

    cliente = controlador_cliente.get_cliente_por_correo(clientecorreo)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    clienteid = cliente.get("id")
    if not clienteid:
        return jsonify({"error": "Cliente sin ID válido"}), 400

    transaccion = controlador_transaccion_venta.obtener_transaccion_provisional(clienteid)
    if not transaccion:
        return jsonify({"error": "No hay carrito"}), 404

    num_serie = transaccion["num_serie"]
    controlador_transaccion_venta.eliminar_todo_detalle_venta(num_serie)
    controlador_transaccion_venta.actualizar_monto_total(num_serie)

    return jsonify({"success": True})

@app.route("/obtener-resumen-pago", methods=["GET"])
def obtener_resumen_pago():
    # clienteid = 1  # O request.cookies.get("idlogin")

    clientecorreo = request.cookies.get('correo')
    if not clientecorreo:
        return jsonify({"error": "No se encontró la cookie de correo"}), 400

    cliente = controlador_cliente.get_cliente_por_correo(clientecorreo)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    clienteid = cliente.get("id")
    if not clienteid:
        return jsonify({"error": "Cliente sin ID válido"}), 400

    transaccion = controlador_transaccion_venta.obtener_transaccion_provisional(clienteid)
    if not transaccion:
        return jsonify({"error": "No hay transacción activa"}), 404

    num_serie = transaccion["num_serie"]
    total = controlador_transaccion_venta.obtener_monto_total(num_serie)
    detalles = controlador_transaccion_venta.obtener_carrito_cliente(clienteid)

    cantidad_total = sum(item["quantity"] for item in detalles)
    subtotal = float(total) / 1.18
    igv = float(total) - subtotal

    resumen = {
        "cantidad": cantidad_total,
        "subtotal": round(subtotal, 2),
        "igv": round(igv, 2),
        "total": round(float(total), 2)
    }

    # print(f"resumen : {resumen}")

    return jsonify(resumen)


@app.route("/metodo_pago")
def metodo_pago():
    # clienteid = 1  # O request.cookies.get("idlogin")
    clientecorreo = request.cookies.get('correo')
    if not clientecorreo:
        return jsonify({"error": "No se encontró la cookie de correo"}), 400

    cliente = controlador_cliente.get_cliente_por_correo(clientecorreo)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    clienteid = cliente.get("id")
    if not clienteid:
        return jsonify({"error": "Cliente sin ID válido"}), 400

    transaccion = controlador_transaccion_venta.obtener_transaccion_provisional(clienteid)
    if not transaccion:
        return redirect("/carrito")  # o muestra un mensaje apropiado

    return render_template("metodo_pago.html")


@app.route("/confirmar-pago", methods=["POST"])
def confirmar_pago():
    try:
        # Obtener el correo desde las cookies
        clientecorreo = request.cookies.get("correo")
        if not clientecorreo:
            return jsonify({"error": "No se encontró el correo del cliente"}), 400

        # Buscar cliente por correo
        cliente = controlador_cliente.get_cliente_por_correo(clientecorreo)
        if not cliente:
            return jsonify({"error": "Cliente no encontrado"}), 404

        clienteid = cliente.get("id")
        if not clienteid:
            return jsonify({"error": "Cliente sin ID válido"}), 400

        # Obtener transacción provisional
        transaccion = controlador_transaccion_venta.obtener_transaccion_provisional(clienteid)
        if not transaccion:
            return jsonify({"error": "No hay transacción activa"}), 400

        num_serie = transaccion["num_serie"]

        # Actualizar estado a pagado
        sql = '''
            UPDATE transaccion_venta SET estado = 1 WHERE num_serie = %s
        '''
        sql_execute(sql, (num_serie,))

        return jsonify({"mensaje": "Pago confirmado"}), 200

    except Exception as e:
        print("Error en confirmar_pago:", e)
        return jsonify({"error": "Ocurrió un error al procesar el pago"}), 500


@app.route("/venta/registrar", methods=["POST"])
def registrar_venta():
    data = request.get_json()

    cliente_id = data.get("cliente_id")
    tipo_comprobante_id = data.get("tipo_comprobante_id")
    metodo_pago_id = data.get("metodo_pago_id")
    articulos = data.get("articulos", [])

    if not cliente_id or not tipo_comprobante_id or not metodo_pago_id or not articulos:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    try:
        # Calcular monto total
        monto_total = 0
        for item in articulos:
            precio = controlador_articulo.obtener_precio_articulo(item["articulo_id"])
            if precio is None:
                return jsonify({"error": f"Artículo {item['articulo_id']} no encontrado"}), 404
            monto_total += precio * item["cantidad"]

        # Insertar cabecera de venta
        venta_id = controlador_transaccion_venta.registrar_transaccion(
            tipo_comprobante_id,
            monto_total,
            cliente_id
        )

        # Insertar cada detalle
        for item in articulos:
            controlador_detalle_venta.registrar_detalle_venta(
                item["articulo_id"],
                venta_id,
                tipo_comprobante_id,
                item["cantidad"]
            )

        # Insertar método de pago
        controlador_metodo_pago_venta.registrar_metodo_pago_venta(
            venta_id,
            tipo_comprobante_id,
            metodo_pago_id
        )

        return jsonify({"status": "ok", "venta_id": venta_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/faq")
def Faq():
    return render_template('Faq.html')


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


##############erliz rutas####


@app.route('/tipos-envio')
def tipos_envio():
    tipos_envios = controlador_tipo_empaque.get_options()
    return render_template('tipos_envio.html', tipos_envios=tipos_envios)



@app.route('/registro-envio')
def registro_envio():
    data_envio = session.get('data_envio')
    
    if data_envio:
        return redirect(url_for('mostrar_resumen_envio'))
    nombre_doc = controlador_tipo_documento.get_options()
    nombre_rep = controlador_tipo_recepcion.get_options()
    rutas_tarifas = controlador_tarifa_ruta.get_sucursales_origen_destino()
    articulos = controlador_contenido_paquete.get_options()
    empaque = controlador_tipo_empaque.get_options()
    condiciones = controlador_regla_cargo.get_condiciones_tarifa()
    tarifas = controlador_tarifa_ruta.get_tarifas_ruta_dict()
    return render_template('registro_envio.html', 
                           nombre_doc=nombre_doc,
                           nombre_rep=nombre_rep,
                           rutasTarifas=json.dumps(rutas_tarifas), 
                           tarifas = json.dumps(tarifas),
                           empaque=empaque, 
                           articulos=articulos,
                           condiciones=condiciones)
    

@app.route('/guardar_datos_envio', methods=['POST'])
def guardar_datos_envio():
    data = request.json  # datos enviados desde JS por fetch

    # Guardar datos en la sesión
    user = controlador_encomiendasss.consultar_tarifa(data['id_origen'], data['id_destino'])
    data['tarifa'] = user
    subtotal = round(float(user) + float(data['valor_paquete']), 2)
    igv = round(subtotal * 0.18, 2)
    total = round(subtotal + igv, 2)
    data['total'] = total

    session['data_envio'] = data

    print("Datos guardados en la sesión:", data)

    return jsonify({"redirect_url": url_for('mostrar_resumen_envio')})

app.secret_key = 'clave_secreta_segura'  # deberías usar una segura en producción


@app.route('/resumen_envio')
def mostrar_resumen_envio():
    data_envio = session.get('data_envio')
    
    if not data_envio:
        return redirect(url_for('registro_envio'))  # si no hay datos, redirige

    return render_template('resumen_envio.html', data_envio=data_envio)

@app.route('/eliminar_envio', methods=['POST'])
def eliminar_envio():
    try:
        # Limpiar los datos de la sesión
        session.pop('data_envio', None)
        return redirect(url_for('registro_envio'))
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/pagar_encomienda')
def pagar_encomienda():
    data_envio = session.get('data_envio')

    
    
    if not data_envio:
        return redirect(url_for('registro_envio'))

    # Calcular valores si es necesario
    subtotal = float(data_envio.get('valor_paquete', 0)) + float(data_envio.get('tarifa', 0))
    igv = round(subtotal * 0.18, 2)
    total = round(subtotal + igv, 2)

    return render_template('pago_encomienda.html',
                           data_envio=data_envio,
                           subtotal=subtotal,
                           igv=igv,
                           total=total)
    


@app.route('/confirmar_pagoenco', methods=['POST'])
def confirmar_pagoenco():
    try:
        data_envio = session.get('data_envio')
        metodo_pago = request.form.get('metodo-pago')
        clave = 123
        if not data_envio:
            return jsonify({"success": False, "message": "No hay datos de envío"}), 400

        controlador_encomiendasss.insertar_pago_2(data_envio, metodo_pago, clave)

        session.pop('data_envio', None)

        return redirect(url_for('registro_envio'))
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
        
    


@app.route('/seguimiento_encomienda')
def seguimiento_encomienda():
    estado_encomienda = controlador_estado_encomienda.get_last_state()
    return render_template('seguimiento.html',estado_encomienda=estado_encomienda)


# @app.route('/resumen_envio_prueba', methods=['POST'])
# def resumen_envio_prueba():
#     try:
#         raw = request.form.get('payload')
#         print("Payload recibido:", raw)
        
#         if not raw:
#             return "No se recibió payload", 400

#         # Obtener datos del request
#         data = json.loads(raw)
#         print("Datos parseados:", data)
        
#         if not data:
#             return jsonify({
#                 'error': 'No se recibieron datos',
#                 'message': 'El request no contiene datos JSON válidos'
#             }), 400

#         # Extraer información del payload
#         envios = data.get('registros', [])
#         remitente = data.get('remitente', {})
#         origen = data.get('origen', {})
#         modo_envio = data.get('modo', 'individual')

#         # Validaciones básicas
#         if not envios:
#             return render_template('resumen_envio_prueba.html',
#                                  error_message='No se encontraron envíos para procesar',
#                                  envios=[],
#                                  remitente={},
#                                  origen={},
#                                  tipo_envio='')

#         # Procesar cada envío para calcular tarifas
#         for i, envio in enumerate(envios):
#             try:
#                 # Mejor manejo de origen/destino
#                 origen_id = envio.get('origen', {}).get('sucursal_origen') or origen.get('sucursal_origen')
#                 destino_id = envio.get('destino', {}).get('sucursal_destino')
                
#                 if not origen_id or not destino_id:
#                     print(f"Error: origen_id={origen_id}, destino_id={destino_id} para envío {i}")
#                     continue
                
#                 valor = Decimal(str(envio.get('valorEnvio', 0)))
#                 peso = Decimal(str(envio.get('peso', 0)))

#                 # Obtener tarifas
#                 tarifa_row = controlador_tarifa_ruta.get_tarifa_ids(origen_id, destino_id) or {}
#                 tarifa_base = Decimal(str(tarifa_row.get('tarifa', 0)))

#                 # Obtener reglas de cargo
#                 regla_p = controlador_regla_cargo.get_regla_cargo_condicion('P', float(peso)) or {}
#                 regla_v = controlador_regla_cargo.get_regla_cargo_condicion('V', float(valor)) or {}
#                 porcentaje_p = Decimal(str(regla_p.get('porcentaje', 0)))
#                 porcentaje_v = Decimal(str(regla_v.get('porcentaje', 0)))
#                 porcentaje_r = Decimal(str(controlador_empresa.get_porcentaje_recojo()))

#                 # Calcular tarifa total
#                 total = controlador_tarifa_ruta.calcularTarifaTotal(
#                     tarifa_base, peso, porcentaje_r, porcentaje_v, porcentaje_p
#                 )
#                 envios[i]['tarifa'] = float(total)  # Convertir a float para JSON
                
#                 print(f"Envío {i}: tarifa calculada = {total}")
                
#             except Exception as e:
#                 print(f"Error calculando tarifa para envío {i}: {str(e)}")
#                 envios[i]['tarifa'] = 0

#         # GUARDAR EN SESIÓN PARA EL SIGUIENTE PASO
#         session['resumen_envios'] = envios
#         session['remitente_data'] = remitente
#         session['origen_data'] = origen
#         session['tipo_envio'] = modo_envio

#         # Log para debugging
#         print(f"Procesando {len(envios)} envíos de tipo {modo_envio}")
#         print(f"Remitente: {remitente.get('nombre_remitente', 'No especificado')}")
#         print(f"Datos guardados en sesión para pago_envio_prueba")

#         # Renderizar la plantilla con los datos
#         return render_template('resumen_envio_prueba.html',
#                              envios=envios,
#                              remitente=remitente,
#                              origen=origen,
#                              tipo_envio=modo_envio,
#                              error_message=None)

        
#     except Exception as e:
#         print(f"Error en resumen_envio_prueba: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({
#             'error': 'Error procesando resumen',
#             'message': str(e)
#         }), 500


#     except Exception as e:
#         print(f"Error en resumen_envio_prueba: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({
#             'error': 'Error procesando resumen',
#             'message': str(e)
#         }), 500

@app.route('/resumen_envio_prueba', methods=['POST'])
def resumen_envio_prueba():
    try:
        raw = request.form.get('payload')
        print("Payload recibido:", raw)
        
        if not raw:
            return "No se recibió payload", 400

        # Obtener datos del request
        data = json.loads(raw)
        print("Datos parseados:", data)
        
        if not data:
            return jsonify({
                'error': 'No se recibieron datos',
                'message': 'El request no contiene datos JSON válidos'
            }), 400

        # Extraer información del payload
        envios = data.get('registros', [])
        remitente = data.get('remitente', {})
        origen = data.get('origen', {})
        modo_envio = data.get('modo', 'individual')

        # Validaciones básicas
        if not envios:
            return render_template('resumen_envio_prueba.html',
                                 error_message='No se encontraron envíos para procesar',
                                 envios=[],
                                 remitente={},
                                 origen={},
                                 tipo_envio='')

        # Procesar cada envío para calcular tarifas
        for i, envio in enumerate(envios):
            try:
                # Mejor manejo de origen/destino
                origen_id = envio.get('origen', {}).get('sucursal_origen') or origen.get('sucursal_origen')
                destino_id = envio.get('destino', {}).get('sucursal_destino')
                
                if not origen_id or not destino_id:
                    print(f"Error: origen_id={origen_id}, destino_id={destino_id} para envío {i}")
                    continue
                
                valor = Decimal(str(envio.get('valorEnvio', 0)))
                peso = Decimal(str(envio.get('peso', 0)))

                # Obtener tarifas
                tarifa_row = controlador_tarifa_ruta.get_tarifa_ids(origen_id, destino_id) or {}
                tarifa_base = Decimal(str(tarifa_row.get('tarifa', 0)))

                # Obtener reglas de cargo
                regla_p = controlador_regla_cargo.get_regla_cargo_condicion('P', float(peso)) or {}
                regla_v = controlador_regla_cargo.get_regla_cargo_condicion('V', float(valor)) or {}
                porcentaje_p = Decimal(str(regla_p.get('porcentaje', 0)))
                porcentaje_v = Decimal(str(regla_v.get('porcentaje', 0)))
                porcentaje_r = Decimal(str(controlador_empresa.get_porcentaje_recojo()))

                # Calcular tarifa total
                total = controlador_tarifa_ruta.calcularTarifaTotal(
                    tarifa_base, peso, porcentaje_r, porcentaje_v, porcentaje_p
                )
                envios[i]['tarifa'] = float(total)  # Convertir a float para JSON
                
                print(f"Envío {i}: tarifa calculada = {total}")
                
            except Exception as e:
                print(f"Error calculando tarifa para envío {i}: {str(e)}")
                envios[i]['tarifa'] = 0

        # GUARDAR EN SESIÓN PARA EL SIGUIENTE PASO
        session['resumen_envios'] = envios
        session['remitente_data'] = remitente
        session['origen_data'] = origen
        session['tipo_envio'] = modo_envio

        # Log para debugging
        print(f"Procesando {len(envios)} envíos de tipo {modo_envio}")
        print(f"Remitente: {remitente.get('nombre_remitente', 'No especificado')}")
        print(f"Datos guardados en sesión para pago_envio_prueba")

        # Renderizar la plantilla con los datos
        return render_template('resumen_envio_prueba.html',
                             envios=envios,
                             remitente=remitente,
                             origen=origen,
                             tipo_envio=modo_envio,
                             error_message=None)

    except Exception as e:
        print(f"Error en resumen_envio_prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Error procesando resumen',
            'message': str(e)
        }), 500


@app.route('/pago_envio_prueba', methods=['POST'])
def pago_envio_prueba():
    try:
        # Obtener datos del formulario
        envios_data = request.form.get('envios_data')
        remitente_data = request.form.get('remitente_data')
        origen_data = request.form.get('origen_data')
        tipo_envio = request.form.get('tipo_envio')
        
        print(f"Datos recibidos del formulario:")
        print(f"- Número de envíos: {len(json.loads(envios_data)) if envios_data else 0}")
        print(f"- Tipo envío: {tipo_envio}")
        
        # Convertir de JSON string a objetos Python
        if not envios_data:
            return redirect(url_for('tipos_envio'))
            
        envios = json.loads(envios_data)
        remitente = json.loads(remitente_data) if remitente_data else {}
        origen = json.loads(origen_data) if origen_data else {}
        
        if not envios:
            return redirect(url_for('tipos_envio'))
        
        # Separar envíos por modalidad de pago
        envios_pago_online = [envio for envio in envios if envio.get('modalidadPago') == '1']
        envios_otras_modalidades = [envio for envio in envios if envio.get('modalidadPago') != '1']
        
        # Calcular totales
        total_general = sum(float(envio.get('tarifa', 0)) for envio in envios)
        total_pago_online = sum(float(envio.get('tarifa', 0)) for envio in envios_pago_online)
        total_otras_modalidades = sum(float(envio.get('tarifa', 0)) for envio in envios_otras_modalidades)
        
        # Detectar si hay envíos con modalidad de pago 1 (pago en línea)
        tiene_pago_online = len(envios_pago_online) > 0
        
        print(f"Total general: S/ {total_general}")
        print(f"Total pago online: S/ {total_pago_online}")
        print(f"Total otras modalidades: S/ {total_otras_modalidades}")
        print(f"¿Tiene pago online?: {tiene_pago_online}")
        print(f"Envíos pago online: {len(envios_pago_online)}")
        print(f"Envíos otras modalidades: {len(envios_otras_modalidades)}")
        
        # Guardar datos para el proceso de pago
        session['datos_pago'] = {
            'envios': envios,
            'envios_pago_online': envios_pago_online,
            'envios_otras_modalidades': envios_otras_modalidades,
            'remitente': remitente,
            'origen': origen,
            'tipo_envio': tipo_envio,
            'total_general': total_general,
            'total_pago_online': total_pago_online,
            'total_otras_modalidades': total_otras_modalidades,
            'tiene_pago_online': tiene_pago_online
        }
        
        # Obtener opciones de pago solo si hay modalidad 1
        tipos_comprobante = []
        metodos_pago = []
        
        if tiene_pago_online:
            tipos_comprobante = controlador_tipo_comprobante.get_tipo_comprobante_by_tipo()
            metodos_pago = controlador_metodo_pago.get_metodo_pago_online()
        
        return render_template('pago_envio_prueba.html',
                             envios=envios,
                             envios_pago_online=envios_pago_online,
                             envios_otras_modalidades=envios_otras_modalidades,
                             remitente=remitente,
                             origen=origen,
                             tipo_envio=tipo_envio,
                             total_general=total_general,
                             total_pago_online=total_pago_online,
                             total_otras_modalidades=total_otras_modalidades,
                             tiene_pago_online=tiene_pago_online,
                             tipos_comprobante=tipos_comprobante,
                             metodos_pago=metodos_pago)
        
        
    except Exception as e:
        print(f"Error en pago_envio_prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Error procesando pago',
            'message': str(e)
        }), 500


@app.route('/resumen')
def resumen():
    resultados = session.get('resumen_envios')
    if not resultados:
        return redirect(url_for('envio_masivo'))

    return render_template('resumen_envio.html', registros=resultados)


@app.route('/pagoenvio')
def mostrar_pagoenvio():
    tipo_comprobante = controlador_tipo_comprobante.get_options_nombre()
    
    metodo_pago = controlador_metodo_pago.get_options()
    return render_template('pago_envio.html', metodo_pago=metodo_pago,tipo_comprobante=tipo_comprobante
                           ) 


@app.route('/pago_envio', methods=['GET', 'POST'])
def pago_envio():
    registros = session.get('resumen_envios')
    if not registros:
        return redirect(url_for('resumen'))

    subtotal = sum(Decimal(str(r['tarifa'])) for r in registros)
    subtotal = subtotal.quantize(Decimal('0.01'), ROUND_HALF_UP)
    igv      = (subtotal * IGV_RATE).quantize(Decimal('0.01'), ROUND_HALF_UP)
    total    = (subtotal + igv).quantize(Decimal('0.01'), ROUND_HALF_UP)

    tipo_comprobante = controlador_tipo_comprobante.get_options_nombre()
    metodo_pago      = controlador_metodo_pago.get_options()

    modalidadPago = registros[0].get('modalidadPago', '')
    print(modalidadPago)

    return render_template('pago_envio.html',
                           registros=registros,
                           cantidad_envios=len(registros),
                           subtotal=subtotal,
                           igv=igv,
                           total=total,
                           modalidadPago=modalidadPago,
                           tipo_comprobante=tipo_comprobante,
                           metodo_pago=metodo_pago)



@app.route('/insertar_envio', methods=['POST'])
def insertar_envio():
    try:
        nombre_empresa = controlador_empresa.get_nombre()
        data = request.get_json()
        if not data:
            return jsonify({'status':'error','message':'No se recibió un JSON válido'}), 400

        tipo_comprobante = data.get('tipo_comprobante')
        registros = session.get('resumen_envios')
        if not registros:
            return jsonify({'status':'error','message':'No hay envíos en sesión'}), 400

        remitente = registros[0].get('remitente', {})
        nombre = remitente.get('nombre_remitente','')
        partes = nombre.split() if nombre else []
        cliente_data = {
            'correo':        remitente.get('correo_remitente',''),
            'telefono':      remitente.get('num_tel_remitente',''),
            'num_documento': remitente.get('num_doc_remitente',''),
            'nombre_siglas': partes[0] if partes else '',
            'apellidos_razon': ' '.join(partes[1:]) if len(partes)>1 else '',
            'tipo_documentoid': int(remitente.get('tipo_doc_remitente',1)),
            'tipo_clienteid':   2 if remitente.get('tipo_doc_remitente')==2 else 1
        }
        # 1) Creamos transacción y paquetes
        num_serie = controlador_encomienda.crear_transaccion_y_paquetes(
            registros, cliente_data, tipo_comprobante
        )

        # 2) Generamos QR para cada paquete (no bloqueante)
        if num_serie:
            try:
                generar_qr_paquetes(registros, num_serie)
            except Exception as qr_err:
                current_app.logger.warning(f"Error generando QR: {qr_err}")

            # 3) Preparamos y enviamos el correo al remitente
            destinatario_email = cliente_data['correo']
            msg = Message(
                subject=f"{nombre_empresa} Envío registrado: {num_serie}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[destinatario_email]
            )
            msg.body = (
                f"Hola {cliente_data['nombre_siglas']},\n\n"
                f"Tu envío con número de serie {num_serie} ha sido registrado exitosamente.\n"
                "Adjunto encontrarás los códigos QR para el seguimiento de cada paquete.\n\n"
                f"¡Gracias por confiar en {nombre_empresa} "
            )

            for r in registros:
                clave = r['clave']
                qr_path = os.path.join(
                    app.static_folder, 'comprobantes', clave, 'qr.png'
                )
                if os.path.exists(qr_path):
                    with open(qr_path, 'rb') as f:
                        qr_data = f.read()
                    msg.attach(f"qr_{clave}.png", 'image/png', qr_data)
                else:
                    current_app.logger.warning(f"QR no encontrado para clave {clave}")

            mail.send(msg)

        current_app.logger.info(f"Transacción creada con número de serie: {num_serie}")
        return jsonify({
            'status': 'success',
            'message': 'Transacción creada correctamente',
            'num_serie': num_serie
        }), 201

    except ValueError as ve:
        current_app.logger.warning(f"Bad request: {ve}")
        return jsonify({'status':'error','message':str(ve)}), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Ocurrió un error al procesar el envío: {repr(e)}'
        }), 500
        
        
@app.route('/insertar_envio_api', methods=['POST'])
def insertar_envio_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        # Obtener datos de la sesión
        registros = session.get('resumen_envios', [])
        modo = session.get('tipo_envio')
        origen_data = session.get('origen_data')
        sucursal_origen = origen_data.get('sucursal_origen') if isinstance(origen_data, dict) else origen_data
        remitente = session.get('remitente_data', {})
        
        # Validaciones
        if not registros:
            return jsonify({'status': 'error', 'message': 'No hay registros de paquetes'}), 400
            
        if not sucursal_origen:
            return jsonify({'status': 'error', 'message': 'Sucursal de origen no proporcionada'}), 400

        # Verificar si requiere datos de pago
        requiere_datos_pago = any(r.get('modalidadPago') == '1' for r in registros)
        tipo_comprobante = data.get('tipo_comprobante') if requiere_datos_pago else None
        metodo_pago = data.get('metodo_pago') if requiere_datos_pago else None

        if requiere_datos_pago and (tipo_comprobante is None or metodo_pago is None):
            return jsonify({
                "status": "error",
                "message": "Debe proporcionar tipo_comprobante y metodo_pago porque al menos un registro tiene modalidadPago = 1"
            }), 400

        # Preparar datos del cliente
        nombre = remitente.get('nombre_remitente', '')
        partes = nombre.split() if nombre else []

        cliente_data = {
            'correo': remitente.get('correo_remitente', ''),
            'telefono': remitente.get('num_tel_remitente', ''),
            'num_documento': remitente.get('num_doc_remitente', ''),
            'nombre_siglas': partes[0] if partes else '',
            'apellidos_razon': ' '.join(partes[1:]) if len(partes) > 1 else '',
            'tipo_documentoid': int(remitente.get('tipo_doc_remitente', 1)),
            'tipo_clienteid': 2 if remitente.get('tipo_doc_remitente') == 2 else 1
        }

        # Procesar la transacción
        nombre_empresa = controlador_empresa.get_nombre()
        num_serie, trackings = controlador_encomienda.crear_transaccion_y_paquetes(
            registros, cliente_data, tipo_comprobante, metodo_pago, sucursal_origen, modo
        )

        # Generar QR y enviar email si es exitoso
        if num_serie:
            try:
                generar_qr_paquetes(trackings)
            except Exception as qr_err:
                current_app.logger.warning(f"Error generando QR: {qr_err}")

            destinatario_email = cliente_data['correo']
            if destinatario_email:
                try:
                    msg = Message(
                        subject=f"{nombre_empresa} Envío registrado: {num_serie}",
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[destinatario_email]
                    )
                    msg.body = (
                        f"Hola {cliente_data['nombre_siglas']},\n\n"
                        f"Tu envío con número de serie {num_serie} ha sido registrado exitosamente.\n"
                        "Adjunto encontrarás los códigos QR para el seguimiento de cada paquete.\n\n"
                        f"¡Gracias por confiar en {nombre_empresa}!"
                    )

                    for tracking in trackings:
                        qr_path = os.path.join(app.static_folder, 'comprobantes', str(tracking), 'qr.png')
                        if os.path.exists(qr_path):
                            with open(qr_path, 'rb') as f:
                                qr_data = f.read()
                            msg.attach(f"qr_{tracking}.png", 'image/png', qr_data)
                        else:
                            current_app.logger.warning(f"QR no encontrado para tracking {tracking}")

                    mail.send(msg)
                except Exception as email_err:
                    current_app.logger.warning(f"Error enviando email: {email_err}")

        session.pop('datos_pago', None)
        session.pop('resumen_envios', None)
        session.pop('remitente_data', None)
        session.pop('origen_data', None)     
        session.pop('tipo_envio', None)      

        current_app.logger.info(f"Transacción creada con número de serie: {num_serie}")

        return jsonify({
            'status': 'success',
            'message': 'Envío procesado correctamente',
            'num_serie': num_serie,
            'trackings': trackings
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error en insertar_envio: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': 'Ocurrió un error al procesar el envío'
        }), 500
       
@app.route('/registrar_envios_masivos', methods=['POST'])
def registrar_envios_masivos():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'status': 'error', 'message': 'No se recibieron datos'}), 400

        tipo_comprobante = data.get('tipo_comprobante')
        registros = data.get('registros')
        # modalidad_pago_seleccionada = data.get('modalidad_pago')

        if not tipo_comprobante:
            return jsonify({'status': 'error', 'message': 'Tipo de comprobante es requerido'}), 400
        # if modalidad_pago_seleccionada is None:
        #     return jsonify({'status': 'error', 'message': 'Modalidad de pago es requerida'}), 400

        origen = data.get('origen')
        sucursal_origen = origen.get('sucursal_origen')
        
        remitente = data.get('remitente', {})
        nombre = remitente.get('nombre_remitente', '')
        partes = nombre.split() if nombre else []

        cliente_data = {
            'correo':        remitente.get('correo_remitente', ''),
            'telefono':      remitente.get('num_tel_remitente', ''),
            'num_documento': remitente.get('num_doc_remitente', ''),
            'nombre_siglas': partes[0] if partes else '',
            'apellidos_razon': ' '.join(partes[1:]) if len(partes) > 1 else '',
            'tipo_documentoid': int(remitente.get('tipo_doc_remitente', 1)),
            'tipo_clienteid': 2 if remitente.get('tipo_doc_remitente') == 2 else 1
        }


        num_serie,trackings = controlador_encomienda.crear_transaccion_y_paquetes(
            registros, cliente_data, tipo_comprobante,sucursal_origen
        )

        if num_serie:
            try:
                generar_qr_paquetes(trackings)
            except Exception as qr_err:
                current_app.logger.warning(f"Error generando QR: {qr_err}")

            # 3) Enviar correo al remitente
            # remitente_email = cliente_data['correo']
            # if remitente_email:
            #     msg = Message(
            #         subject=f"{nombre_empresa} Envío registrado: {num_serie}",
            #         sender=app.config['MAIL_USERNAME'],
            #         recipients=[remitente_email]
            #     )
            #     msg.body = (
            #         f"Hola {cliente_data['nombre_siglas']},\n\n"
            #         f"Tu envío con número de serie {num_serie} ha sido registrado exitosamente.\n"
            #         "Adjunto encontrarás los códigos QR para el seguimiento de cada paquete.\n\n"
            #         f"¡Gracias por confiar en {nombre_empresa}!"
            #     )

            #     for r in trackings:
            #         tracking = r
            #         qr_path = os.path.join(app.static_folder, 'comprobantes', str(tracking), 'qr.png')
            #         if os.path.exists(qr_path):
            #             with open(qr_path, 'rb') as f:
            #                 qr_data = f.read()
            #             msg.attach(f"qr_{tracking}.png", 'image/png', qr_data)
            #         else:
            #             current_app.logger.warning(f"QR no encontrado para tracking {tracking}")


            #     mail.send(msg)


        session.pop('datos_pago', None)
        session.pop('resumen_envios', None)
        session.pop('remitente_data', None)

        return jsonify({
            'status': 'success',
            'message': 'Envío procesado correctamente',
            'num_serie': num_serie,
            'trackings': trackings
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error en insertar_envio: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': 'Ocurrió un error al procesar el envío'
        }), 500
        
##PARA PROBAR EL API E INSERTAR 
# {
#   "tipo_comprobante": 2,
#   "origen": {
#     "sucursal_origen": 2
#   },
#   "remitente": {
#     "nombre_remitente": "Ana Torres",
#     "correo_remitente": "ana@example.com",
#     "num_tel_remitente": "987654320",
#     "num_doc_remitente": "87654321",
#     "tipo_doc_remitente": 1
#   },
#   "registros": [
#     {
#      "modo": "individual",
#       "clave": "ABC123",
#       "valorEnvio": 100.5,
#       "peso": 4.0,
#       "alto": 35.0,
#       "largo": 40.0,
#       "ancho": 25.0,
#       "tarifa": 20.0,
#       "tipoEmpaqueId": 1,
#       "tipoArticuloId": 2,
#       "tipoEntregaId": 1,
#       "estado_pago": "P",
#       "modalidadPago": "1",
#       "destino": {
#         "sucursal_destino": 5
#       },
#       "destinatario": {
#         "nombres": "Carlos",
#         "apellidos": "Ramírez",
#         "tipo_doc_destinatario": 1,
#         "num_doc_destinatario": "44556677",
#         "num_tel_destinatario": "912345678"
#       }
#     },
#     {
#       "modo": "masivo",
#       "clave": "DEF456",
#       "valorEnvio": 120.0,
#       "peso": 6.2,
#       "alto": 38.0,
#       "largo": 45.0,
#       "ancho": 28.0,
#       "tarifa": 30.0,
#       "tipoEmpaqueId": 2,
#       "tipoArticuloId": 1,
#       "tipoEntregaId": 2,
#       "estado_pago": "P",
#       "modalidadPago": "2",
#       "destino": {
#         "sucursal_destino": 7
#       },
#       "destinatario": {
#         "nombres": "María",
#         "apellidos": "Gómez",
#         "tipo_doc_destinatario": 1,
#         "num_doc_destinatario": "88990011",
#         "num_tel_destinatario": "987112233"
#       }
#     }
#   ]
# }


def generar_qr_paquetes(trackings):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(ip_address)
    for tracking in trackings:
        qr_data = f"http://192.168.100.15:8000/insertar_estado?tracking={tracking}"

        img = qrcode.make(qr_data)

        # 3) Crear carpeta del paquete
        carpeta = os.path.join(
            current_app.static_folder,
            'comprobantes',
            str(tracking)
        )
        os.makedirs(carpeta, exist_ok=True)

        # 4) Guardar imagen QR
        ruta_qr = os.path.join(carpeta, 'qr.png')
        img.save(ruta_qr)

        # 5) Guardar ruta relativa del QR en la base de datos
        qr_rel_path = f"comprobantes/{tracking}/qr.png"
        sql_execute(
            "UPDATE paquete SET qr_url = %s WHERE tracking = %s",
            (qr_rel_path, tracking)
        )


@app.route('/generar_boleta', methods=['POST'])
def generar_boleta_post():
    tracking = request.json.get('tracking')
    if not tracking:
        return "Falta el campo 'tracking'", 400
    return redirect(url_for('generar_comprobante', tracking=tracking))


@app.route('/comprobante=<int:tracking>')
def generar_comprobante(tracking):
    carpeta = os.path.join("static", "comprobantes", str(tracking))
    ruta_pdf = os.path.join(carpeta, "comprobante.pdf")

    if not os.path.exists(ruta_pdf):
        try:
            transaccion = controlador_encomienda.get_transaction_by_tracking(tracking)
            if not transaccion or not isinstance(transaccion, dict):
                return "Transacción no encontrada", 404

            empresa = controlador_empresa.getDataComprobante()
            tipo_comprobante  = transaccion['tipo_comprobante']
            comprobante_serie = transaccion['comprobante_serie']
            num_serie         = transaccion['num_serie']
            cliente           = {
                'nombre_siglas': transaccion['nombre_siglas'],
                'apellidos_razon': transaccion['apellidos_razon']
            }

            items, masivo = controlador_encomienda.obtener_items_por_num_serie(num_serie)
            resumen = controlador_encomienda.calcular_resumen_venta(transaccion['monto_total'], empresa['igv'])

            os.makedirs(carpeta, exist_ok=True)
            qr_path = url_for('static', filename=f"comprobantes/{tracking}/qr.png", _external=True)

            html = render_template("plantilla_comprobante_pago.html",
                transaccion=transaccion,
                cliente=cliente,
                empresa=empresa,
                tipo_comprobante=tipo_comprobante,
                comprobante_serie=comprobante_serie,
                items=items,
                resumen=resumen,
                qr_path=qr_path,
                masivo=masivo
            )

            ruta_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
            options = {
                'page-size': 'A6',
                'margin-top': '5mm',
                'margin-right': '5mm',
                'margin-bottom': '5mm',
                'margin-left': '5mm',
                'encoding': "UTF-8",
            }

            pdfkit.from_string(html, ruta_pdf, configuration=config, options=options)

        except Exception as e:
            return f"Error al generar PDF: {e}", 500

    return send_file(ruta_pdf, as_attachment=False)


@app.route('/rotulo=<int:tracking>')
def generar_rotulo(tracking):
    carpeta = os.path.join("static", "comprobantes", str(tracking))
    ruta_pdf = os.path.join(carpeta, "rotulo.pdf")

    if not os.path.exists(ruta_pdf):
        try:
            paquete =controlador_paquete.get_paquete_by_tracking(tracking) 
            if not paquete:
                return "Paquete no encontrado", 404

            transaccion = controlador_encomienda.get_transaction_by_tracking(tracking)
            if not transaccion:
                return "Transacción no encontrada", 404

            empresa = controlador_empresa.getDataComprobante()
            cliente = {
                'nombre_siglas': transaccion['nombre_siglas'],
                'apellidos_razon': transaccion['apellidos_razon']
            }

            contenido = controlador_paquete.get_contenido(tracking)

            os.makedirs(carpeta, exist_ok=True)
            qr_path = url_for('static', filename=f"comprobantes/{tracking}/qr.png", _external=True)

            html = render_template("plantilla_rotulo.html",
                transaccion=transaccion,
                cliente=cliente,
                empresa=empresa,
                paquete=paquete,  # Datos específicos del paquete
                contenido=contenido,
                qr_path=qr_path,
                tracking=tracking
            )

            ruta_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
            options = {
                'page-size': 'A6',
                'orientation': 'Landscape',  # Horizontal para rótulo
                'margin-top': '2mm',
                'margin-right': '2mm',
                'margin-bottom': '2mm',
                'margin-left': '2mm',
                'encoding': "UTF-8",
            }

            pdfkit.from_string(html, ruta_pdf, configuration=config, options=options)

        except Exception as e:
            return f"Error al generar PDF: {e}", 500

    return send_file(ruta_pdf, as_attachment=False)



@app.route('/envio_masivo')
def envio_masivo():
    nombre_doc = controlador_tipo_documento.get_options()
    departamento_origen = controlador_tarifa_ruta.get_departamentos_origen()
    articulos = controlador_contenido_paquete.get_options()
    empaque = controlador_tipo_empaque.get_options()
    modalidad_pago = controlador_modalidad_pago.get_options()
    peso = controlador_tipo_empaque.get_peso()
    valor_max = controlador_regla_cargo.get_max_valor()
    valores = controlador_regla_cargo.get_rango()
    porcentaje_peso = controlador_regla_cargo.get_porcentaje_peso()
    
    return render_template('envio_masivo.html', 
                           nombre_doc=nombre_doc,
                           departamento_origen = departamento_origen,
                           modalidad_pago = modalidad_pago,
                           empaque=empaque, 
                           articulos=articulos,
                           peso = peso,
                           valor_max = valor_max,
                           valores=valores,
                           porcentaje_peso=porcentaje_peso
                           )
   

@app.route('/api/recepcion', methods=["POST"])
def recepcion():
    try:
        datos = request.get_json()
        modalidad = datos.get('modalidad')
        recepcion = controlador_tipo_recepcion.get_options_dict()
        if int(modalidad) == 3:
            data = (recepcion[1],)
        else:
            data = recepcion
        res = {
            'data': data,
            'msg': "Se listó con éxito",
            'status': 1
        }

        return jsonify(res)
    except Exception as e:
         res = {
            'data': [],
            'msg': f"Ocurrió un error al listar las provincias: {repr(e)}",
            'status':-1
        }
         return jsonify(res)
    
    
@app.route('/api/provincia_origen',  methods=["POST"])
def provincia_origen():
    try:
        datos = request.get_json()
        dep = datos.get('dep')
        provincias = controlador_tarifa_ruta.get_provincia_origen(dep)
        res = {
            'data': provincias,
            'msg': "Se listó con éxito",
            'status':1
        }
        return jsonify(res)
    except Exception as e:
        res = {
            'data': [],
            'msg': f"Ocurrió un error al listar las provincias: {repr(e)}",
            'status':-1
        }
        return jsonify(res)
        
        
@app.route('/api/distrito_origen',  methods=["POST"])
def distrito_origen():
    try:
        datos = request.get_json()
        prov = datos.get('prov')
        distritos = controlador_tarifa_ruta.get_distrito_origen(prov)
        return {
            'data': distritos,
            'msg': "Se listó con éxito",
            'status':1
        }
    except Exception as e:
        return {
            'data': [],
            'msg': f"Ocurrió un error al listar las distritos: {repr(e)}",
            'status':-1
        }
    

@app.route('/api/sucursal_origen',  methods=["POST"])
def sucursal_origen():
    try:
        datos = request.get_json()
        dep = datos.get('dep')
        prov = datos.get('prov')
        dist = datos.get('dist')
        
        ubigeo = controlador_tarifa_ruta.get_codigo_ubigeo(dep,prov,dist)
        sucursales = controlador_tarifa_ruta.get_sucursal_origen(ubigeo['codigo'])
        return {
            'data': sucursales,
            'msg': "Se listó con éxito",
            'status':1
        }
    except Exception as e:
        return {
            'data': [],
            'msg': f"Ocurrió un error al listar las sucursales: {repr(e)}",
            'status':-1
        }
    

@app.route('/api/departamento_destino',  methods=["POST"])
def departamento_destino():
    try:
        datos = request.get_json()
        id_suc_origen = datos.get('suc_origen')
        
        departamentos = controlador_tarifa_ruta.get_departamento_destino(id_suc_origen)
        
        return {
            'data': departamentos,
            'msg': "Se listó con éxito",
            'status':1
        }
    except Exception as e:
        return {
            'data': [],
            'msg': f"Ocurrió un error al listar las departamentos: {repr(e)}",
            'status':-1
        }
    

@app.route('/api/provincia_destino',  methods=["POST"])
def provincia_destino():
    try:
        datos = request.get_json()
        codigo = datos.get('codigo')
        dep = datos.get('dep')
        
        
        provincias = controlador_tarifa_ruta.get_provincia_destino(dep,codigo)
        
        return {
            'data': provincias,
            'msg': "Se listó con éxito",
            'status':1
        }
    except Exception as e:
        return {
            'data': [],
            'msg': f"Ocurrió un error al listar las provincias: {repr(e)}",
            'status':-1
        }
        
        
@app.route('/api/distrito_destino',  methods=["POST"])
def distrito_destino():
    try:
        datos = request.get_json()
        codigo = datos.get('codigo')
        prov = datos.get('prov')
        
        
        distritos = controlador_tarifa_ruta.get_distrito_destino(prov,codigo)
        
        res = {
            'data': distritos,
            'msg': "Se listó con éxito",
            'status':1
        }
        return jsonify(res)
    except Exception as e:
        res  = {
            'data': [],
            'msg': f"Ocurrió un error al listar las distritos: {repr(e)}",
            'status':-1
        }
        return jsonify(res)
    

@app.route('/api/sucursal_destino',  methods=["POST"])
def sucursal_destino():
    try:
        datos = request.get_json()
        dep = datos.get('dep')
        prov = datos.get('prov')
        dist = datos.get('dist')
        origen = datos.get('cod_origen')
        
        codigo_destino = controlador_tarifa_ruta.get_codigo_ubigeo(dep,prov,dist)
        sucursales = controlador_tarifa_ruta.get_sucursal_destino(origen,codigo_destino['codigo'])
        return {
            'data': sucursales,
            'msg': "Se listó con éxito",
            'status':1
        }
    except Exception as e:
        return {
            'data': [],
            'msg': f"Ocurrió un error al listar las departamentos: {repr(e)}",
            'status':-1
        }
        
        
@app.route('/api/id_sucursal',  methods=["POST"])
def id_sucursal():
    try:
        datos = request.get_json()
        dep = datos.get('dep')
        prov = datos.get('prov')
        dist = datos.get('dist')
        origen = datos.get('cod_origen')
        
        codigo_destino = controlador_tarifa_ruta.get_codigo_ubigeo(dep,prov,dist)
        
        sucursales = controlador_tarifa_ruta.get_sucursal_destino(origen,codigo_destino['codigo'])
        
        return {
            'data': sucursales,
            'msg': "Se listó con éxito",
            'status':1
        }
    except Exception as e:
        return {
            'data': [],
            'msg': f"Ocurrió un error al listar las departamentos: {repr(e)}",
            'status':-1
        }
        

def generar_boleta(datos: dict, qr_png: BytesIO) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    ancho, alto = A4
    num_serie = str(uuid.uuid4())[:8]

    # 1. Cabecera
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, alto-20*mm, "New Olva S.A.C.")
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, alto-25*mm, "RUC 20512528458  |  AV. MEXICO NRO. 1187, LIMA")
    c.drawString(20*mm, alto-30*mm, f"BOLETA DE VENTA ELECTRÓNICA    Nº {num_serie}-{datos['numero']}")

    # 2. Datos del adquiriente
    y = alto-40*mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, y, "ADQUIRIENTE")
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, y-5*mm, f"DNI: {datos['cliente']['dni']}")
    c.drawString(60*mm, y-5*mm, datos['cliente']['nombre'])

    # 3. Detalle de la venta (tabla muy básica)
    y -= 15*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, y, "Cant.")
    c.drawString(35*mm, y, "Descripción")
    c.drawString(120*mm, y, "P/U")
    c.drawString(150*mm, y, "Total")
    c.setFont("Helvetica", 10)
    for i, item in enumerate(datos['items'], start=1):
        y -= 6*mm
        c.drawString(20*mm, y, str(item['cantidad']))
        c.drawString(35*mm, y, item['descripcion'])
        c.drawRightString(135*mm, y, f"{item['pu']:.2f}")
        c.drawRightString(175*mm, y, f"{item['total']:.2f}")

    # 4. Totales
    y -= 12*mm
    c.drawRightString(150*mm, y, "GRAVADA S/")
    c.drawRightString(175*mm, y, f"{datos['gravada']:.2f}")
    y -= 6*mm
    c.drawRightString(150*mm, y, "IGV S/")
    c.drawRightString(175*mm, y, f"{datos['igv']:.2f}")
    y -= 6*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(150*mm, y, "TOTAL S/")
    c.drawRightString(175*mm, y, f"{datos['total']:.2f}")

    # 5. Insertar el QR en la esquina inferior derecha
    qr_x = ancho - 50*mm
    qr_y = 20*mm
    c.drawImage(qr_png, qr_x, qr_y, width=30*mm, height=30*mm)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def generar_qr_boleta(datos):
    info_qr = f"{datos['serie']}-{datos['numero']}|{datos['total']}"
    img = qrcode.make(info_qr)
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output



# @app.route('/boleta/<int:numero>')
# def ver_boleta(serie, numero):
#     datos = obtener_datos_de_boleta(numero)  # tu lógica propia
#     qr_png = generar_qr_boleta(datos)  # genera el QR y devuélvelo como BytesIO

#     pdf_file = generar_boleta(datos, qr_png)
    
#     return send_file(
#         pdf_file,
#         as_attachment=False,  # True para forzar descarga
#         download_name=f"boleta_{serie}-{numero}.pdf",
#         mimetype='application/pdf'
#     )


# @app.route('/generar_comprobante', methods=['POST'])
# def generar_comprobante():
#     data = request.get_json()
#     # session['resumen_envios'] = data  # opcional, si deseas persistirlo

#     tipo_doc = int(data['remitente']['tipo_doc_remitente'])
#     nro_doc = data['remitente']['num_doc_remitente']
#     correo = data['remitente']['correo']
#     telefono = data['remitente']['num_tel_remitente']
#     nombre_siglas = data['remitente']['nombre_remitente']

#     cliente = controlador_cliente.get_cliente_tipo_nro_documento(tipo_doc , nro_doc)
#     if not cliente:
#         cliente_id = controlador_cliente.register_client(correo, telefono, nro_doc, nombre_siglas, '', tipo_doc, 1 )
#     else:
#         cliente_id = cliente['id']

#     num_serie = str(uuid.uuid4())[:8]  # o tu lógica de serie/numero
#     # monto_total = sum(Decimal(str(r['tarifa'])) for r in data['envios'])
#     now = datetime.now()
#     sql = """
#       INSERT INTO transaccion_encomienda
#        (num_serie, masivo, descripcion, recojo_casa,
#         id_sucursal_origen, estado_pago, fecha, hora,
#         direccion_recojo, clienteid, tipo_comprobanteid)
#       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     params = (
#       num_serie,
#       1,  # masivo
#       'Envíos masivos',
#       1 if data['modalidad_pago']=='1' else 0,
#       data['envios'][0]['origen']['sucursal_origen'],
#       'P',  # pendiente
#       now.date(), 
#       now.time(),
#       None,  # direccion_recojo si aplica
#       cliente_id,
#       int(data['tipo_comprobante'])
#     )
#     sql_execute(sql, params)


#     for envio in data['envios']:
#         # token = str(uuid.uuid4())
#         # qr_png = make_qr(url_for('seguimiento', token=token, _external=True))
#         # opcional: guarda qr_png en disco o en BLOB
#         sql = """
#         INSERT INTO paquete
#             (tracking, clave, valor, peso, alto, largo, precio_ruta, ancho,
#             descripcion, direccion_destinatario, telefono_destinatario,
#             num_documento_destinatario, sucursal_destino_id,
#             tipo_documento_destinatario_id, tipo_empaqueid,
#             contenido_paqueteid, tipo_recepcionid, salidaid,
#             transaccion_encomienda_num_serie, qr_token, qr_image)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s, %s, %s, %s,
#                 %s, %s, %s, %s, %s)
#         """
#         params = (
#             None,  # si es AUTO_INCREMENT
#             envio['clave'],
#             envio['valorEnvio'],
#             envio['peso'],
#             envio['alto'], envio['largo'],
#             envio['tarifa'], envio['ancho'],
#             envio.get('descripcion',''),
#             envio.get('destino_text',''),
#             envio.get('telefono_destinatario',''),
#             envio['destino']['num_doc_destinatario'],
#             envio['destino']['sucursal_destino'],
#             envio['tipo_doc_destinatario'],
#             envio['tipo_empaqueid'],
#             envio.get('contenido_paqueteid'),
#             envio.get('tipo_recepcionid'),
#             None,  # salidaid
#             num_serie,
#             None , # token,
#             None
#             # qr_png.read()  # o la ruta si la guardas en FS
#         )
#         sql_execute(sql, params)







@app.route("/perfil")
def perfil():
    return render_template('perfil.html')


##################_ METHOD POST GENERALES _################## 

@app.route("/procesar_login", methods=["POST"])
def procesar_login():
    try:
        correo = request.form["email"]
        contrasenia = request.form["password"]
        resp = resp_login( correo , contrasenia )
        return resp
    except Exception as e:
        return rdrct_error(redirect_url('login')  , e)


@app.route("/login_android", methods=["POST"])
def login_android():
    try:
        data = request.get_json()
        correo = data.get("correo")
        contrasenia = data.get("contrasenia")
        usuario = controlador_usuario.get_usuario_por_correo(correo)
        encpassword = encrypt_sha256_string(contrasenia)
        if usuario and encpassword == usuario['contrasenia']:
            data = {
                'message': 200
            }
            return jsonify(data)
    except Exception as e:
        return jsonify(e)
    
@app.route('/salidas_android', methods=['POST'])
def salidas_android():
    try:
        data = request.get_json()
        correo = data.get('correo')

        if not correo:
            return jsonify({'error': 'El campo "correo" es requerido'}), 400

        datos = controlador_sucursal.get_data_exit(correo)

        if not datos:
            return jsonify({'error': 'No se encontró información para el correo proporcionado'}), 404

        fecha_str = datos['fecha'].strftime('%Y-%m-%d') if hasattr(datos['fecha'], 'strftime') else str(datos['fecha'])

        if isinstance(datos['hora'], timedelta):
            total_seconds = int(datos['hora'].total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            hora_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            hora_str = str(datos['hora'])

        res = {
            'id': datos['id'],
            'fecha': fecha_str,
            'hora': hora_str,
            'estado': datos['estado'],
            'latitud_origen': float(datos['latitud_origen']),
            'longitud_origen': float(datos['longitud_origen']),
            'latitud_destino': float(datos['latitud_destino']),
            'longitud_destino': float(datos['longitud_destino'])
        }

        return jsonify(res), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/obtener_coordenadas', methods=['POST'])
def obtener_coordenadas():
    try:
        data = request.get_json()

        id_salida = data['salida']

        coordenadas = controlador_sucursal.get_coordenadas_actual(id_salida)
        print('coordenas:',coordenadas)

        if not coordenadas:
            return jsonify({'error': 'No se encontraron coordenadas'}), 404

        res = {
            'id':id_salida,
            'latitud_origen': coordenadas['latitud_origen'],
            'longitud_origen': coordenadas['longitud_origen'],
            'latitud_destino': coordenadas['latitud_destino'],
            'longitud_destino': coordenadas['longitud_destino'],
            "status":1
        }
        return jsonify(res)

    except Exception as e:
        print("ERROR EN BACKEND:", repr(e))
        return jsonify({'error': str(e),
                        "status":-1}), 500

@app.route('/cambiar_estado_salida', methods=['POST'])
def cambiar_estado_salida():
    try:
        data = request.get_json()
        if not data or 'id' not in data:
            return jsonify({'success': False, 'message': 'Falta el campo "id" en el cuerpo JSON'}), 400

        id_salida = data.get('id')
        resultado = controlador_salida.change_state_exit(id_salida)
        return jsonify(resultado)

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error del servidor: {str(e)}'}), 500




@app.route('/seguimiento_unidad_prueba')
def seguimiento_unidad_prueba():
    lat1 = request.args.get('lat1')
    lon1 = request.args.get('lon1')
    lat2 = request.args.get('lat2')
    lon2 = request.args.get('lon2')
    id = request.args.get('id')
    
    data = [{
        
        'iniciolat_via': lat1,
        'iniciolon_via': lon1,
        'finlat_via': lat2,
        'finlon_via': lon2,
        'id':id
    }]
    info = controlador_salida.get_data_by_id_salida(id)
    print(info)
    return render_template('seguimiento_empleado.html', data=data,info=info)



@app.route("/procesar_register", methods=["POST"])
def procesar_register():
    try:
        firma = inspect.signature(resp_register)

        valores = []
        for nombre, parametro in firma.parameters.items():
            valor = request.form.get(nombre)
            valores.append(valor)

        return resp_register( *valores )

    except Exception as e:
        return rdrct_error(redirect_url('login')  , e)

####################3 RECUPERAR CONTRASENIA #########
@app.route("/procesar_recuperacion", methods=["POST"])
def procesar_recuperacion():
    try:
        email = request.form.get("email")
        if not email:
            return rdrct_error(redirect_url('recuperar_contrasenia'), 'Correo requerido')

        usuario = controlador_usuario.get_usuario_por_correo(email)
        if not usuario:
            return rdrct_error(redirect_url('recuperar_contrasenia'), 'Correo no registrado')

        serializer = URLSafeSerializer(app.secret_key)
        token = serializer.dumps(email)
        enlace = url_for('cambiar_contrasenia', token=token, _external=True)

        # Contenido HTML bonito
        html_body = f"""
            <html>
            <body style="margin:0;padding:0;background-color:#f4f4f4;font-family:Arial,sans-serif;">
                <div style="max-width:600px;margin:30px auto;background-color:#ffffff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);padding:40px;">
                <h2 style="color:#333333;text-align:center;">Recuperación de Contraseña</h2>
                <p style="font-size:16px;line-height:1.6;color:#555;">
                    Hola <strong>{usuario['correo']}</strong>,
                </p>
                <p style="font-size:16px;line-height:1.6;color:#555;">
                    Recibimos una solicitud para restablecer tu contraseña. Para continuar, haz clic en el botón de abajo:
                </p>
                <div style="text-align:center;margin:30px 0;">
                    <a href="{enlace}" style="background-color:#007BFF;color:white;padding:14px 28px;text-decoration:none;border-radius:6px;display:inline-block;font-weight:bold;">
                    Restablecer contraseña
                    </a>
                </div>
                <p style="font-size:15px;color:#666;">
                    Si el botón no funciona, copia y pega el siguiente enlace en tu navegador:
                </p>
                <p style="font-size:14px;word-break:break-all;color:#007BFF;">
                    <a href="{enlace}" style="color:#007BFF;text-decoration:none;">{enlace}</a>
                </p>
                <hr style="margin:30px 0;border:none;border-top:1px solid #eee;">
                <p style="font-size:13px;color:#999;text-align:center;">
                    Si tú no realizaste esta solicitud, puedes ignorar este mensaje. Tu contraseña permanecerá segura.
                </p>
                <p style="font-size:13px;color:#999;text-align:center;margin-top:10px;">
                    — El equipo de <strong>{controlador_empresa.get_nombre()}</strong>
                </p>
                </div>
            </body>
            </html>
            """

        msg = Message(subject="Recupera tu contraseña",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email],
                      html=html_body)

        mail.send(msg)

        return redirect_url('login')

    except Exception as e:
        return rdrct_error(redirect_url('recuperar_contrasenia'), e)

@app.route('/cambiar_contrasenia')
def cambiar_contrasenia():
    token = request.args.get('token')
    user_id = request.cookies.get('user_id')

    correo_recuperado = None
    is_recuperando = False

    if token:
        try:
            serializer = URLSafeSerializer(app.secret_key)
            correo_recuperado = serializer.loads(token)
            is_recuperando = True
        except Exception:
            return rdrct_error(redirect_url('login'), 'Token inválido')

    elif user_id:
        is_recuperando = False
    else:
        return redirect_url('login')

    return render_template(
        'cambiar_contrasenia.html',
        token=correo_recuperado,
        is_recuperando=is_recuperando
    )


@app.route("/procesar_cambio_contrasenia", methods=["POST"])
def procesar_cambio_contrasenia():
    try:
        nueva = request.form.get("nueva_contrasena")
        confirmar = request.form.get("confirmar_contrasena")
        actual = request.form.get("contrasena_actual")
        correo = request.cookies.get("correo")

        # Intentar recuperar correo desde form si está visible
        if not correo:
            correo = request.form.get("correo")

        # Token (recuperación por URL)
        token = request.args.get("token")
        if not correo and token:
            try:
                serializer = URLSafeSerializer(app.secret_key)
                correo = serializer.loads(token)
            except Exception:
                return rdrct_error(redirect_url('cambiar_contrasenia'), 'Token inválido')

        if not nueva or not confirmar or not correo:
            return rdrct_error(redirect_url('cambiar_contrasenia'), 'Datos incompletos')

        if nueva != confirmar:
            return rdrct_error(redirect_url('cambiar_contrasenia'), 'Las nuevas contraseñas no coinciden')

        usuario = controlador_usuario.get_usuario_por_correo(correo)
        if not usuario:
            return rdrct_error(redirect_url('login'), 'Usuario no encontrado')

        # Solo se valida contraseña actual si hay sesión iniciada
        if request.cookies.get("user_id"):
            if not actual:
                return rdrct_error(redirect_url('cambiar_contrasenia'), 'Falta contraseña actual')

            actual_hash = encrypt_sha256_string(actual)
            if usuario['contrasenia'] != actual_hash:
                return rdrct_error(redirect_url('cambiar_contrasenia'), 'Contraseña actual incorrecta')

        # Cambiar contraseña
        nueva_hash = encrypt_sha256_string(nueva)
        controlador_usuario.actualizar_contrasenia(usuario['id'], nueva_hash)

        # Enviar correo de notificación
        empresa = controlador_empresa.get_nombre()
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px;">
            <div style="max-width: 600px; background-color: white; padding: 25px; border-radius: 8px; margin: auto;">
                <h2 style="color: #333;">Contraseña actualizada</h2>
                <p>Hola <strong>{usuario['correo']}</strong>,</p>
                <p>Te informamos que tu contraseña fue modificada correctamente.</p>
                <p>Si tú no realizaste este cambio, por favor contacta de inmediato con el soporte técnico de <strong>{empresa}</strong>.</p>
                <p style="font-size: 0.9em; color: #888;">Este es un mensaje automático, no respondas directamente a este correo.</p>
                <p style="margin-top: 20px;">— El equipo de <strong>{empresa}</strong></p>
            </div>
        </body>
        </html>
        """
        msg = Message(
            subject="Tu contraseña fue actualizada",
            sender=app.config['MAIL_USERNAME'],
            recipients=[correo],
            html=html
        )
        mail.send(msg)

        # Cierre de sesión
        resp = make_response(redirect_url('login'))
        resp.set_cookie('correo', '', max_age=0)
        resp.set_cookie('user_id', '', max_age=0)
        return resp

    except Exception as e:
        return rdrct_error(redirect_url('cambiar_contrasenia'), e)

######################

##################_ PAGINAS EMPLEADO _################## 


PAGINAS_SIMPLES_ADMIN = [ 
    # 'panel' , 
    'programacion_devolucion',
]

registrar_paginas_con_decorador(app, PAGINAS_SIMPLES_ADMIN, validar_empleado)


@app.route("/panel")
@validar_empleado()
def panel():
    return render_template('panel.html')


@app.route("/modulo=<module_name>")
@validar_empleado()
def modulo(module_name):
    modulo = permiso.get_modulo_key(module_name)
    # usuario = controlador_usuario.get_usuario_empleado_user_id(request.cookies.get('user_id'))

    if modulo['activo'] == 1 :
        tipos_pag = permiso.get_tipos_pagina_moduloid(modulo['id'])
        return render_template(
            'MODULO.html' , 
            module_name = module_name , 
            modulo = modulo ,
            REPORTES = REPORTES ,
            tipos_pag = tipos_pag ,
            )
    return None


@app.route("/crud=<tabla>")
@validar_empleado()
def crud_generico(tabla):
    config = CONTROLADORES.get(tabla)
    page = permiso.get_pagina_key(tabla)
    user_info = getDatosUsuario()
    permisos = permiso.consult_permiso_rol(page['id'] , user_info['rolid'])

    if config and page:
        active = config["active"] and (page['activo'] == 1 )
        tipo_paginaid = page['tipo_paginaid']
        no_crud = config.get('no_crud')
        # print(active , ' - ',tipo_paginaid ,' - ', no_crud)

        if active is True and tipo_paginaid == 1 and (no_crud is None or no_crud is False):
            icon_page_crud = get_icon_page(page.get("icono"))
            titulo = f'{NOMBRE_CRUD_PAGE} {page["titulo"].lower() }' 

            nombre_tabla = config["nombre_tabla"]
            filters = config["filters"]
            fields_form = config["fields_form"]
            controlador = config["controlador"]

            existe_activo = controlador.exists_Activo()
            columnas , filas = controlador.get_table()
            primary_key = controlador.get_primary_key()
            table_columns  = list(filas[0].keys()) if filas else []
            
            CRUD_FORMS = config["crud_forms"]
            crud_search = CRUD_FORMS.get("crud_search")     and permisos['search']                       
            crud_consult = CRUD_FORMS.get("crud_consult")   and permisos['consult']                      
            crud_insert = CRUD_FORMS.get("crud_insert")     and permisos['insert']                       
            crud_update = CRUD_FORMS.get("crud_update")     and permisos['update']                       
            crud_delete = CRUD_FORMS.get("crud_delete")     and permisos['delete']                       
            crud_unactive = CRUD_FORMS.get("crud_unactive") and permisos['unactive'] and existe_activo 

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
                columnas       = columnas ,
                key_columns    = list(columnas.keys()) ,
                table_columns  = table_columns ,
                # crud_list      = crud_list,
                crud_search    = crud_search,
                crud_consult   = crud_consult,
                crud_insert    = crud_insert,
                crud_update    = crud_update,
                crud_delete    = crud_delete,
                crud_unactive  = crud_unactive,
            )



@app.route("/transaccion=<tabla>",defaults={'pk_foreign': None})
@app.route("/transaccion=<tabla>/<pk_foreign>")
# @validar_empleado()
def transaccion(tabla , pk_foreign):
    config = TRANSACCIONES.get(tabla)
    page = permiso.get_pagina_key(tabla)
    user_info = getDatosUsuario()
    permisos = permiso.consult_permiso_rol(page['id'] , user_info['rolid'])

    if config and page:
        active = config["active"] and (page['activo'] == 1 )
        tipo_paginaid = page['tipo_paginaid']
        no_crud = config.get('no_crud')

        if active is True and tipo_paginaid == 3 and (no_crud is None or no_crud is False):
            icon_page_crud = get_icon_page(page.get("icono"))
            titulo = f'{page["titulo"]}'

            nombre_tabla = config["nombre_tabla"]
            filters = config["filters"]
            fields_form = config["fields_form"]
            controlador = config["controlador"]
            lst_buttons = config['buttons']
            lst_options = config['options']

            existe_activo = controlador.exists_Activo()
            if pk_foreign is not None:
                columnas , filas = controlador.get_table_pk_foreign(pk_foreign = pk_foreign)
            else:
                columnas , filas = controlador.get_table()
            primary_key = controlador.get_primary_key()
            table_columns  = list(filas[0].keys()) if filas else []
            
            CRUD_FORMS = config["crud_forms"]
            crud_search = CRUD_FORMS.get("crud_search") and (permisos['search']                          )
            crud_consult = CRUD_FORMS.get("crud_consult") and (permisos['consult']                       )
            crud_insert = CRUD_FORMS.get("crud_insert") and   (permisos['insert']                        )
            crud_update = CRUD_FORMS.get("crud_update") and   (permisos['update']                        )
            crud_delete = CRUD_FORMS.get("crud_delete") and   (permisos['delete']                        )
            crud_unactive = CRUD_FORMS.get("crud_unactive") and existe_activo and ( permisos['unactive'] )
            
            buttons = []
            options = []

            import json

            
            for btn in lst_buttons:
                permiso_otro_button = json.loads(permisos.get('otro')) if permisos.get('otro') is not None else {}
                if permiso_otro_button and permiso_otro_button.get(btn[6]) and permiso_otro_button.get(btn[6]) == 1:
                    buttons.append(btn)
                elif permisos.get(btn[6]) == 1:
                    buttons.append(btn)

            for btn in lst_options:
                permiso_otro_option = json.loads(permisos.get('otro')) if permisos.get('otro') is not None else {}
                if permiso_otro_option and permiso_otro_option.get(btn[6]) and permiso_otro_option.get(btn[6]) == 1:
                    options.append(btn)
                elif permisos.get(btn[6]) == 1:
                    options.append(btn)

            return render_template(
                "TRANSACCION.html" ,
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
                crud_search    = crud_search,
                crud_consult   = crud_consult,
                crud_insert    = crud_insert,
                crud_update    = crud_update,
                crud_delete    = crud_delete,
                crud_unactive  = crud_unactive,
                esTransaccion = True ,
                buttons = buttons ,
                options = options ,
                pk_foreign = pk_foreign if pk_foreign else None
            )

    
@app.route("/reporte=<report_name>")
@validar_empleado()
def reporte(report_name):
    config = REPORTES.get(report_name)
    page = permiso.get_pagina_key(report_name)

    if config and page:
        active = config["active"]
        tipo_paginaid = page['tipo_paginaid']

        if active is True and tipo_paginaid == 4 :
            icon_page_crud = get_icon_page(page.get("icono"))
            titulo = page["titulo"]

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
                primary_key    = None ,
                crud_search    = True,
                esReporte      = True ,
            )


@app.route("/administrar_paginas")
@validar_empleado()
def administrar_paginas():
    modulos = permiso.get_lista_modulos()
    paginas = permiso.get_todos_paginas()
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
    paginas = permiso.get_paginas_todos_permiso_rol(rolid)
    roles = permiso.get_lista_roles()
    tipos_rol = permiso.get_lista_tipo_roles()
    cants_mod = permiso.get_cants_modulos()

    info_rol = permiso.get_info_rol(rolid)

    # Enriquecer cada página con sus datos de CRUD y existencia de campo activo
    for pagina in paginas:
        key = pagina.get("key")
        tipo = pagina.get("tipo_paginaid")
        
        page_dict = None
        if tipo == 1:
            page_dict = CONTROLADORES
        elif tipo == 3:
            page_dict = TRANSACCIONES
        elif tipo == 4:
            page_dict = REPORTES

        config = page_dict.get(key) if page_dict else None

        if config:
            pagina["tiene_crud"] = config.get("crud_forms", {})
            pagina["existe_activo"] = False

            controlador = config.get("controlador")
            if controlador and hasattr(controlador, "exists_Activo"):
                try:
                    pagina["existe_activo"] = controlador.exists_Activo()
                except Exception as e:
                    print(f"[!] Error en exists_Activo de {key}: {e}")

        if pagina['otro']:
            import json
            datos_json = json.loads(pagina['otro'])
            pagina['otro'] = datos_json

    return render_template(
        'administrar_paginas.html',
        modulos=modulos,
        paginas=paginas,
        roles=roles,
        tipos_rol=tipos_rol,
        rolid=rolid,
        info_rol=info_rol,
        cants_mod=cants_mod,
        CONTROLADORES=CONTROLADORES,
        TRANSACCIONES=TRANSACCIONES,
        REPORTES=REPORTES,
        cur_modulo_id=permiso.get_pagina_key('administrar_paginas')['moduloid'],
    )


@app.route("/informacion_empresa")
@validar_empleado()
def informacion_empresa():
    emp_id = request.args.get("emp_id")
    sucursales = controlador_sucursal.get_options_sucursales()
    lst_empresas = controlador_empresa.get_rows()

    if emp_id:
        information = controlador_empresa.get_data_id(emp_id)
    else:
        information = controlador_empresa.get_data()
    
    return render_template(
        'informacion_empresa.html' ,
        information = information ,
        sucursales = sucursales,
        lst_empresas = lst_empresas ,
        )



##################_ PAGINAS EMPLEADO METHOD POST _################## 

@app.route("/insert_row=<tabla>", methods=["POST"])
@validar_empleado()
@validar_error_crud()
def crud_insert(tabla):
    # try:
        if tabla in CONTROLADORES.keys():    
            config = CONTROLADORES.get(tabla)
            url_redirect = 'crud_generico'
        elif tabla in TRANSACCIONES.keys():    
            config = TRANSACCIONES.get(tabla)
            url_redirect = 'transaccion'

        if not config:
            return "Tabla no soportada", 404

        active = config["active"]
        no_crud = config.get('no_crud')
        # transaccion = config.get('transaccion')

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
            return redirect(url_for(url_redirect , tabla = tabla))
    # except Exception as e:
    #     return f"No se aceptan carácteres especiales", 400


@app.route("/update_row=<tabla>", methods=["POST"])
@validar_empleado()
# @validar_error_crud()
def crud_update(tabla):
    # try:
        if tabla in CONTROLADORES.keys():    
            config = CONTROLADORES.get(tabla)
            url_redirect = 'crud_generico'
        elif tabla in TRANSACCIONES.keys():    
            config = TRANSACCIONES.get(tabla)
            url_redirect = 'transaccion'

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
                if archivo.filename != "":
                    nuevo_nombre = guardar_imagen_bd(tabla,'' ,archivo)
                    valores.append(nuevo_nombre)
                else:
                    # Si no se selecciona una nueva imagen, mantener la actual
                    valores.append(request.form.get(f"{nombre}_actual"))
            else:
                valor = request.form.get(nombre)
                if valor == '':
                    valor = None
                valores.append(valor)

        controlador.update_row( *valores )

        if no_crud :
            return redirect(url_for(str(no_crud)))
        else:
            return redirect(url_for(url_redirect, tabla = tabla))
    # except Exception as e:
    #     return f"No se aceptan carácteres especiales", 400


@app.route("/delete_row=<tabla>", methods=["POST"])
@validar_empleado()
@validar_error_crud()
def crud_delete(tabla):
    if tabla in CONTROLADORES.keys():    
        config = CONTROLADORES.get(tabla)
        url_redirect = 'crud_generico'
    elif tabla in TRANSACCIONES.keys():    
        config = TRANSACCIONES.get(tabla)
        url_redirect = 'transaccion'

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
        return redirect(url_for(url_redirect, tabla = tabla))


@app.route("/unactive_row=<tabla>", methods=["POST"])
@validar_empleado()
@validar_error_crud()
def crud_unactive(tabla):
    if tabla in CONTROLADORES.keys():    
        config = CONTROLADORES.get(tabla)
        url_redirect = 'crud_generico'
    elif tabla in TRANSACCIONES.keys():    
        config = TRANSACCIONES.get(tabla)
        url_redirect = 'transaccion'

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
        return redirect(url_for(url_redirect, tabla = tabla))


@app.route("/update_empresa", methods=["POST"])
@validar_empleado()
@validar_error_crud()
def update_empresa():
    controlador = controlador_empresa
    funcion = controlador.insert_row
    firma = inspect.signature(funcion)

    valores = []
    for nombre, parametro in firma.parameters.items():
        if nombre in request.files:
            archivo = request.files[nombre]
            if archivo.filename != "":
                ahora = datetime.now()
                formateado = ahora.strftime("%Y%m%d%H%M%S")
                nuevo_nombre = guardar_imagen_bd('empresa' ,f'{formateado}_',archivo)
                valores.append(nuevo_nombre)
            else:
                valores.append(request.form.get(f"{nombre}_actual"))
        else:
            valor = request.form.get(nombre)
            valores.append(valor)

    empresa_id = funcion(*valores)
    controlador_empresa.dar_actual_empresa_id(empresa_id)
    return redirect(url_for('informacion_empresa'))



@app.route("/update_admin_pag=<tabla>", methods=["POST"])
@validar_empleado()
def update_admin_pag(tabla):
        if tabla == 'modulo':
            controlador = controlador_modulo
        elif tabla == 'pagina':
            controlador = controlador_pagina

        firma = inspect.signature(controlador.update_row)

        valores = []
        for nombre, parametro in firma.parameters.items():
            if nombre in request.files:
                archivo = request.files[nombre]
                if archivo.filename != "":
                    nuevo_nombre = guardar_imagen_bd(tabla,'' ,archivo)
                    valores.append(nuevo_nombre)
                else:
                    # Si no se selecciona una nueva imagen, mantener la actual
                    valores.append(request.form.get(f"{nombre}_actual"))
            else:
                valor = request.form.get(nombre)
                if valor == '':
                    valor = None
                valores.append(valor)

        controlador.update_row( *valores )

        return redirect(url_for('administrar_paginas'))



@app.route("/op_crud_empresa=<op>", methods=["POST"])
@validar_empleado()
@validar_error_crud()
def op_crud_empresa(op):
    primary_key = 'id'
    if op == 'delete':
        controlador_empresa.delete_row(request.form.get(primary_key))
    elif op == 'actual':
        controlador_empresa.dar_actual_empresa_id(request.form.get(primary_key))
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
        if column in ['insert' , 'update' , 'delete' , 'unactive' , 'search' , 'acceso' , 'consult']:
            rpta_column = permiso.consult_permiso_rol(paginaid , rolid)[column]
        else:
            import json
            permiso_otro = permiso.consult_permiso_rol(paginaid , rolid)['otro']
            dict_otro = json.loads(permiso_otro)
            rpta_column = dict_otro.get(column)


        return jsonify({'success': True , 'rpta' : rpta_column})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@app.route('/actualizar_permiso_modulo', methods=['POST'])
def actualizar_permiso_modulo():
    data = request.get_json()

    moduloid = data.get('moduloid')
    column = data.get('column')
    rolid = data.get('rolid')
    value = data.get('value')

    try:
        permiso.change_permiso_modulo(column , moduloid , rolid , value)
        rpta_list = permiso.get_modulo_permiso_rol(rolid , moduloid)
        return jsonify({'success': True , 'rpta': rpta_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@app.route("/api/seguimiento/<placa>", methods=["GET"])
def api_seguimiento_vehiculo(placa):
    try:
        data = controlador_salida.get_salida_pendiente_placa(placa.upper())

        if not data:
            return jsonify({"error": "No hay salida activa para esta placa."}), 404

        return jsonify(data[0])  # asumiendo solo una salida activa por placa
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/seguimiento_empleado_prueba=<placa>")
@validar_empleado()
def seguimiento_empleado_prueba(placa):
    data = controlador_salida.get_info_salida_pendiente_placa(placa.upper())
    return render_template(
        'seguimiento_empleado_prueba.html', 
        placa = placa ,
        data = data ,
        cur_modulo_id = permiso.get_pagina_key('salida')['moduloid'] ,
        )


@socketio.on("ubicacion_movil")
def recibir_ubicacion(data):
    emit("ubicacion_actualizada", data, broadcast=True)


@app.route("/simulador_envio_ubicacion")
def simulador_envio_ubicacion():
    return render_template(
        'simulador_envio_ubicacion.html', 
        )
    
@app.route("/buscar_paquete", methods=['POST'])
def buscar_paquete():
    tracking = request.form.get('tracking')
    anio = request.form.get('anio')
    paquete = controlador_paquete.buscar_paquete(tracking, anio)
    print(paquete)
    if paquete is not None:
        return redirect(url_for('seguimiento_tracking', tracking=paquete))
    else:
        return redirect(url_for('seguimiento_tracking', tracking=0))


   
@app.route('/seguimiento')
def seguimiento():
    try:
        estado = controlador_estado_encomienda.get_options()
        return render_template('seguimiento.html',estado=estado)
    except Exception as e:
        return e   
 
    
@app.route("/seguimiento=<tracking>")
def seguimiento_tracking(tracking):
    estados = controlador_estado_encomienda.get_states()
    ultimo_estado = controlador_estado_encomienda.get_last_states(tracking)
    estados_actuales = controlador_estado_encomienda.get_estados_insertados(tracking)
    comprobantes = controlador_estado_encomienda.get_comprobantes(tracking)
    datos = controlador_estado_encomienda.get_data_package(tracking)
    estados_usados = [e['estado_encomiendaid'] for e in estados_actuales]
    detalles_estado = controlador_estado_encomienda.get_detalles_estado_by_tracking(tracking)
    
    detalles_por_estado = defaultdict(list)
    for det in detalles_estado:
        detalles_por_estado[det['estado_encomiendaid']].append(det)
    
    return render_template('seguimiento.html',
                           estados=estados,
                           ultimo_estado=ultimo_estado,
                           comprobantes=comprobantes,
                           datos=datos,
                           tracking=tracking,
                           estados_usados=estados_usados,
                           detalles_por_estado=detalles_por_estado
                           )
    

@app.route("/insertar_estado")
def interfaz_insertar_estado():
    tracking = request.args.get("tracking")

    if not tracking:
        return "Tracking no proporcionado", 400

    detalles_estado = controlador_estado_encomienda.get_estados_restantes(tracking)

    return render_template("simulacion_escaneo_qr.html",
                           tracking=tracking,
                           detalles_estado=detalles_estado)



@app.route("/ver_img_qr=<int:tracking>")
def ver_img_qr(tracking):
    return send_from_directory(f"static/comprobantes/{tracking}","qr.png")


@app.route('/api_insertar_estado', methods=['POST'])
def insertar_detalle_estado():
    try:
        data = request.get_json()
        tracking = data['tracking']
        detalle_estado = data['detalle_estado']
        tipo_comprobanteid = data.get('tipo_comprobanteid')  # opcional

        exito = controlador_estado_encomienda.insertar_seguimiento(tracking, detalle_estado, tipo_comprobanteid)

        if exito:
            return jsonify({"status": 1, "mensaje": "Estado insertado correctamente"})
        else:
            return jsonify({"status": 0, "mensaje": "Error al insertar estado"}), 500

    except Exception as e:
        return jsonify({"status": -1, "mensaje": f"Excepción: {str(e)}"}), 500
    
    
@app.route('/salida_informacion')
def salida_informacion():
    sucursal_origen = controlador_sucursal.sucursales_origen()
    unidades = controlador_unidad.get_capacidad_unidad()
    empleados = controlador_empleado.get_driver_employee()
    agencias = controlador_sucursal.get_agencias_data()
    paquetes = controlador_paquete.listar_paquetes_por_sucursal_escalas()
    recojo_casa = controlador_encomienda.get_recojo_casa()
    return render_template('salida_informacion.html',
                           sucursal_origen=sucursal_origen,
                           unidades=unidades,
                           empleados=empleados,
                           agencias=agencias,
                           paquetes = paquetes,
                           recojo_casa = recojo_casa)

@app.route('/sucursales_destino_api',  methods=["POST"])
def sucursales_destino_api():
    try:
        datos = request.get_json()
        id = datos.get('sucursal_origen_id')
        sucursal_destino = controlador_sucursal.sucursales_destino(id)
        return {
            'data': sucursal_destino,
            'msg': "Se listó con éxito",
            'status':1
        }
    except Exception as e:
        return {
            'data': [],
            'msg': f"Ocurrió un error al listar las distritos: {repr(e)}",
            'status':-1
        }

@app.route("/buscar_paquete_devolucion", methods=["POST"])
@validar_empleado()
def buscar_paquete_devolucion():
    """
    Endpoint para buscar paquetes disponibles para devolución
    """
    try:
        data = request.get_json()
        tracking = data.get('criterio', '').strip()
        
        if not tracking:
            return jsonify({
                'success': False,
                'message': 'Código de tracking requerido'
            }), 400
        
        # Validar que sea un número
        if not tracking.isdigit():
            return jsonify({
                'success': False,
                'message': 'El código de tracking debe ser numérico'
            }), 400
        
        paquete = controlador_programacion_devolucion.buscar_paquete(tracking)
        
        if paquete:
            # Validar que el paquete pueda ser devuelto
            puede_devolver = controlador_programacion_devolucion.validar_paquete_para_devolucion(paquete['tracking'])
            
            if puede_devolver:
                return jsonify({
                    'success': True,
                    'paquete': paquete,
                    'message': 'Paquete encontrado'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Este paquete no está disponible para devolución'
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Paquete no encontrado'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al buscar paquete: {str(e)}'
        }), 500


@app.route("/obtener_unidades_devolucion", methods=["POST"])
@validar_empleado()
def obtener_unidades_devolucion():
    """
    Endpoint para obtener unidades disponibles para devoluciones
    """
    try:
        data = request.get_json()
        tracking = data.get('tracking')
        
        if not tracking:
            return jsonify({
                'success': False,
                'message': 'Tracking requerido para buscar unidades disponibles'
            }), 400
        
        unidades = controlador_programacion_devolucion.obtener_unidades_disponibles(tracking)
        
        return jsonify({
            'success': True,
            'unidades': unidades
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener unidades: {str(e)}'
        }), 500


@app.route("/programar_devolucion", methods=["POST"])
@validar_empleado()
def programar_devolucion():
    """
    Endpoint para programar una devolución
    """
    try:
        data = request.get_json()
        tracking = data.get('tracking')
        unidad_id = data.get('unidad_id')
        
        if not tracking or not unidad_id:
            return jsonify({
                'success': False,
                'message': 'Tracking y unidad son requeridos'
            }), 400
        
        # Validar que el paquete pueda ser devuelto
        puede_devolver = controlador_programacion_devolucion.validar_paquete_para_devolucion(tracking)
        
        if not puede_devolver:
            return jsonify({
                'success': False,
                'message': 'Este paquete no puede ser programado para devolución'
            }), 400
        
        resultado = controlador_programacion_devolucion.programar_devolucion(tracking, unidad_id)
        
        if resultado['success']:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al programar devolución: {str(e)}'
        }), 500


@app.route("/historial_devoluciones", methods=["GET"])
@validar_empleado()
def historial_devoluciones():
    """
    Endpoint para obtener el historial de devoluciones
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        
        historial = controlador_programacion_devolucion.obtener_historial_devoluciones(limit)
        
        return jsonify({
            'success': True,
            'historial': historial
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener historial: {str(e)}'
        }), 500


@app.route("/estados_devolucion", methods=["GET"])
@validar_empleado()
def estados_devolucion():
    """
    Endpoint para obtener estados relacionados con devoluciones
    """
    try:
        estados = controlador_programacion_devolucion.obtener_estados_devolucion()
        
        return jsonify({
            'success': True,
            'estados': estados
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estados: {str(e)}'
        }), 500


# Opcional: Endpoint para validar un paquete específico
@app.route("/validar_paquete_devolucion/<int:tracking>", methods=["GET"])
@validar_empleado()
def validar_paquete_devolucion_endpoint(tracking):
    """
    Endpoint para validar si un paquete específico puede ser devuelto
    """
    try:
        puede_devolver = controlador_programacion_devolucion.validar_paquete_para_devolucion(tracking)
        
        return jsonify({
            'success': True,
            'puede_devolver': puede_devolver,
            'tracking': tracking
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al validar paquete: {str(e)}'
        }), 500


@app.route("/obtener_paquetes_estado_17", methods=["GET"])
@validar_empleado()
def obtener_paquetes_estado_17():
    """
    Endpoint para obtener paquetes con detalle_estado_id = 17
    """
    try:
        paquetes = controlador_programacion_devolucion.obtener_paquetes_estado_17()
        
        return jsonify({
            'success': True,
            'paquetes': paquetes
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener paquetes: {str(e)}'
        }), 500
    
####################SEGUIMIENTO DE RECLAMOS############################3

# Ruta principal de seguimiento de reclamos
@app.route("/seguimiento_reclamo")
def seguimiento_reclamo():
    """
    Página principal de seguimiento de reclamos
    """
    return render_template('seguimiento_reclamo.html')

# Ruta para buscar reclamo
@app.route("/buscar_reclamo", methods=["POST"])
def buscar_reclamo():
    """
    Busca un reclamo por ID o documento
    """
    try:
        reclamo_id = request.form.get('reclamo_id', '').strip()
        numero_documento = request.form.get('documento', '').strip()
        
        if not reclamo_id and not numero_documento:
            flash('Debe ingresar al menos un criterio de búsqueda', 'error')
            return redirect(url_for('seguimiento_reclamo'))
        
        # Convertir reclamo_id a entero si está presente
        if reclamo_id:
            try:
                reclamo_id = int(reclamo_id)
            except ValueError:
                flash('El ID del reclamo debe ser un número válido', 'error')
                return redirect(url_for('seguimiento_reclamo'))
        
        # Buscar el reclamo
        reclamo = controlador_seguimiento_reclamos.buscar_reclamo_por_id_o_documento(reclamo_id, numero_documento)
        
        if not reclamo:
            flash('No se encontró ningún reclamo con los criterios proporcionados', 'error')
            return redirect(url_for('seguimiento_reclamo'))
        
        # Obtener datos relacionados
        estados_reclamo = controlador_seguimiento_reclamos.obtener_estados_reclamo()
        seguimientos = controlador_seguimiento_reclamos.obtener_seguimientos_reclamo(reclamo['id'])
        ultimo_seguimiento = controlador_seguimiento_reclamos.obtener_ultimo_seguimiento_reclamo(reclamo['id'])
        estados_usados = controlador_seguimiento_reclamos.obtener_estados_usados_reclamo(reclamo['id'])
        
        # Agrupar seguimientos por estado
        seguimientos_por_estado = controlador_seguimiento_reclamos.agrupar_seguimientos_por_estado(seguimientos)
        
        return render_template('seguimiento_reclamo.html',
                             reclamo=reclamo,
                             estados_reclamo=estados_reclamo,
                             seguimientos_por_estado=seguimientos_por_estado,
                             ultimo_seguimiento=ultimo_seguimiento,
                             estados_usados=estados_usados)
        
    except Exception as e:
        flash(f'Error al buscar reclamo: {str(e)}', 'error')
        return redirect(url_for('seguimiento_reclamo'))

# Ruta directa con ID de reclamo
@app.route("/seguimiento_reclamo/<int:reclamo_id>")
def seguimiento_reclamo_directo(reclamo_id):
    """
    Acceso directo al seguimiento con ID de reclamo
    """
    try:
        # Buscar el reclamo
        reclamo = controlador_seguimiento_reclamos.buscar_reclamo_por_id_o_documento(reclamo_id=reclamo_id)
        
        if not reclamo:
            flash('No se encontró el reclamo especificado', 'error')
            return redirect(url_for('seguimiento_reclamo'))
        
        # Obtener datos relacionados
        estados_reclamo = controlador_seguimiento_reclamos.obtener_estados_reclamo()
        seguimientos = controlador_seguimiento_reclamos.obtener_seguimientos_reclamo(reclamo['id'])
        ultimo_seguimiento = controlador_seguimiento_reclamos.obtener_ultimo_seguimiento_reclamo(reclamo['id'])
        estados_usados = controlador_seguimiento_reclamos.obtener_estados_usados_reclamo(reclamo['id'])
        
        # Agrupar seguimientos por estado
        seguimientos_por_estado = controlador_seguimiento_reclamos.agrupar_seguimientos_por_estado(seguimientos)
        
        return render_template('seguimiento_reclamo.html',
                             reclamo=reclamo,
                             estados_reclamo=estados_reclamo,
                             seguimientos_por_estado=seguimientos_por_estado,
                             ultimo_seguimiento=ultimo_seguimiento,
                             estados_usados=estados_usados)
        
    except Exception as e:
        flash(f'Error al consultar reclamo: {str(e)}', 'error')
        return redirect(url_for('seguimiento_reclamo'))

# Endpoint para agregar seguimiento a reclamo (solo empleados)
@app.route("/agregar_seguimiento_reclamo", methods=["POST"])
@validar_empleado()
def agregar_seguimiento_reclamo():
    """
    Agrega un nuevo seguimiento a un reclamo existente
    """
    try:
        data = request.get_json()
        
        reclamo_id = data.get('reclamo_id')
        detalle_reclamo_id = data.get('detalle_reclamo_id')
        
        if not reclamo_id or not detalle_reclamo_id:
            return jsonify({
                'success': False,
                'message': 'Reclamo ID y Detalle Reclamo ID son requeridos'
            }), 400
        
        resultado = controlador_seguimiento_reclamos.agregar_seguimiento_reclamo(reclamo_id, detalle_reclamo_id)
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al agregar seguimiento: {str(e)}'
        }), 500

# Endpoint para obtener reclamos por estado (solo empleados)
@app.route("/reclamos_por_estado/<int:estado_id>", methods=["GET"])
@validar_empleado()
def reclamos_por_estado(estado_id):
    """
    Obtiene reclamos filtrados por estado
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        
        reclamos = controlador_seguimiento_reclamos.obtener_reclamos_por_estado_activo(estado_id, limit)
        
        return jsonify({
            'success': True,
            'reclamos': reclamos
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener reclamos: {str(e)}'
        }), 500

# Endpoint para obtener detalles de reclamo por estado (solo empleados)
@app.route("/detalles_reclamo_por_estado/<int:estado_id>", methods=["GET"])
@validar_empleado()
def detalles_reclamo_por_estado(estado_id):
    """
    Obtiene los detalles disponibles para un estado de reclamo
    """
    try:
        detalles = controlador_seguimiento_reclamos.obtener_detalles_reclamo_por_estado(estado_id)
        
        return jsonify({
            'success': True,
            'detalles': detalles
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener detalles: {str(e)}'
        }), 500

# Endpoint API para obtener información de reclamo (JSON)
@app.route("/api/reclamo/<int:reclamo_id>", methods=["GET"])
def api_info_reclamo(reclamo_id):
    """
    API endpoint para obtener información de un reclamo en formato JSON
    """
    try:
        reclamo = controlador_seguimiento_reclamos.buscar_reclamo_por_id_o_documento(reclamo_id=reclamo_id)
        
        if not reclamo:
            return jsonify({
                'success': False,
                'message': 'Reclamo no encontrado'
            }), 404
        
        ultimo_seguimiento = controlador_seguimiento_reclamos.obtener_ultimo_seguimiento_reclamo(reclamo['id'])
        seguimientos = controlador_seguimiento_reclamos.obtener_seguimientos_reclamo(reclamo['id'])
        
        return jsonify({
            'success': True,
            'reclamo': dict(reclamo),
            'ultimo_seguimiento': dict(ultimo_seguimiento) if ultimo_seguimiento else None,
            'seguimientos': [dict(s) for s in seguimientos]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al consultar reclamo: {str(e)}'
        }), 500

# Endpoint para validar si existe un tracking para reclamo
@app.route("/validar_tracking_reclamo/<int:tracking>", methods=["GET"])
def validar_tracking_reclamo(tracking):
    """
    Valida si un tracking existe y puede ser asociado a un reclamo
    """
    try:
        paquete = controlador_seguimiento_reclamos.validar_tracking_existe(tracking)
        
        if paquete:
            return jsonify({
                'success': True,
                'existe': True,
                'info_paquete': {
                    'tracking': paquete.get('tracking'),
                    'destinatario': paquete.get('destinatario_completo')
                }
            })
        else:
            return jsonify({
                'success': True,
                'existe': False,
                'message': 'Tracking no encontrado'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al validar tracking: {str(e)}'
        }), 500

# Endpoint para obtener todos los reclamos (vista administrativa)
@app.route("/admin/reclamos", methods=["GET"])
@validar_empleado()
def admin_reclamos():
    """
    Vista administrativa de todos los reclamos
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        reclamos = controlador_seguimiento_reclamos.obtener_todos_los_reclamos(limit)
        
        return render_template('admin_reclamos.html', reclamos=reclamos)
        
    except Exception as e:
        flash(f'Error al cargar reclamos: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

# Endpoint para obtener tipos de reclamo
@app.route("/api/tipos_reclamo", methods=["GET"])
def api_tipos_reclamo():
    """
    API para obtener tipos de reclamo disponibles
    """
    try:
        tipos = controlador_seguimiento_reclamos.obtener_tipos_reclamo()
        
        return jsonify({
            'success': True,
            'tipos': tipos
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener tipos de reclamo: {str(e)}'
        }), 500

# Endpoint para obtener motivos por tipo de reclamo
@app.route("/api/motivos_reclamo/<int:tipo_id>", methods=["GET"])
def api_motivos_reclamo(tipo_id):
    """
    API para obtener motivos por tipo de reclamo
    """
    try:
        motivos = controlador_seguimiento_reclamos.obtener_motivos_por_tipo_reclamo(tipo_id)
        
        return jsonify({
            'success': True,
            'motivos': motivos
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener motivos: {str(e)}'
        }), 500

# Endpoint para obtener causas por motivo de reclamo
@app.route("/api/causas_reclamo/<int:motivo_id>", methods=["GET"])
def api_causas_reclamo(motivo_id):
    """
    API para obtener causas por motivo de reclamo
    """
    try:
        causas = controlador_seguimiento_reclamos.obtener_causas_por_motivo_reclamo(motivo_id)
        
        return jsonify({
            'success': True,
            'causas': causas
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener causas: {str(e)}'
        }), 500

# Endpoint para obtener estados de reclamo
@app.route("/api/estados_reclamo", methods=["GET"])
def api_estados_reclamo():
    """
    API para obtener estados de reclamo disponibles
    """
    try:
        estados = controlador_seguimiento_reclamos.obtener_estados_reclamo()
        
        return jsonify({
            'success': True,
            'estados': estados
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estados: {str(e)}'
        }), 500
##############################################3
##############################################

if __name__ == "__main__":
    # app.run(host='192.168.48.178', port=8000, debug=True, use_reloader=True)
    # Thread(target=enviar_posiciones).start()
    # app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=True)
    socketio.run(app, host='0.0.0.0', port=8000, debug=True , use_reloader=True)


