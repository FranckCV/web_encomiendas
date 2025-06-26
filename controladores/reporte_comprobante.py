
from fpdf import FPDF
from datetime import datetime
import os
import qrcode
from PIL import Image

class ComprobantePDF(FPDF):
    def __init__(self, empresa_data):
        super().__init__()
        self.empresa = empresa_data
        
    def header(self):
        # Encabezado con datos de la empresa
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, self.empresa.get('razon_social', ''), ln=True, align="C")
        
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, f"RUC: {self.empresa.get('ruc', '')}", ln=True, align="C")
        self.cell(0, 6, self.empresa.get('direccion', ''), ln=True, align="C")
        self.cell(0, 6, f"Tel: {self.empresa.get('telefono', '')} | Email: {self.empresa.get('email', '')}", ln=True, align="C")
        self.ln(5)

    def comprobante_header(self, tipo_comprobante, serie, fecha):
        # Recuadro del tipo de comprobante
        self.set_fill_color(240, 240, 240)
        self.set_font("Helvetica", "B", 12)
        
        if tipo_comprobante.upper() == 'BOLETA':
            titulo = "BOLETA DE VENTA ELECTRÓNICA"
        else:
            titulo = "FACTURA ELECTRÓNICA"
            
        self.cell(0, 10, titulo, border=1, ln=True, align="C", fill=True)
        
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 8, f"RUC: {self.empresa.get('ruc', '')}", ln=True, align="C")
        self.cell(0, 8, serie, ln=True, align="C")
        self.ln(5)

    def cliente_section(self, cliente_data):
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, "DATOS DEL CLIENTE", ln=True, fill=True)
        
        self.set_font("Helvetica", "", 9)
        self.cell(30, 6, "Señor(es):", ln=False)
        nombre_completo = f"{cliente_data.get('nombre_siglas', '')} {cliente_data.get('apellidos_razon', '')}".strip()
        self.cell(0, 6, nombre_completo, ln=True)
        
        if cliente_data.get('documento_identidad'):
            tipo_doc = "DNI" if len(cliente_data.get('documento_identidad', '')) == 8 else "RUC"
            self.cell(30, 6, f"{tipo_doc}:", ln=False)
            self.cell(0, 6, cliente_data.get('documento_identidad', ''), ln=True)
        
        if cliente_data.get('direccion'):
            self.cell(30, 6, "Dirección:", ln=False)
            self.cell(0, 6, cliente_data.get('direccion', ''), ln=True)
        
        self.ln(3)
    def items_table(self, items):
        # Encabezados de la tabla
        self.set_font("Helvetica", "B", 9)
        self.cell(30, 7, "Cant.", border=1, align="C")
        self.cell(40, 7, "Unidad", border=1, align="C")
        self.cell(60, 7, "V. Unit.", border=1, align="C")
        self.cell(60, 7, "Importe", border=1, align="C")
        self.ln()

        # Contenido de la tabla
        self.set_font("Helvetica", "", 9)
        for item in items:
            cantidad = 1
            unidad = 'UNIDAD'

            try:
                tarifa = float(item.get('tarifa') or 0)
            except:
                tarifa = 0.00

            importe = tarifa * cantidad

            self.cell(30, 7, str(cantidad), border=1, align="R")
            self.cell(40, 7, unidad, border=1, align="C")
            self.cell(60, 7, f"{tarifa:.2f}", border=1, align="R")
            self.cell(60, 7, f"{importe:.2f}", border=1, align="R")
            self.ln()



    def totales_section(self, resumen):
        # Sección de totales alineada a la derecha
        x_start = 120
        self.set_xy(x_start, self.get_y() + 10)
        
        self.set_font("Helvetica", "", 9)
        
        # Op. Gravada
        self.cell(40, 6, "Op. Gravada:", ln=False, align="L")
        self.cell(30, 6, f"S/ {resumen.get('op_gravada', 0):.2f}", ln=True, align="R")
        self.set_x(x_start)
        
        # Op. Exonerada
        self.cell(40, 6, "Op. Exonerada:", ln=False, align="L")
        self.cell(30, 6, f"S/ {resumen.get('op_exonerada', 0):.2f}", ln=True, align="R")
        self.set_x(x_start)
        
        # Op. Inafecta
        self.cell(40, 6, "Op. Inafecta:", ln=False, align="L")
        self.cell(30, 6, f"S/ {resumen.get('op_inafecta', 0):.2f}", ln=True, align="R")
        self.set_x(x_start)
        
        # ISC
        self.cell(40, 6, "ISC:", ln=False, align="L")
        self.cell(30, 6, f"S/ {resumen.get('isc', 0):.2f}", ln=True, align="R")
        self.set_x(x_start)
        
        # IGV
        self.cell(40, 6, "IGV:", ln=False, align="L")
        self.cell(30, 6, f"S/ {resumen.get('igv', 0):.2f}", ln=True, align="R")
        self.set_x(x_start)
        
        # ICBPER
        self.cell(40, 6, "ICBPER:", ln=False, align="L")
        self.cell(30, 6, f"S/ {resumen.get('icbper', 0):.2f}", ln=True, align="R")
        self.set_x(x_start)
        
        # Otros Cargos
        self.cell(40, 6, "Otros Cargos:", ln=False, align="L")
        self.cell(30, 6, f"S/ {resumen.get('otros_cargos', 0):.2f}", ln=True, align="R")
        self.set_x(x_start)
        
        # Otros Tributos
        self.cell(40, 6, "Otros Tributos:", ln=False, align="L")
        self.cell(30, 6, f"S/ {resumen.get('otros_tributos', 0):.2f}", ln=True, align="R")
        self.set_x(x_start)
        
        # Importe Total (destacado)
        self.set_font("Helvetica", "B", 10)
        self.cell(40, 8, "Importe Total:", border=1, align="L")
        self.cell(30, 8, f"S/ {resumen.get('importe_total', 0):.2f}", border=1, align="R")
        self.ln(10)

    def son_section(self, monto_total):
        from num2words import num2words
        
        # Convertir número a palabras
        try:
            entero = int(monto_total)
            decimal = int(round((monto_total - entero) * 100))
            
            palabras = num2words(entero, lang='es').upper()
            if decimal > 0:
                son_text = f"SON: {palabras} CON {decimal:02d}/100 SOLES"
            else:
                son_text = f"SON: {palabras} Y 00/100 SOLES"
        except:
            son_text = f"SON: MONTO EN SOLES"
        
        self.set_font("Helvetica", "", 9)
        self.cell(0, 6, son_text, ln=True)
        self.ln(5)

    def qr_section(self, qr_data, qr_path=None):
        # Generar código QR
        if not qr_path or not os.path.exists(qr_path):
            qr = qrcode.QRCode(version=1, box_size=3, border=1)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            temp_path = "temp_qr.png"
            qr_img.save(temp_path)
            qr_path = temp_path
        
        # Insertar QR en el PDF
        try:
            self.image(qr_path, x=10, y=self.get_y(), w=30, h=30)
        except:
            pass  # Si falla la imagen, continuar sin QR
        
        # Limpiar archivo temporal
        if qr_path == "temp_qr.png" and os.path.exists(qr_path):
            os.remove(qr_path)

    def footer_text(self):
        self.ln(35)  # Espacio para el QR
        self.set_font("Helvetica", "", 8)
        footer_msg = ("Esta es una representación impresa de la Boleta de Venta Electrónica, "
                     "generada en el Sistema de la SUNAT. El Emisor Electrónico puede verificarla "
                     "utilizando su clave SOL, el Adquiriente o Usuario puede consultar su validez "
                     "en SUNAT Virtual: www.sunat.gob.pe, en Opciones sin Clave SOL / Consulta de Validez")
        
        # Texto justificado manualmente
        words = footer_msg.split()
        lines = []
        current_line = ""
        
        for word in words:
            if self.get_string_width(current_line + " " + word) < 180:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        for line in lines:
            self.cell(0, 4, line, ln=True, align="L")

def generar_comprobante_pdf(transaccion, cliente, empresa, tipo_comprobante, 
                           comprobante_serie, items, resumen, qr_path=None, 
                           masivo=False, ruta_pdf="comprobante.pdf"):
    
    # Crear directorio si no existe
    directorio = os.path.dirname(ruta_pdf)
    if directorio:
        os.makedirs(directorio, exist_ok=True)
    
    pdf = ComprobantePDF(empresa)
    pdf.add_page()
    
    # Encabezado del comprobante
    fecha_emision = transaccion.get('fecha_emision', datetime.now().strftime("%d/%m/%Y"))
    pdf.comprobante_header(tipo_comprobante, comprobante_serie, fecha_emision)
    
    # Datos del cliente
    pdf.cliente_section(cliente)
    
    # Tabla de items
    pdf.items_table(items)
    
    # Sección de totales
    pdf.totales_section(resumen)
    
    # SON (monto en letras)
    pdf.son_section(float(resumen.get('importe_total', 0)))
    
    # Código QR
    qr_data = f"{empresa.get('ruc')}|{tipo_comprobante}|{comprobante_serie}|{resumen.get('importe_total', 0)}"
    pdf.qr_section(qr_data, qr_path)
    
    # Texto del pie
    pdf.footer_text()
    
    # Guardar PDF
    pdf.output(ruta_pdf)