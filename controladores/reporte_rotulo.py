from fpdf import FPDF
import qrcode
import os

def generar_rotulo_pdf(datos, ruta_pdf):
    # Crear QR con el tracking
    tracking = datos['tracking']
    qr = qrcode.make(str(tracking))
    ruta_qr = "temp_qr.png"
    qr.save(ruta_qr)

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Dimensiones y posiciones
    x_inicio = 10
    y_inicio = 15
    ancho_total = 190
    alto_total = 120
    
    # Borde principal
    pdf.rect(x_inicio, y_inicio, ancho_total, alto_total)

    # Tracking y Fecha (líneas guía + texto)
    pdf.set_xy(x_inicio + 5, y_inicio + 10)
    pdf.cell(100, 8, f"Tracking : ___________________", ln=0)
    pdf.cell(0, 8, f"Fecha : ______________", ln=1)

    # Sobreponer texto real
    pdf.set_xy(x_inicio + 35, y_inicio + 10)
    pdf.cell(0, 8, str(tracking))
    
    pdf.set_xy(x_inicio + 130, y_inicio + 10)
    pdf.cell(0, 8, datos['fecha'].strftime('%d/%m/%Y'))

    # Espacio
    pdf.ln(8)

    # Datos del remitente
    pdf.set_x(x_inicio + 5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Datos de remitente :", ln=1)

    pdf.set_font("Arial", size=12)
    pdf.ln(3)
    pdf.set_x(x_inicio + 5)
    pdf.cell(0, 8, "Nombre : _______________________", ln=1)
    pdf.set_xy(x_inicio + 35, pdf.get_y() - 8)
    pdf.cell(0, 8, datos['nombre_remitente'])

    pdf.ln(8)
    pdf.set_x(x_inicio + 5)
    pdf.cell(0, 10, "N° documento: ___________________", ln=1)
    pdf.set_xy(x_inicio + 40, pdf.get_y() - 9)
    pdf.cell(0, 8, datos['doc_remitente'])

    # Espacio
    pdf.ln(8)

    # Datos del destinatario
    pdf.set_x(x_inicio + 5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Datos del destinatario:", ln=1)

    pdf.set_font("Arial", size=12)
    pdf.ln(3)
    pdf.set_x(x_inicio + 5)
    pdf.cell(0, 8, "Nombre : _______________________", ln=1)
    pdf.set_xy(x_inicio + 35, pdf.get_y() - 8)
    pdf.cell(0, 8, datos['nom_destinatario'])

    pdf.ln(8)
    pdf.set_x(x_inicio + 5)
    pdf.cell(0, 8, "N° documento: ___________________", ln=1)
    pdf.set_xy(x_inicio + 45, pdf.get_y() - 8)
    pdf.cell(0, 8, datos['doc_destinatario'])

    # Línea horizontal inferior (guía visual)
    pdf.line(x_inicio, y_inicio + alto_total, x_inicio + ancho_total, y_inicio + alto_total)

    # Origen
    pdf.set_xy(x_inicio, y_inicio + alto_total + 10)
    pdf.cell(0, 8, "Origen: _____________________________________________________________", ln=1)
    pdf.set_xy(x_inicio + 25, pdf.get_y() - 8)
    pdf.cell(0, 8, datos['origen'])

    # Espacio
    pdf.ln(5)

    # Destino
    pdf.set_x(x_inicio)
    pdf.cell(0, 8, "Destino: ____________________________________________________________", ln=1)
    pdf.set_xy(x_inicio + 27, pdf.get_y() - 8)
    pdf.cell(0, 8, datos['destino'])

    # Agregar el QR (dentro del rectángulo)
    pdf.image(ruta_qr, x=x_inicio + ancho_total - 100, y=y_inicio + 25, w=90)

    # Guardar PDF
    pdf.output(ruta_pdf)

    # Eliminar QR temporal
    if os.path.exists(ruta_qr):
        os.remove(ruta_qr)
