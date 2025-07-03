// Validaciones generales para formularios
// Uso: configurarValidacion({ tipo: "email", selector: "input", id: "correo" });

const tiposValidacion = {
    email: {
        regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, // simple
        mensaje: "Correo inválido"
    },
    letras: {
        regex: /^[a-zA-Záéíóúñ\s]+$/, // letras con acentos y espacios
        mensaje: "Solo letras"
    },
    numeros: {
        regex: /^\d+$/,
        mensaje: "Solo números"
    },
    entero_positivo: {
        regex: /^[1-9]\d*$/,
        mensaje: "Solo números enteros positivos "
    },
    alfanumerico: {
        regex: /^[a-zA-Záéíóúñ0-9\s]+$/,
        mensaje: "Solo letras, números y espacios"
    },
    alfanumerico_simbolos: {
        regex: /^[a-zA-Záéíóúñ0-9\s.,\-_/()]+$/,
        mensaje: "Solo letras, números y algunos símbolos (.,-_/())"
    },
    texto_avanzado: {
        regex: /^[a-zA-Záéíóúñ0-9\s.,;:!¡¿?()@#&%$'"\-_/]+$/,
        mensaje: "Texto con caracteres inválidos"
    },
    url: {
        regex: /^(https?:\/\/)?([\w\-]+(\.[\w\-]+)+)(\/[\w\-.,@?^=%&:/~+#]*)?$/,
        mensaje: "URL inválida"
    },
    placa_peru: {
        regex: /^[A-Z0-9]{6}$/,
        mensaje: "Placa inválida (debe tener 6 caracteres alfanuméricos en mayúsculas)"
    },
    ip: {
        regex: /^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$/,
        mensaje: "IP inválida"
    },
    mayusculas: {
        regex: /^[A-Z]+$/,
        mensaje: "Solo letras mayúsculas"
    },
    minusculas: {
        regex: /^[a-z]+$/,
        mensaje: "Solo letras minúsculas"
    },
    dni: {
        regex: /^\d{8}$/,
        mensaje: "DNI debe tener 8 dígitos"
    },
    ruc: {
        regex: /^\d{11}$/,
        mensaje: "RUC debe tener 11 dígitos"
    },
    ce: {
        regex: /^[a-zA-Z0-9]{9,12}$/,
        mensaje: "Carnet de extranjería inválido"
    },
    pas: {
        regex: /^[a-zA-Z0-9]{6,12}$/,
        mensaje: "Pasaporte inválido"
    },
    tuc: {
        regex: /^[A-Z0-9]{6,12}$/,
        mensaje: "TUC inválido (6 a 12 caracteres alfanuméricos en mayúsculas, sin espacios)"
    },
    mtc: {
        regex: /^\d{6,10}$/,
        mensaje: "MTC inválido (debe estar 6 a 10 dígitos)"
    },
    checkbox: {
        mensaje: "Este campo debe estar marcado"
    },
    select: {
        mensaje: "Debe seleccionar una opción válida"
    },
    decimal2: {
        regex: /^(0|[1-9]\d*)(\.\d{1,2})?$/,
        mensaje: "Solo números positivos con máximo 2 decimales"
    },
    decimal6: {
        regex: /^(0|[1-9]\d*)(\.\d{1,6})?$/,
        mensaje: "Solo números positivos con máximo 6 decimales"
    },
    coordenada: {
        regex: /^-?(0|[1-9]\d*)(\.\d{1,10})?$/,
        mensaje: "Coordenada inválida (número con decimales, puede ser negativo)"
    },
    min8: {
        regex: /^.{8,}$/,
        mensaje: "Mínimo 8 caracteres"
    },
    match: {
        mensaje: "Los campos no coinciden"
    },
    telefono: {
        regex: /^\d{9,15}$/,  // entre 9 y 15 dígitos
        mensaje: "Teléfono inválido (mínimo 9 dígitos)"
    },
    hexadecimal: {
        regex: /^[0-9A-Fa-f]+$/,
        mensaje: "Valor hexadecimal inválido"
    },

};

function configurarValidacion({ tipo, selector, id }) {
    const elementos = document.querySelectorAll(`${selector}#${id}`);

    elementos.forEach(el => {
        el.dataset.tipo = tipo;

        el.addEventListener("input", () => {
            const tipoData = el.dataset.tipo;
            validarCampo(el, tipoData);
        });

        let msgError = el.parentElement.querySelector(".mensaje-error");
        if (!msgError) {
            msgError = document.createElement("p");
            msgError.className = "mensaje-error";
            el.parentElement.appendChild(msgError);
        }
    });
}



function validarCampo(el, tipo, matchId = null) {
    const msgError = el.parentElement.querySelector(".mensaje-error");
    const tipos = tipo.split(",");
    const errores = [];

    for (let t of tipos) {
        const matchIdLocal = t.startsWith("match:") ? t.split(":")[1] : null;

        // Checkbox
        if (t === "checkbox") {
            if (!el.checked) {
                errores.push(tiposValidacion[t].mensaje);
            }
            continue;
        }

        // Select
        if (t === "select") {
            const val = el.value;
            const isInvalid = val === "" || val === "-1" || el.options[el.selectedIndex]?.disabled;
            if (isInvalid) {
                errores.push(tiposValidacion[t].mensaje);
            }
            continue;
        }

        // match: campo igual a otro
        if (t.startsWith("match:")) {
            const otroCampo = document.querySelector(`#${matchIdLocal}`);
            if (!otroCampo || el.value !== otroCampo.value) {
                errores.push(tiposValidacion["match"].mensaje);
            }
            continue;
        }

        // min:X
        if (t.startsWith("min:")) {
            const min = parseInt(t.split(":")[1]);
            if (el.value.length < min) {
                errores.push(`Mínimo ${min} caracteres`);
            }
            continue;
        }      

        // max:X
        if (t.startsWith("max:")) {
            const max = parseInt(t.split(":")[1]);
            if (el.value.length > max) {
                errores.push(`Máximo ${max} caracteres`);
            }
            continue;
        }

        // min_val:X.Y
        if (t.startsWith("min_val:")) {
            const min = parseFloat(t.split(":")[1]);
            const valNum = parseFloat(el.value);
            if (!isNaN(valNum) && valNum < min) {
                errores.push(`El valor mínimo es ${min}`);
            }
            continue;
        }

        // max_val:X.Y
        if (t.startsWith("max_val:")) {
            const max = parseFloat(t.split(":")[1]);
            const valNum = parseFloat(el.value);
            if (!isNaN(valNum) && valNum > max) {
                errores.push(`El valor máximo es ${max}`);
            }
            continue;
        }


        // Validación normal con regex
        const val = el.value.trim();
        const tipoBase = t.includes(":") ? t.split(":")[0] : t;
        const { regex, mensaje } = tiposValidacion[tipoBase] || {};

        if (!el.required && val === "") {
            continue;
        }
        if (!regex || !regex.test(val)) {
            errores.push(mensaje || "Campo inválido");
        }
    }

    if (errores.length > 0) {
        el.classList.add("input-error");
        el.classList.remove("input-ok");
        msgError.textContent = errores.map(e => `${e}`).join(" / ");
        msgError.style.display = "block";
        return false;
    } else {
        el.classList.remove("input-error");
        el.classList.add("input-ok");
        msgError.textContent = "";
        msgError.style.display = "none";
        return true;
    }
}


function validarFormularioGlobal(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return;

    form.addEventListener("submit", e => {
        const inputs = form.querySelectorAll("input, select, textarea");
        let validos = true;

        inputs.forEach(input => {
            const tipo = input.dataset.tipo;
            if (tipo) {
                const tipos = tipo.split(",");
                for (let t of tipos) {
                    const matchId = t.startsWith("match:") ? t.split(":")[1] : null;
                    const esValido = validarCampo(input, t, matchId);
                    if (!esValido) validos = false;
                }
            }

        });

        if (!validos) {
            e.preventDefault();
        }
    });
}

function configurarValidacionDocumento(idSelect, idInput) {
    const select = document.getElementById(idSelect);
    const input = document.getElementById(idInput);

    if (!select || !input) return;

    select.addEventListener("change", () => {
        const siglas = select.options[select.selectedIndex]?.dataset?.siglas?.toLowerCase();

        if (!siglas) return;

        configurarValidacion({ tipo: siglas, selector: "input", id: idInput });
        input.dispatchEvent(new Event('input'));

    });
}


function configurarFiltroDocumentosPorTipoCliente(idSelectCliente, idSelectDocumento) {
    const selectCliente = document.getElementById(idSelectCliente);
    const selectDocumento = document.getElementById(idSelectDocumento);

    if (!selectCliente || !selectDocumento) return;

    // Clonamos las opciones originales
    const opcionesOriginales = Array.from(selectDocumento.options).filter(opt => opt.value !== "-1");

    function actualizarOpcionesDocumento() {
        const tipoClienteId = selectCliente.value;

        // Limpiamos todas las opciones excepto la "-1"
        selectDocumento.innerHTML = '<option value="-1" selected disabled>Tipo de Documento</option>';

        let nuevasOpciones;

        if (tipoClienteId === "2") {
            // Persona Jurídica: solo RUC
            nuevasOpciones = opcionesOriginales.filter(opt => opt.dataset.siglas === "RUC");
        } else {
            // Persona Natural: DNI, PAS, CE
            nuevasOpciones = opcionesOriginales.filter(opt => {
                const siglas = opt.dataset.siglas;
                return siglas === "DNI" || siglas === "PAS" || siglas === "CE";
            });
        }

        nuevasOpciones.forEach(opt => selectDocumento.appendChild(opt));
        selectDocumento.dispatchEvent(new Event('change'));
        
    }

    selectCliente.addEventListener("change", actualizarOpcionesDocumento);

    // Llamada inicial en caso venga precargado
    actualizarOpcionesDocumento();

}




// Ejemplo de uso:
// configurarValidacion({ tipo: "email", selector: "input", id: "correo" });
// configurarValidacion({ tipo: "dni", selector: "input", id: "num_documento" });
// validarFormularioGlobal("form");
