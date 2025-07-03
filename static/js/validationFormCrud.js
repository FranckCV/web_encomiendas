// === VALIDACIÓN AUTOMÁTICA EN MODALES CRUD BASADA EN data-tipo ===

// Detecta inserción de modal en #enlargedModal y aplica validaciones automáticas
const observerCrudModal = new MutationObserver(() => {
    configurarValidacionEnModalClonado();
});

const enlargedModalContainer = document.getElementById('enlargedModal');
if (enlargedModalContainer) {
    observerCrudModal.observe(enlargedModalContainer, { childList: true, subtree: true });
}

function configurarValidacionUniversalEnContenedor(contenedor) {
    if (!contenedor) return;
    const campos = contenedor.querySelectorAll("input, select, textarea");

    campos.forEach(campo => {
        if (!campo.id) return;
        const tipo = campo.dataset.tipo; // ✅ usa directamente el data-tipo renderizado desde CONTROLADORES
        if (tipo) {
            configurarValidacion({
                tipo: tipo,
                selector: campo.tagName.toLowerCase(),
                id: campo.id
            });
        }
    });
}

function validarFormularioDirecto(form) {
    if (!form) return;

    form.addEventListener("submit", e => {
        const inputs = form.querySelectorAll("input, select:not(.filterSelect), textarea");
        let validos = true;

        inputs.forEach(input => {
            const tipo = input.dataset.tipo;
            if (tipo) {
                const tipos = tipo.split(",");
                tipos.forEach(t => {
                    const matchId = t.startsWith("match:") ? t.split(":")[1] : null;
                    if (!validarCampo(input, t, matchId)) validos = false;
                });
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
        validarFormularioDirecto(form);
    }

    modalClonado.dataset.validado = "1";
}
