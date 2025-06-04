document.getElementById('contactForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        nombreCompleto: document.getElementById('nombreCompleto').value,
        numeroDocumento: document.getElementById('numeroDocumento').value,
        email: document.getElementById('email').value,
        telefono: document.getElementById('telefono').value,
        mensaje: document.getElementById('mensaje').value || '',
        tipoDocumentoId: document.getElementById('tipoDocumento')?.value || null,
        tipoClienteId: document.getElementById('tipoCliente')?.value,
        sucursalId: document.getElementById('sucursal')?.value,
    };

    try {
        const response = await fetch('/enviar-formulario', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        if (result.success) {
            // Mostrar el mensaje de éxito
            const successMessage = document.getElementById('successMessage');
            successMessage.style.display = 'block';
            successMessage.classList.add('show'); // Animar la aparición

            // Ocultar el mensaje después de 5 segundos
            setTimeout(() => {
                successMessage.classList.remove('show');
                successMessage.style.display = 'none'; // Ocultar el mensaje después de la animación
            }, 5000);

            // Resetear el formulario después de mostrar el mensaje
            e.target.reset();
        } else {
            alert('Ocurrió un error al enviar el formulario.');
        }
    } catch (error) {
        console.error(error);
        alert('Error enviando el formulario.');
    }
});
