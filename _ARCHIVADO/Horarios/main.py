from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
from datetime import datetime, date
# from flask_jwt import JWT, jwt_required, current_identity
# import uuid
# from functools import wraps
import hashlib
import base64
import controladores.controlador_horario as controlador_horario
import controladores.controlador_curso as controlador_curso
import controladores.controlador_color as controlador_color
import controladores.controlador_matricula as controlador_matricula
import controladores.controlador_alumno as controlador_alumno

app = Flask(__name__, template_folder='templates')

USUARIO_ID = 1
HORAS = (7,8,9,10,11,12,13,14,15,16,17,18,19,20,21)
DIAS = (0,1,2,3,4,5,6)

def generalPage(page):
    return "general_pages/"+page


def adminPage(page):
    return "admin_pages/"+page


def formPage(page):
    return "form_pages/"+page


def crudPage(page):
    return "crud_pages/"+page



@app.context_processor
def inject_globals():
    matriculas = controlador_matricula.obtener_matriculas_alumno(USUARIO_ID)
    horas = HORAS
    dias = DIAS
    return dict(
        horas = horas,
        dias = dias,
        matriculas = matriculas
    )


@app.route("/")
def index():
    return render_template(generalPage("index.html"))



@app.route("/prerrequisitos")
def prerrequisitos():
    cursos = controlador_curso.obtener_cursos()
    return render_template(generalPage("prerrequisitos_cursos.html") , cursos = cursos)



@app.route("/horario")
def horario():
    horarios = controlador_horario.obtener_horarios()
    return render_template(generalPage("horario.html") , horarios = horarios )



@app.route("/semestre=<semestre>")
def semestre(semestre):
    horarios = controlador_horario.obtener_horario_semestre(semestre)
    return render_template(generalPage("horario.html") , horarios = horarios )




@app.route("/horario_matricula=<int:mat_id>")
def horario_matricula(mat_id):
    horarios = controlador_horario.obtener_horario_matricula(mat_id)
    return render_template(generalPage("horario.html") , horarios = horarios )



@app.route("/cursos_alumno=<int:alu_id>")
def cursos_alumno(alu_id):
    cursos = controlador_alumno.obtener_prerrequisitos(alu_id)
    return render_template(generalPage("cursos.html") , cursos = cursos )











@app.route("/listado_curso")
def listado_curso():
    cursos = controlador_curso.obtener_listado_cursos()
    colores = controlador_color.obtener_color()
    return render_template(crudPage("listado_curso.html") , cursos = cursos , colores = colores)


@app.route("/buscar_curso")
def buscar_curso():
    return render_template(crudPage("listado_curso.html"))


@app.route("/guardar_curso", methods=["POST"])
def guardar_curso():
    nombre = request.form["nombre"]
    abrev = request.form["abrev"]
    cred = request.form["cred"]
    ciclo = request.form["ciclo"]
    colorid = request.form["colorid"]
    controlador_curso.insertar_curso(nombre,abrev,cred,ciclo,colorid)
    return redirect("/listado_curso")
    

@app.route("/listado_color")
def listado_color():
    colores = controlador_color.obtener_listado_colores()
    return render_template(crudPage("listado_color.html") , colores = colores)


@app.route("/guardar_color", methods=["POST"])
def guardar_color():
    nombre = request.form["nombre"]
    fondo = request.form["fondo"]
    texto = request.form["texto"]
    controlador_color.insertar_color(nombre,fondo,texto)
    return redirect("/listado_color")
    










if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
