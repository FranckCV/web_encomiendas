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
        self.cell(0, 8, self.empresa.get('nombre', ''), ln=True, align="C")

        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, f"RUC: {self.empresa.get('ruc', '')}", ln=True, align="C")
        
        direccion = self.empresa.get('direccion', '')
        ubicacion = f"{self.empresa.get('distrito', '')}, {self.empresa.get('provincia', '')} - {self.empresa.get('departamento', '')}"
        self.cell(0, 6, f"{direccion}, {ubicacion}", ln=True, align="C")
        
        self.cell(0, 6, f"Tel: {self.empresa.get('nro_telefono', '')} | Email: {self.empresa.get('correo', '')}", ln=True, align="C")
        self.ln(5)

    def comprobante_header(self, tipo_comprobante, serie, fecha):
        self.set_fill_color(240, 240, 240)
        self.set_font("Helvetica", "B", 12)

        tipo = tipo_comprobante.upper()
        if not tipo.endswith("ELECTRÓNICA"):
            tipo += " ELECTRÓNICA"

        self.cell(0, 10, tipo, border=1, ln=True, align="C", fill=True)

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
        # Encabezados de la tabla con anchos ajustados
        self.set_font("Helvetica", "B", 9)
        self.cell(20, 7, "Cant.", border=1, align="C")
        self.cell(40, 7, "Unidad", border=1, align="C")
        self.cell(90, 7, "Servicio", border=1, align="C")
        self.cell(25, 7, "V. Unit.", border=1, align="C")
        self.cell(25, 7, "Importe", border=1, align="C")
        self.ln()

        # Contenido
        self.set_font("Helvetica", "", 8)
        for item in items:
            cantidad = 1
            unidad = "SERVICIO DE TRANSPORTE"
            # Cambio de formato: departamento/provincia/distrito
            servicio = f"{item['origen']['departamento']}/{item['origen']['provincia']}/{item['origen']['distrito']} -> {item['destino']['departamento']}/{item['destino']['provincia']}/{item['destino']['distrito']}"
            try:
                tarifa = float(item.get('tarifa') or 0)
            except:
                tarifa = 0.00
            importe = tarifa * cantidad

            # Calcular altura necesaria para el texto del servicio
            servicio_lines = self.get_text_lines(servicio, 90)
            line_height = 7
            cell_height = max(line_height, len(servicio_lines) * 4)

            # Guardar posición Y inicial
            y_start = self.get_y()

            # Cantidad
            self.cell(20, cell_height, str(cantidad), border=1, align="C")
            
            # Unidad
            self.cell(40, cell_height, unidad, border=1, align="C")
            
            # Servicio (texto multilínea)
            x_servicio = self.get_x()
            self.cell(90, cell_height, "", border=1)  # Celda vacía con borde
            self.set_xy(x_servicio + 1, y_start + 1)  # Posición dentro de la celda
            for i, line in enumerate(servicio_lines):
                if i > 0:
                    self.ln(4)
                    self.set_x(x_servicio + 1)
                self.cell(88, 4, line, align="L")
            
            # Volver a la posición correcta para las siguientes celdas
            self.set_xy(x_servicio + 90, y_start)
            
            # Valor unitario
            self.cell(25, cell_height, f"S/ {tarifa:.2f}", border=1, align="R")
            
            # Importe
            self.cell(25, cell_height, f"S/ {importe:.2f}", border=1, align="R")
            
            self.ln(cell_height)

    def get_text_lines(self, text, max_width):
        """Divide el texto en líneas que caben en el ancho especificado"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.get_string_width(test_line) <= max_width - 2:  # -2 para margen
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
            
        return lines if lines else [text]

    def totales_section(self, resumen):
        x_start = 120
        self.set_xy(x_start, self.get_y() + 10)
        self.set_font("Helvetica", "", 9)

        campos = [
            ("Op. Gravada", "op_gravada"),
            ("Op. Exonerada", "op_exonerada"),
            ("Op. Inafecta", "op_inafecta"),
            ("ISC", "isc"),
            ("IGV", "igv"),
            ("ICBPER", "icbper"),
            ("Otros Cargos", "otros_cargos"),
            ("Otros Tributos", "otros_tributos")
        ]

        for label, key in campos:
            self.cell(40, 6, f"{label}:", ln=False, align="L")
            self.cell(30, 6, f"S/ {resumen.get(key, 0):.2f}", ln=True, align="R")
            self.set_x(x_start)

        self.set_font("Helvetica", "B", 10)
        self.cell(40, 8, "Importe Total:", border=1, align="L")
        self.cell(30, 8, f"S/ {resumen.get('importe_total', 0):.2f}", border=1, align="R")
        self.ln(10)

    def son_section(self, monto_total):
        from num2words import num2words
        try:
            entero = int(monto_total)
            decimal = int(round((monto_total - entero) * 100))
            palabras = num2words(entero, lang='es').upper()
            if decimal > 0:
                son_text = f"SON: {palabras} CON {decimal:02d}/100 SOLES"
            else:
                son_text = f"SON: {palabras} Y 00/100 SOLES"
        except:
            son_text = "SON: MONTO EN SOLES"

        self.set_font("Helvetica", "", 9)
        self.cell(0, 6, son_text, ln=True)
        self.ln(5)

    def qr_section(self, qr_data, qr_path=None):
        if not qr_path or not os.path.exists(qr_path):
            qr = qrcode.QRCode(version=1, box_size=3, border=1)
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            temp_path = "temp_qr.png"
            qr_img.save(temp_path)
            qr_path = temp_path

        try:
            self.image(qr_path, x=10, y=self.get_y(), w=30, h=30)
        except:
            pass

        if qr_path == "temp_qr.png" and os.path.exists(qr_path):
            os.remove(qr_path)

    def footer_text(self):
        self.ln(35)
        self.set_font("Helvetica", "", 8)
        footer_msg = (
            "Esta es una representación impresa de la Boleta de Venta Electrónica, "
            "generada en el Sistema de la SUNAT. El Emisor Electrónico puede verificarla "
            "utilizando su clave SOL, el Adquiriente o Usuario puede consultar su validez "
            "en SUNAT Virtual: www.sunat.gob.pe, en Opciones sin Clave SOL / Consulta de Validez"
        )

        words = footer_msg.split()
        current_line = ""
        for word in words:
            if self.get_string_width(current_line + " " + word) < 180:
                current_line += " " + word if current_line else word
            else:
                self.cell(0, 4, current_line, ln=True, align="L")
                current_line = word
        if current_line:
            self.cell(0, 4, current_line, ln=True, align="L")

def generar_comprobante_pdf(transaccion, cliente, empresa, tipo_comprobante, 
                           comprobante_serie, items, resumen, qr_path=None, 
                           masivo=False, ruta_pdf="comprobante.pdf"):

    directorio = os.path.dirname(ruta_pdf)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    pdf = ComprobantePDF(empresa)
    pdf.add_page()

    fecha_emision = transaccion.get('fecha_emision', datetime.now().strftime("%d/%m/%Y"))
    pdf.comprobante_header(tipo_comprobante, comprobante_serie, fecha_emision)

    pdf.cliente_section(cliente)
    pdf.items_table(items)
    pdf.totales_section(resumen)
    pdf.son_section(float(resumen.get('importe_total', 0)))

    qr_data = f"{empresa.get('ruc')}|{tipo_comprobante}|{comprobante_serie}|{resumen.get('importe_total', 0)}"
    pdf.qr_section(qr_data, qr_path)

    pdf.footer_text()
    pdf.output(ruta_pdf)