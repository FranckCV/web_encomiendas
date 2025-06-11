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

};

function configurarValidacion({ tipo, selector, id }) {
    const elementos = document.querySelectorAll(`${selector}#${id}`);

    elementos.forEach(el => {
        el.dataset.tipo = tipo;

        el.addEventListener("input", () => validarCampo(el, tipo));

        // Crear mensaje de error si no existe
        let msgError = el.parentElement.querySelector(".mensaje-error");
        if (!msgError) {
            msgError = document.createElement("p");
            msgError.className = "mensaje-error";
            el.parentElement.appendChild(msgError);
        }
    });
}

function validarCampo(el, tipo) {
    const msgError = el.parentElement.querySelector(".mensaje-error");

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

    // Validación normal (input, textarea)
    const val = el.value.trim();
    const { regex, mensaje } = tiposValidacion[tipo];

    if (val === "" || !regex.test(val)) {
        el.classList.add("input-error");
        msgError.textContent = mensaje;
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
            if (tipo && tiposValidacion[tipo]) {
                const esValido = validarCampo(input, tipo);
                if (!esValido) validos = false;
            }
        });

        if (!validos) {
            e.preventDefault();
        }
    });
}



// Ejemplo de uso:
// configurarValidacion({ tipo: "email", selector: "input", id: "correo" });
// configurarValidacion({ tipo: "dni", selector: "input", id: "num_documento" });
// validarFormularioGlobal("form");
