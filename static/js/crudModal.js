function openModal(idmodal) {
    const elementModal = '#' + idmodal + '.space_modal';
    const overlay = document.getElementById('overlayModal');
    const enlargedModal = document.getElementById('enlargedModal');
    const modalDiv = document.querySelector(elementModal);
    // console.log(enlargedModal);
    // console.log(modalDiv);

    enlargedModal.innerHTML = modalDiv.outerHTML;
    enlargedModal.querySelector(elementModal).style.display = 'flex';
    overlay.style.display = 'flex';
}

function closeModal() {
    const overlay = document.getElementById('overlayModal');
    overlay.style.display = 'none';
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
