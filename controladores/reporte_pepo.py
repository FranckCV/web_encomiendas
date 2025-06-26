from fpdf import FPDF
from datetime import datetime
import os

class GuiaRemisionPDF(FPDF):
    def header(self):
        # Título principal
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "GUÍA DE REMISIÓN - TRANSPORTISTA", border=False, ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, title, ln=True, fill=True)

    def section_text(self, label, text):
        self.set_font("Helvetica", "", 9)
        self.cell(50, 6, f"{label}:", ln=False)
        self.cell(0, 6, text, ln=True)

    def bienes_table(self, items):
        self.set_font("Helvetica", "B", 9)
        self.cell(70, 7, "Descripción", border=1)
        self.cell(30, 7, "Unidad", border=1)
        self.cell(30, 7, "Cantidad", border=1, align="R")
        self.cell(30, 7, "Peso (kg)", border=1, align="R")
        self.ln()

        self.set_font("Helvetica", "", 9)
        for item in items:
            self.cell(70, 7, item["descripcion"], border=1)
            self.cell(30, 7, item["unidad"], border=1)
            self.cell(30, 7, str(item["cantidad"]), border=1, align="R")
            self.cell(30, 7, str(item["peso"]), border=1, align="R")
            self.ln()

def generar_guia_pdf(datos, filename="static/img/guias/guia_remision.pdf"):
    directorio = os.path.dirname(filename)
    if directorio:  # Solo crear si hay una ruta válida
        os.makedirs(directorio, exist_ok=True)

    pdf = GuiaRemisionPDF()
    pdf.add_page()

    # Sección Emisor
    pdf.section_title("1. Datos del Emisor")
    pdf.section_text("RUC", datos["emisor"]["ruc"])
    pdf.section_text("Razón Social", datos["emisor"]["razon_social"])
    pdf.section_text("Dirección", datos["emisor"]["direccion"])
    pdf.ln(3)

    # Sección Destinatario
    pdf.section_title("2. Datos del Destinatario")
    pdf.section_text("DNI/RUC", datos["destinatario"]["ruc_dni"])
    pdf.section_text("Nombre / Razón Social", datos["destinatario"]["nombre"])
    pdf.section_text("Dirección", datos["destinatario"]["direccion"])
    pdf.ln(3)

    # Sección Transporte
    pdf.section_title("3. Datos del Transporte")
    pdf.section_text("Fecha de Inicio", datos["transporte"]["fecha_inicio"])
    pdf.section_text("Punto de Partida", datos["transporte"]["punto_partida"])
    pdf.section_text("Punto de Llegada", datos["transporte"]["punto_llegada"])
    pdf.section_text("Placa del Vehículo", datos["transporte"]["placa"])
    pdf.section_text("Conductor", datos["transporte"]["conductor"])
    pdf.section_text("DNI del Conductor", datos["transporte"]["dni_conductor"])
    pdf.ln(3)

    # Sección Bienes
    pdf.section_title("4. Bienes Transportados")
    pdf.bienes_table(datos["bienes"])

    pdf.output(filename)


# datos_simulados = {
#     "emisor": {
#         "ruc": "20123456789",
#         "razon_social": "Transportes Andinos S.A.",
#         "direccion": "Av. Principal 123, Lima"
#     },
#     "destinatario": {
#         "ruc_dni": "10456789012",
#         "nombre": "Juan Pérez",
#         "direccion": "Calle Comercio 456, Arequipa"
#     },
#     "transporte": {
#         "fecha_inicio": "2025-06-25",
#         "punto_partida": "Lima - Lima - San Isidro",
#         "punto_llegada": "Arequipa - Arequipa - Cercado",
#         "placa": "ABC-123",
#         "conductor": "Carlos Gómez",
#         "dni_conductor": "44556677"
#     },
#     "bienes": [
#         {"descripcion": "Cajas de repuestos", "unidad": "Caja", "cantidad": 10, "peso": 120},
#         {"descripcion": "Herramientas eléctricas", "unidad": "Unidad", "cantidad": 5, "peso": 35.5}
#     ]
# }

# generar_guia_pdf(datos_simulados)
