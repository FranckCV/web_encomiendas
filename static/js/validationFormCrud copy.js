
const validacionAutomaticaCampos = {
    descripcion: "alfanumerico",
    direccion: "alfanumerico",
    comentario: "alfanumerico",
    referencia: "alfanumerico",
    nombre: "letras",
    apellidos: "letras",
    correo: "email",
    email: "email",
    telefono: "telefono",
    celular: "telefono",
    dni: "dni",
    ruc: "ruc",
    ce: "ce",
    pas: "pas",
    capacidad: "decimal2",
    volumen: "decimal2",
    cantidad: "numeros"
    // Añade más según tu flujo
};

// Lógica para aplicar validaciones en un contenedor específico
function configurarValidacionUniversalEnContenedor(contenedor) {
    if (!contenedor) return;

    const campos = contenedor.querySelectorAll("input, select, textarea");

    campos.forEach(campo => {
        if (!campo.id) return;
        const id = campo.id?.toLowerCase() || "";
        const name = campo.name?.toLowerCase() || "";
        for (let key in validacionAutomaticaCampos) {
            if (id.includes(key) || name.includes(key)) {
                configurarValidacion({
                    tipo: validacionAutomaticaCampos[key],
                    selector: campo.tagName.toLowerCase(),
                    id: campo.id
                });
                // console.log('tipo -> ',validacionAutomaticaCampos[key]);
                // console.log('selector -> ',  campo.tagName.toLowerCase());
                // console.log('id -> ', campo.id );
                break; // Evita duplicidades
            }
        }
    });
}

// Observer para detectar cuándo insertan el modal en #enlargedModal
const observerCrudModal = new MutationObserver(() => {
    configurarValidacionEnModalClonado();
});

const enlargedModalContainer = document.getElementById('enlargedModal');
if (enlargedModalContainer) {
    observerCrudModal.observe(enlargedModalContainer, { childList: true, subtree: true });
}

function validarFormularioDirecto(form) {
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
            e.stopPropagation();
            alert("Corrige los campos marcados antes de enviar.");
        }
    });
}

function configurarValidacionEnModalClonado() {
    const enlargedModal = document.getElementById('enlargedModal');
    if (!enlargedModal) return;

    const modalClonado = enlargedModal.querySelector('.modal_crud_base');
    if (!modalClonado || modalClonado.dataset.validado === "1") return;

    configurarValidacionUniversalEnContenedor(modalClonado);

    const form = modalClonado.querySelector('form');
    if (form) {
        validarFormularioDirecto(form); // ✅ Asegura aplicar validación real
    }

    modalClonado.dataset.validado = "1";
}
