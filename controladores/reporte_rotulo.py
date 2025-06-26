from fpdf import FPDF
import os
import qrcode

class RotuloPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format=(100, 150))  # etiqueta tamaño 100x150 mm

    def header(self):
        self.set_font("Helvetica", "B", 13)
        self.cell(0, 10, "RÓTULO DE ENCOMIENDA", ln=True, align="C")
        self.ln(3)

    def cuerpo(self, data):
        self.set_font("Helvetica", "", 10)

        self._fila_dato("Tracking:", data.get("tracking", ""))
        self._fila_dato("Sucursal Origen:", data.get("sucursal_origen", ""))
        self._fila_dato("Sucursal Destino:", data.get("sucursal_destino", ""))

        self.ln(5)

    def _fila_dato(self, etiqueta, valor):
        self.set_font("Helvetica", "", 10)
        self.set_x(10)
        self.cell(35, 6, etiqueta, ln=0)
        self.set_font("Helvetica", "B", 10)
        self.multi_cell(0, 6, valor)

    def agregar_qr(self, texto, ruta_qr):
        qr = qrcode.make(texto)
        qr.save(ruta_qr)
        # Centrado horizontalmente
        x_centro = (100 - 40) / 2  # etiqueta es 100 mm de ancho
        self.image(ruta_qr, x=x_centro, y=self.get_y(), w=40)
        os.remove(ruta_qr)

def generar_rotulo_pdf(data, ruta_pdf="rotulo.pdf"):
    pdf = RotuloPDF()
    pdf.add_page()
    pdf.cuerpo(data)

    qr_texto = f"Tracking: {data.get('tracking', '')}\nDestino: {data.get('sucursal_destino', '')}"
    pdf.agregar_qr(qr_texto, "temp_qr.png")

    pdf.output(ruta_pdf)
