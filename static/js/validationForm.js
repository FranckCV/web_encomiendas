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
    alfanumerico: {
        regex: /^[a-zA-Z0-9]+$/, // sin espacios
        mensaje: "Solo letras y números"
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
    checkbox: {
        mensaje: "Este campo debe estar marcado"
    },
    select: {
        mensaje: "Debe seleccionar una opción válida"
    },
    decimal2: {
        regex: /^\d+(\.\d{1,2})?$/,
        mensaje: "Máximo 2 decimales"
    },
    decimal6: {
        regex: /^\d+(\.\d{1,6})?$/,
        mensaje: "Máximo 6 decimales"
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

};

function configurarValidacion({ tipo, selector, id }) {
    const elementos = document.querySelectorAll(`${selector}#${id}`);

    elementos.forEach(el => {
        el.dataset.tipo = tipo;

        el.addEventListener("input", () => {
            const tipos = tipo.split(",");
            let valido = true;
            for (let t of tipos) {
                const matchId = t.startsWith("match:") ? t.split(":")[1] : null;
                if (!validarCampo(el, t, matchId)) valido = false;
            }
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

    // Checkbox
    if (tipo === "checkbox") {
        if (!el.checked) {
            el.classList.add("input-error");
            msgError.textContent = tiposValidacion[tipo].mensaje;
            msgError.style.display = "block";
            return false;
        } else {
            el.classList.remove("input-error");
            msgError.textContent = "";
            msgError.style.display = "none";
            return true;
        }
    }

    // Select
    if (tipo === "select") {
        const val = el.value;
        const isInvalid = val === "" || val === "-1" || el.options[el.selectedIndex]?.disabled;
        if (isInvalid) {
            el.classList.add("input-error");
            msgError.textContent = tiposValidacion[tipo].mensaje;
            msgError.style.display = "block";
            return false;
        } else {
            el.classList.remove("input-error");
            msgError.textContent = "";
            msgError.style.display = "none";
            return true;
        }
    }

    // match: campo igual a otro
    if (tipo.startsWith("match:")) {
        const otroCampo = document.querySelector(`#${matchId}`);
        const mismoValor = otroCampo && el.value === otroCampo.value;
        if (!mismoValor) {
            el.classList.add("input-error");
            msgError.textContent = tiposValidacion["match"].mensaje;
            msgError.style.display = "block";
            return false;
        } else {
            el.classList.remove("input-error");
            msgError.textContent = "";
            msgError.style.display = "none";
            return true;
        }
    }

    // Validaciones min / max dinámicas
    if (tipo.startsWith("min:")) {
        const min = parseInt(tipo.split(":")[1]);
        if (el.value.length < min) {
            el.classList.add("input-error");
            msgError.textContent = `Mínimo ${min} caracteres`;
            msgError.style.display = "block";
            return false;
        } else {
            el.classList.remove("input-error");
            msgError.textContent = "";
            msgError.style.display = "none";
            return true;
        }
    }

    if (tipo.startsWith("max:")) {
        const max = parseInt(tipo.split(":")[1]);
        if (el.value.length > max) {
            el.classList.add("input-error");
            msgError.textContent = `Máximo ${max} caracteres`;
            msgError.style.display = "block";
            return false;
        } else {
            el.classList.remove("input-error");
            msgError.textContent = "";
            msgError.style.display = "none";
            return true;
        }
    }


    // Validación normal con regex
    const val = el.value.trim();
    const tipoBase = tipo.includes(":") ? tipo.split(":")[0] : tipo;
    const { regex, mensaje } = tiposValidacion[tipoBase] || {};

    if (!regex || val === "" || !regex.test(val)) {
        el.classList.add("input-error");
        msgError.textContent = mensaje || "Campo inválido";
        msgError.style.display = "block";
        return false;
    } else {
        el.classList.remove("input-error");
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
