// ==============================
// VALIDACIÓN AUTOMÁTICA PARA MODALES CRUD CLONADOS
// ==============================

// Configuración base de campos automáticos
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
                console.log('tipo -> ',validacionAutomaticaCampos[key]);
                console.log('selector -> ',  campo.tagName.toLowerCase());
                console.log('id -> ', campo.id );
                break; // Evita duplicidades
            }
        }
    });
}

// Hook seguro para modales clonados por openModal
function configurarValidacionEnModalClonado() {
    const enlargedModal = document.getElementById('enlargedModal');
    if (!enlargedModal) return;

    const modalClonado = enlargedModal.querySelector('.modal_crud_base');
    if (!modalClonado || modalClonado.dataset.validado === "1") return;

    // Aplica validaciones automáticas
    configurarValidacionUniversalEnContenedor(modalClonado);

    // Aplica validación global al formulario dentro del modal
    const form = modalClonado.querySelector('form');
    if (form && form.id) {
        validarFormularioGlobal(`#${modalClonado.id} form`);
    }

    // Marcar como validado para evitar duplicación
    modalClonado.dataset.validado = "1";
}

// Observer para detectar cuándo insertan el modal en #enlargedModal
const observerCrudModal = new MutationObserver(() => {
    configurarValidacionEnModalClonado();
});

const enlargedModalContainer = document.getElementById('enlargedModal');
if (enlargedModalContainer) {
    observerCrudModal.observe(enlargedModalContainer, { childList: true, subtree: true });
}

// Si necesitas forzar manualmente en algunos casos:
// configurarValidacionEnModalClonado();
