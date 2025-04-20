function openModal(idmodal) {
    const elementModal = '#' + idmodal + '.space_modal';
    const overlay = document.getElementById('overlayModal');
    const enlargedModal = document.getElementById('enlargedModal');
    const modalDiv = document.querySelector(elementModal);
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
        // openModal(event.target.id);
        openModal(button.id);
    });
});