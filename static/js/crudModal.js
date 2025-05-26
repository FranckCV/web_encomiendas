function openModal(idmodal) {
    const elementModal = '#' + idmodal + '.space_modal';
    const overlay = document.getElementById('overlayModal');
    const enlargedModal = document.getElementById('enlargedModal');
    const modalDiv = document.querySelector(elementModal);

    enlargedModal.innerHTML = modalDiv.outerHTML;
    const modalClonado = enlargedModal.querySelector(elementModal);

    modalClonado.style.display = 'flex';
    overlay.style.display = 'flex';

    // Llenar selects dinámicamente al abrir el modal
    llenarSelectsDelModal(modalClonado);
}

function closeModal() {
    const overlay = document.getElementById('overlayModal');
    const enlargedModal = document.getElementById('enlargedModal');

    // Limpiar selects antes de cerrar (por si queda en memoria)
    const modalAbierto = enlargedModal.querySelector('.space_modal');
    if (modalAbierto) {
        limpiarSelectsDelModal(modalAbierto);
    }

    overlay.style.display = 'none';
    enlargedModal.innerHTML = ''; // Limpiar modal para evitar acumulación de nodos
}

document.querySelectorAll('.clickable-modal').forEach(button => {
    button.addEventListener('click', function (event) {
        openModal(button.id);
    });
});



document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll(".form_fields");
    forms.forEach(form => {
        const inputs = form.querySelectorAll(".form_field:not(.form_textarea)");
        const cantidad = inputs.length;

        let columnas = 1;
        if (cantidad <= 2) columnas = cantidad;
        else if (cantidad === 4) columnas = 2;
        else columnas = 3;

        form.style.gridTemplateColumns = `repeat(${columnas}, 1fr)`;

    });

});




function llenarSelectsDelModal(modal) {
    const selects = modal.querySelectorAll("select[data-select]");
    selects.forEach(select => {
        const key = select.dataset.select;
        const opciones = SELECT_OPTIONS[key] || [];

        // Si ya está lleno, no lo volvemos a llenar
        if (select.options.length > 1) return;

        opciones.forEach(op => {
            const option = document.createElement("option");
            option.value = op.value;
            option.textContent = op.label;

            const valorSeleccionado = select.getAttribute("data-select-value");
            if (valorSeleccionado !== null && valorSeleccionado == op.value) {
                option.selected = true;
            }

            select.appendChild(option);
        });

        // Si es modo insert y no hay valor, selecciona el placeholder
        if (select.dataset.modo === "insert") {
            select.value = "-1";
        }
    });
}

function limpiarSelectsDelModal(modal) {
    const selects = modal.querySelectorAll("select[data-select]");
    selects.forEach(select => {
        select.innerHTML = ""; // Limpia todo
    });
}
























document.addEventListener('input', (e) => {
    if (e.target.matches('.form_icon input[type="text"]:not(:disabled)')) {
        const input = e.target;
        const block_icon = input.closest('.form_icon').querySelector('i');

        const valor = input.value.trim();
        const claseIcono = valor.split(' ').find(clase => clase.startsWith('fa-') && clase !== 'fa-solid');
        if (claseIcono && block_icon) {
            block_icon.className = `fa-solid ${claseIcono}`;
        }
    }
});


document.addEventListener('input', (e) => {
    if (e.target.matches('.input_color_sync')) {
        const input = e.target;
        const name = input.dataset.name;
        const value = input.value;

        // Buscar los otros inputs con el mismo data-name, pero que no sean el que disparó el evento
        const siblings = document.querySelectorAll(`.input_color_sync[data-name="${name}"]`);
        siblings.forEach(el => {
            if (el !== input) {
                el.value = value;
            }
        });
    }
});



