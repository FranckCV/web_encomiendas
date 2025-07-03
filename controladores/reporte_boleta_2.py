"""
Módulo para generar comprobantes de venta en PDF (Boletas y Facturas)
Archivo: reporte_boleta_2.py
"""

from fpdf import FPDF
from datetime import datetime
import os
import qrcode
from PIL import Image
from num2words import num2words


class ComprobantePDF(FPDF):
    """Clase para generar PDFs de comprobantes de venta"""
    
    def __init__(self, empresa_data):
        super().__init__()
        self.empresa = empresa_data
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Encabezado del documento con datos de la empresa"""
        # Logo de la empresa (si existe)
        logo_path = self.empresa.get('logo_path')
        if logo_path and os.path.exists(logo_path):
            try:
                self.image(logo_path, 10, 8, 33)
                self.ln(20)
            except:
                pass
        
        # Datos de la empresa
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, self.empresa.get('nombre', '1EMPRESA'), ln=True, align="C")
        
        self.set_font("Arial", "", 11)
        self.cell(0, 6, f"RUC: {self.empresa.get('ruc', '')}", ln=True, align="C")
        self.cell(0, 6, self.empresa.get('direccion', ''), ln=True, align="C")
        
        contacto = []
        if self.empresa.get('telefono'):
            contacto.append(f"Tel: {self.empresa.get('telefono')}")
        if self.empresa.get('email'):
            contacto.append(f"Email: {self.empresa.get('email')}")
        
        if contacto:
            self.cell(0, 6, " | ".join(contacto), ln=True, align="C")
        
        self.ln(8)

    def comprobante_header(self, tipo_comprobante, serie, fecha, hora=None):
        """Encabezado específico del comprobante"""
        # Recuadro del tipo de comprobante
        self.set_fill_color(52, 73, 94)  # Color azul oscuro
        self.set_text_color(255, 255, 255)  # Texto blanco
        self.set_font("Arial", "B", 14)
        
        if tipo_comprobante.upper() == 'BOLETA':
            titulo = "BOLETA DE VENTA ELECTRÓNICA"
        else:
            titulo = "FACTURA ELECTRÓNICA"
            
        self.cell(0, 12, titulo, border=1, ln=True, align="C", fill=True)
        
        # Restablecer colores
        self.set_text_color(0, 0, 0)
        self.set_fill_color(245, 245, 245)
        
        # Información del comprobante
        self.set_font("Arial", "B", 11)
        self.cell(0, 8, f"RUC: {self.empresa.get('ruc', '')}", ln=True, align="C", fill=True)
        self.cell(0, 8, f"SERIE: {serie}", ln=True, align="C", fill=True)
        
        # FIX: Convertir fecha a string si es necesario
        fecha_str = fecha
        if hasattr(fecha, 'strftime'):  # Si es un objeto date/datetime
            fecha_str = fecha.strftime('%d/%m/%Y')
        elif not isinstance(fecha, str):
            fecha_str = str(fecha)
        
        fecha_hora = fecha_str
        if hora:
            # Convertir hora a string si es necesario
            hora_str = hora
            if hasattr(hora, 'strftime'):  # Si es un objeto time/datetime
                hora_str = hora.strftime('%H:%M:%S')
            elif not isinstance(hora, str):
                hora_str = str(hora)
            fecha_hora += f" - {hora_str}"
        
        self.cell(0, 8, f"FECHA: {fecha_hora}", ln=True, align="C", fill=True)
        
        self.ln(8)

    def cliente_section(self, cliente_data):
        """Sección con datos del cliente"""
        self.set_font("Arial", "B", 11)
        self.set_fill_color(52, 73, 94)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, "DATOS DEL CLIENTE", ln=True, fill=True, align="C")
        
        # Restablecer colores
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 10)
        
        # Nombre completo
        self.cell(35, 7, "Señor(es):", ln=False, border=1)
        nombre_completo = f"{cliente_data.get('nombre_siglas', '')} {cliente_data.get('apellidos_razon', '')}".strip()
        self.cell(0, 7, nombre_completo, ln=True, border=1)
        
        # Documento de identidad
        if cliente_data.get('documento_identidad'):
            tipo_doc = cliente_data.get('tipo_documento', 'DNI')
            self.cell(35, 7, f"{tipo_doc}:", ln=False, border=1)
            self.cell(0, 7, cliente_data.get('documento_identidad', ''), ln=True, border=1)
        
        # Dirección
        self.cell(35, 7, "Dirección:", ln=False, border=1)
        self.cell(0, 7, cliente_data.get('direccion', 'No especificada'), ln=True, border=1)
        
        # Email y teléfono (si existen)
        if cliente_data.get('correo'):
            self.cell(35, 7, "Email:", ln=False, border=1)
            self.cell(0, 7, cliente_data.get('correo', ''), ln=True, border=1)
        
        if cliente_data.get('telefono'):
            self.cell(35, 7, "Teléfono:", ln=False, border=1)
            self.cell(0, 7, cliente_data.get('telefono', ''), ln=True, border=1)
        
        self.ln(8)

    def items_table_header(self):
        """Encabezados de la tabla de artículos"""
        self.set_font("Arial", "B", 10)
        self.set_fill_color(52, 73, 94)
        self.set_text_color(255, 255, 255)
        
        # Encabezados
        self.cell(15, 8, "CANT", border=1, align="C", fill=True)
        self.cell(25, 8, "CÓDIGO", border=1, align="C", fill=True)
        self.cell(85, 8, "DESCRIPCIÓN", border=1, align="C", fill=True)
        self.cell(25, 8, "P. UNIT.", border=1, align="C", fill=True)
        self.cell(30, 8, "IMPORTE", border=1, align="C", fill=True)
        self.ln()
        
        # Restablecer colores
        self.set_text_color(0, 0, 0)

    def items_table_row(self, item):
        """Fila de la tabla de artículos"""
        self.set_font("Arial", "", 9)
        
        cantidad = float(item.get('cantidad', 1))
        precio_unitario = float(item.get('precio_unitario', 0))
        subtotal = cantidad * precio_unitario
        
        # Datos del artículo
        codigo = str(item.get('codigo', item.get('articuloid', '')))
        descripcion = item.get('descripcion', item.get('articulo_nombre', ''))
        
        # Agregar dimensiones si existen
        if item.get('dimensiones'):
            descripcion += f" - {item.get('dimensiones')}"
        if item.get('tamaño'):
            descripcion += f" ({item.get('tamaño')})"
        
        # Limitar longitud de descripción
        if len(descripcion) > 50:
            descripcion = descripcion[:47] + "..."
        
        self.cell(15, 7, f"{cantidad:.0f}", border=1, align="C")
        self.cell(25, 7, codigo, border=1, align="C")
        self.cell(85, 7, descripcion, border=1, align="L")
        self.cell(25, 7, f"S/ {precio_unitario:.2f}", border=1, align="R")
        self.cell(30, 7, f"S/ {subtotal:.2f}", border=1, align="R")
        self.ln()

    def items_table(self, items):
        """Tabla completa de artículos"""
        self.items_table_header()
        
        for item in items:
            self.items_table_row(item)
        
        self.ln(5)

    def totales_section(self, resumen):
        """Sección de totales"""
        # Posición para totales (lado derecho)
        x_start = 120
        y_start = self.get_y()
        
        self.set_xy(x_start, y_start)
        self.set_font("Arial", "", 10)
        
        # Crear tabla de totales
        totales = [
            ("Op. Gravada:", resumen.get('op_gravada', 0)),
            ("Op. Exonerada:", resumen.get('op_exonerada', 0)),
            ("Op. Inafecta:", resumen.get('op_inafecta', 0)),
            ("ISC:", resumen.get('isc', 0)),
            ("IGV (18%):", resumen.get('igv', 0)),
            ("ICBPER:", resumen.get('icbper', 0)),
            ("Otros Cargos:", resumen.get('otros_cargos', 0)),
            ("Otros Tributos:", resumen.get('otros_tributos', 0))
        ]
        
        for concepto, valor in totales:
            self.cell(45, 6, concepto, border=1, align="L")
            self.cell(35, 6, f"S/ {valor:.2f}", border=1, align="R")
            self.ln()
            self.set_x(x_start)
        
        # Total final destacado
        self.set_font("Arial", "B", 12)
        self.set_fill_color(52, 73, 94)
        self.set_text_color(255, 255, 255)
        self.cell(45, 10, "IMPORTE TOTAL:", border=1, align="L", fill=True)
        self.cell(35, 10, f"S/ {resumen.get('importe_total', 0):.2f}", border=1, align="R", fill=True)
        
        # Restablecer colores
        self.set_text_color(0, 0, 0)
        self.ln(15)

    def son_section(self, monto_total):
        """Monto en letras"""
        try:
            # Convertir a entero y decimal
            entero = int(monto_total)
            decimal = int(round((monto_total - entero) * 100))
            
            # Convertir a palabras
            palabras = num2words(entero, lang='es').upper()
            
            if decimal > 0:
                son_text = f"SON: {palabras} CON {decimal:02d}/100 SOLES"
            else:
                son_text = f"SON: {palabras} Y 00/100 SOLES"
                
        except Exception as e:
            print(f"Error al convertir monto a palabras: {e}")
            son_text = f"SON: {monto_total:.2f} SOLES"
        
        self.set_font("Arial", "B", 10)
        self.set_fill_color(245, 245, 245)
        self.cell(0, 8, son_text, ln=True, border=1, fill=True, align="C")
        self.ln(8)

    def generar_qr(self, qr_data, qr_path):
        """Generar código QR"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,
                border=2
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(qr_path)
            return True
        except Exception as e:
            print(f"Error al generar QR: {e}")
            return False

    def qr_section(self, qr_data, qr_path=None):
        """Sección del código QR"""
        if not qr_path:
            qr_path = "temp_qr.png"
        
        # Generar QR
        qr_generado = self.generar_qr(qr_data, qr_path)
        
        if qr_generado and os.path.exists(qr_path):
            try:
                # Insertar QR en el PDF
                y_qr = self.get_y()
                self.image(qr_path, x=15, y=y_qr, w=35, h=35)
                
                # Texto explicativo al lado del QR
                self.set_xy(55, y_qr + 5)
                self.set_font("Arial", "", 8)
                self.multi_cell(140, 4, 
                    "Representación impresa de la Boleta/Factura Electrónica.\n"
                    "Consulte su validez en: www.sunat.gob.pe\n"
                    "Autorizado mediante Resolución de Intendencia\n"
                    f"QR: {qr_data[:50]}...")
                
                # Limpiar archivo temporal
                if qr_path == "temp_qr.png":
                    try:
                        os.remove(qr_path)
                    except:
                        pass
                        
            except Exception as e:
                print(f"Error al insertar QR en PDF: {e}")
        
        self.ln(40)

    def footer_legal(self):
        """Pie de página con información legal"""
        self.ln(10)
        self.set_font("Arial", "", 8)
        self.set_text_color(100, 100, 100)
        
        footer_text = (
            "Esta es una representación impresa de la Boleta de Venta Electrónica, "
            "generada en el Sistema Integrado de Facturación Electrónica de la SUNAT. "
            "Para consultar su validez diríjase a www.sunat.gob.pe en Opciones sin "
            "Clave SOL / Consulta de Validez del Comprobante de Pago."
        )
        
        self.multi_cell(0, 4, footer_text, align="J")
        
        # Línea de separación
        self.ln(3)
        self.line(10, self.get_y(), 200, self.get_y())
        
        # Información adicional
        self.ln(2)
        self.set_font("Arial", "I", 7)
        self.cell(0, 4, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 
                 align="C")


def generar_comprobante_venta_pdf(transaccion, cliente, empresa, tipo_comprobante, 
                                 comprobante_serie, items, resumen, qr_path=None, 
                                 ruta_pdf="comprobante_venta.pdf"):
    """
    Función principal para generar PDF de comprobante de venta
    
    Args:
        transaccion (dict): Datos de la transacción
        cliente (dict): Datos del cliente
        empresa (dict): Datos de la empresa
        tipo_comprobante (str): 'BOLETA' o 'FACTURA'
        comprobante_serie (str): Serie del comprobante
        items (list): Lista de artículos vendidos
        resumen (dict): Resumen de totales
        qr_path (str, optional): Ruta del código QR
        ruta_pdf (str): Ruta de salida del PDF
    """
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta_pdf)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
        
        # Crear PDF
        pdf = ComprobantePDF(empresa)
        pdf.add_page()
        
        # Generar contenido - FIX: Manejo correcto de fechas
        fecha_raw = transaccion.get('fecha')
        hora_raw = transaccion.get('hora')
        
        # Convertir fecha a string
        if fecha_raw:
            if hasattr(fecha_raw, 'strftime'):  # datetime.date o datetime.datetime
                fecha_emision = fecha_raw.strftime("%d/%m/%Y")
            else:
                fecha_emision = str(fecha_raw)
        else:
            fecha_emision = datetime.now().strftime("%d/%m/%Y")
        
        # Convertir hora a string
        if hora_raw:
            if hasattr(hora_raw, 'strftime'):  # datetime.time o datetime.datetime
                hora_emision = hora_raw.strftime("%H:%M:%S")
            else:
                hora_emision = str(hora_raw)
        else:
            hora_emision = datetime.now().strftime("%H:%M:%S")
        
        # Encabezado del comprobante
        pdf.comprobante_header(tipo_comprobante, comprobante_serie, fecha_emision, hora_emision)
        
        # Datos del cliente
        pdf.cliente_section(cliente)
        
        # Tabla de artículos
        if items:
            pdf.items_table(items)
        
        # Totales
        pdf.totales_section(resumen)
        
        # Monto en letras
        pdf.son_section(float(resumen.get('importe_total', 0)))
        
        # Código QR
        ruc = empresa.get('ruc', '')
        tipo_doc = '03' if tipo_comprobante.upper() == 'BOLETA' else '01'
        serie_numero = comprobante_serie.replace('-', '|')
        igv = resumen.get('igv', 0)
        total = resumen.get('importe_total', 0)
        
        # FIX: Formato de fecha para QR (YYYY-MM-DD)
        if hasattr(fecha_raw, 'strftime'):
            fecha_qr = fecha_raw.strftime("%Y-%m-%d")
        else:
            try:
                # Intentar parsear si es string en formato DD/MM/YYYY
                if isinstance(fecha_raw, str) and '/' in fecha_raw:
                    from datetime import datetime
                    fecha_obj = datetime.strptime(fecha_raw, "%d/%m/%Y")
                    fecha_qr = fecha_obj.strftime("%Y-%m-%d")
                else:
                    fecha_qr = str(fecha_raw) if fecha_raw else datetime.now().strftime("%Y-%m-%d")
            except:
                fecha_qr = datetime.now().strftime("%Y-%m-%d")
        
        doc_cliente = cliente.get('documento_identidad', '')
        
        qr_data = f"{ruc}|{tipo_doc}|{serie_numero}|{igv:.2f}|{total:.2f}|{fecha_qr}|{doc_cliente}"
        pdf.qr_section(qr_data, qr_path)
        
        # Pie legal
        pdf.footer_legal()
        
        # Guardar PDF
        pdf.output(ruta_pdf)
        
        print(f"Comprobante generado exitosamente: {ruta_pdf}")
        return True
        
    except Exception as e:
        print(f"Error al generar comprobante PDF: {str(e)}")
        import traceback
        traceback.print_exc()  # Para debugging
        return False



def generar_comprobante_masivo(transacciones_data, ruta_directorio="comprobantes_masivos"):
    """
    Generar múltiples comprobantes en lote
    
    Args:
        transacciones_data (list): Lista de diccionarios con datos de transacciones
        ruta_directorio (str): Directorio donde guardar los comprobantes
    """
    try:
        if not os.path.exists(ruta_directorio):
            os.makedirs(ruta_directorio, exist_ok=True)
        
        resultados = []
        
        for i, data in enumerate(transacciones_data):
            try:
                nombre_archivo = f"comprobante_{data['transaccion']['num_serie']:08d}.pdf"
                ruta_completa = os.path.join(ruta_directorio, nombre_archivo)
                
                exito = generar_comprobante_venta_pdf(
                    transaccion=data['transaccion'],
                    cliente=data['cliente'],
                    empresa=data['empresa'],
                    tipo_comprobante=data['tipo_comprobante'],
                    comprobante_serie=data['comprobante_serie'],
                    items=data['items'],
                    resumen=data['resumen'],
                    ruta_pdf=ruta_completa
                )
                
                resultados.append({
                    'num_serie': data['transaccion']['num_serie'],
                    'archivo': nombre_archivo,
                    'exito': exito
                })
                
            except Exception as e:
                print(f"Error procesando transacción {i+1}: {str(e)}")
                resultados.append({
                    'num_serie': data.get('transaccion', {}).get('num_serie', 'N/A'),
                    'archivo': f"error_{i+1}.pdf",
                    'exito': False,
                    'error': str(e)
                })
        
        return resultados
        
    except Exception as e:
        print(f"Error en generación masiva: {str(e)}")
        return []


# Ejemplo de uso
# if __name__ == "__main__":
#     # Datos de ejemplo para prueba
#     empresa_ejemplo = {
#         'razon_social': 'MI EMPRESA S.A.C.',
#         'ruc': '20123456789',
#         'direccion': 'Av. Principal 123, Lima, Perú',
#         'telefono': '01-234-5678',
#         'email': 'ventas@miempresa.com',
#         'igv': 18
#     }
    
#     cliente_ejemplo = {
#         'nombre_siglas': 'Juan Carlos',
#         'apellidos_razon': 'Pérez García',
#         'documento_identidad': '12345678',
#         'tipo_documento': 'DNI',
#         'direccion': 'Jr. Los Alamos 456',
#         'correo': 'juan@email.com',
#         'telefono': '987654321'
#     }
    
#     transaccion_ejemplo = {
#         'num_serie': 1,
#         'fecha': '2024-01-15',
#         'hora': '14:30:00',
#         'monto_total': 118.0
#     }
    
#     items_ejemplo = [
#         {
#             'codigo': 'ART001',
#             'descripcion': 'Producto de Ejemplo',
#             'cantidad': 2,
#             'precio_unitario': 50.0,
#             'dimensiones': '10x20x30 cm'
#         }
#     ]
    
#     resumen_ejemplo = {
#         'op_gravada': 100.0,
#         'op_exonerada': 0,
#         'op_inafecta': 0,
#         'isc': 0,
#         'igv': 18.0,
#         'icbper': 0,
#         'otros_cargos': 0,
#         'otros_tributos': 0,
#         'importe_total': 118.0
#     }
    
#     # Generar comprobante de prueba
#     generar_comprobante_venta_pdf(
#         transaccion=transaccion_ejemplo,
#         cliente=cliente_ejemplo,
#         empresa=empresa_ejemplo,
#         tipo_comprobante='BOLETA',
#         comprobante_serie='B001-00000001',
#         items=items_ejemplo,
#         resumen=resumen_ejemplo,
#         ruta_pdf='comprobante_prueba.pdf'
#     )