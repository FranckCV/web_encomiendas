document.addEventListener('DOMContentLoaded', () => {
    // Selección de los elementos de los formularios
    const tipoDocumentoSelect = document.getElementById('tipoDocumento');
    const tipoClienteSelect = document.getElementById('tipoCliente');
    const sucursalSelect = document.getElementById('sucursal');
    const successMessage = document.getElementById('successMessage');

    // Función genérica para cargar opciones en un select
    function cargarOpciones(selectElement, datos, valorKey, textoKey) {
        selectElement.innerHTML = '<option value="" selected disabled>-</option>';
        datos.forEach(item => {
            const option = document.createElement('option');
            option.value = item[valorKey];
            option.textContent = item[textoKey];
            selectElement.appendChild(option);
        });
    }

    // Cargar tipos de documento desde backend
    async function cargarTiposDocumento() {
        try {
            const res = await fetch('/api/tipo_documento');
            if (!res.ok) throw new Error('Error al cargar tipos de documento');
            const data = await res.json();
            cargarOpciones(tipoDocumentoSelect, data, 'id', 'nombre');
        } catch (error) {
            console.error(error);
            alert('No se pudieron cargar los tipos de documento.');
        }
    }

    // Cargar tipos de cliente desde backend
    async function cargarTiposCliente() {
        try {
            const res = await fetch('/api/tipo_cliente');
            if (!res.ok) throw new Error('Error al cargar tipos de cliente');
            const data = await res.json();
            cargarOpciones(tipoClienteSelect, data, 'id', 'nombre');
        } catch (error) {
            console.error(error);
            alert('No se pudieron cargar los tipos de cliente.');
        }
    }

    // Cargar sucursales desde backend
    async function cargarSucursales() {
        try {
            const res = await fetch('/api/sucursales_simple');
            if (!res.ok) throw new Error('Error al cargar sucursales');
            const data = await res.json();
            cargarOpciones(sucursalSelect, data, 'id', 'direccion');
        } catch (error) {
            console.error(error);
            alert('No se pudieron cargar las sucursales.');
        }
    }

    // Función para mostrar mensaje de éxito con animación
    function mostrarMensajeExito() {
        // Mostrar el mensaje
        successMessage.style.display = 'flex';

        // Pequeño delay para permitir que el display tome efecto
        setTimeout(() => {
            successMessage.classList.add('show');
        }, 10);

        // Ocultar el mensaje después de 5 segundos
        setTimeout(() => {
            successMessage.classList.remove('show');

            // Ocultar completamente después de que termine la animación
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 600); // 600ms coincide con la duración de la transición CSS
        }, 5000);
    }

    // Inicializar carga de selects
    cargarTiposDocumento();
    cargarTiposCliente();
    cargarSucursales();

    // Manejo del envío del formulario
    const form = document.getElementById('contactForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Recopilación de datos del formulario
        const data = {
            nombreCompleto: form.nombreCompleto.value.trim(),
            numeroDocumento: form.numeroDocumento.value.trim(),
            email: form.email.value.trim(),
            telefono: form.telefono.value.trim(),
            mensaje: form.mensaje.value.trim(),
            tipoDocumentoId: parseInt(form.tipoDocumento.value),
            tipoClienteId: parseInt(form.tipoCliente.value),
            sucursalId: parseInt(form.sucursal.value)
        };

        try {
            // Enviar los datos al backend
            const response = await fetch('/enviar-formulario', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();

            // Si la respuesta es exitosa
            if (result.success) {
                // Mostrar el mensaje de éxito con animación
                mostrarMensajeExito();

                // Resetear el formulario
                e.target.reset();
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error(error);
            alert('Error enviando el formulario.');
        }
    });
});