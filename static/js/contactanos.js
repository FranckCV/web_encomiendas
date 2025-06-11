document.addEventListener('DOMContentLoaded', () => {  
    // Selección de los elementos de los formularios
    const tipoDocumentoSelect = document.getElementById('tipoDocumento');
    const tipoClienteSelect = document.getElementById('tipoCliente');
    const sucursalSelect = document.getElementById('sucursal');
    const successMessage = document.getElementById('successMessage');
    const numeroDocumentoInput = document.getElementById('numeroDocumento');
    const telefonoInput = document.getElementById('telefono');
    const documentError = document.getElementById('documentError');
    const phoneError = document.getElementById('phoneError');

    // Función genérica para cargar opciones en un select
    function cargarOpciones(selectElement, datos, valorKey, textoKey) {
        selectElement.innerHTML = '<option value="" selected disabled>Selecciona una opción</option>';
        datos.forEach(item => {
            const option = document.createElement('option');
            option.value = item[valorKey];
            option.textContent = item[textoKey];
            selectElement.appendChild(option);
        });
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

    // Cargar tipos de documento desde backend para un tipo de cliente específico
    async function cargarTiposDocumento(tipoClienteId) {
        try {
            const res = await fetch(`/api/tipo_documento?tipo_cliente_id=${tipoClienteId}`);
            if (!res.ok) throw new Error('Error al cargar tipos de documento');
            const data = await res.json();
            cargarOpciones(tipoDocumentoSelect, data, 'id', 'nombre');
        } catch (error) {
            console.error(error);
            alert('No se pudieron cargar los tipos de documento.');
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

    // Validación del teléfono (máximo 9 dígitos)
    function validarTelefono(telefono) {
        const regex = /^[0-9]{9}$/;
        return regex.test(telefono);
    }

    // Validación del número de documento según tipo de documento
    function validarDocumento(numeroDocumento, tipoDocumentoId) {
        const longitudes = {
            1: 8,  // DNI
            2: 11, // RUC
            3: 20, // Carnet de Extranjería
            4: 20   // Pasaporte
        };
        return numeroDocumento.length === longitudes[tipoDocumentoId];
    }

    // Función para mostrar mensaje de éxito con animación
    function mostrarMensajeExito() {
        successMessage.style.display = 'flex';
        setTimeout(() => {
            successMessage.classList.add('show');
        }, 10);
        setTimeout(() => {
            successMessage.classList.remove('show');
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 600); // 600ms coincide con la duración de la transición CSS
        }, 5000);
    }

    // Manejo del cambio de tipo de cliente (actualiza los tipos de documento y limpia el número de documento)
    tipoClienteSelect.addEventListener('change', () => {
        const tipoClienteId = parseInt(tipoClienteSelect.value);
        // Si es Persona Jurídica, solo cargar RUC
        if (tipoClienteId === 2) {
            tipoDocumentoSelect.innerHTML = '<option value="2">Registro Único Contribuyente</option>';
        } else {
            cargarTiposDocumento(tipoClienteId);
        }

        // Limpiar el campo de número de documento y los errores cuando cambie el tipo de cliente
        numeroDocumentoInput.value = ''; // Limpiar el campo de número de documento
        numeroDocumentoInput.classList.remove('error', 'valid'); // Eliminar clases de error o validación
        documentError.style.display = 'none'; // Ocultar el mensaje de error
    });

    // Manejo del cambio de tipo de documento (limpia el número de documento y ajusta la longitud permitida)
    tipoDocumentoSelect.addEventListener('change', () => {
        const tipoDocumentoId = parseInt(tipoDocumentoSelect.value);
        // Limpiar el número de documento y el error al cambiar el tipo de documento
        numeroDocumentoInput.value = '';
        numeroDocumentoInput.classList.remove('error', 'valid');
        documentError.style.display = 'none';

        // Ajustar la longitud máxima permitida para el número de documento según el tipo de documento seleccionado
        if (tipoDocumentoId === 1) { // DNI
            numeroDocumentoInput.maxLength = 8;  // 8 dígitos
        } else if (tipoDocumentoId === 2) { // RUC
            numeroDocumentoInput.maxLength = 11; // 11 dígitos
        } else if (tipoDocumentoId === 3) { // Carnet de Extranjería
            numeroDocumentoInput.maxLength = 20; // 12 dígitos
        } else if (tipoDocumentoId ===4){
            numeroDocumentoInput.maxLength = 20 // 6 dígitos 
        }
    });

    // Inicializar carga de selects
    cargarTiposCliente();
    cargarSucursales();

    // Validaciones mientras el usuario escribe en el campo de número de teléfono (solo números)
    telefonoInput.addEventListener('input', () => {
        // Permitir solo números
        telefonoInput.value = telefonoInput.value.replace(/[^0-9]/g, '');

        const telefono = telefonoInput.value.trim();
        if (!validarTelefono(telefono)) {
            telefonoInput.maxLength = 9
            telefonoInput.classList.add('error');
            telefonoInput.classList.remove('valid');
            phoneError.style.display = 'block';
        } else {
            telefonoInput.classList.remove('error');
            telefonoInput.classList.add('valid');
            phoneError.style.display = 'none';
        }
    });

    // Validaciones mientras el usuario escribe en el campo de número de documento (solo números)
    numeroDocumentoInput.addEventListener('input', () => {
        // Permitir solo números
        numeroDocumentoInput.value = numeroDocumentoInput.value.replace(/[^0-9]/g, '');

        const numeroDocumento = numeroDocumentoInput.value.trim();
        const tipoDocumentoId = parseInt(tipoDocumentoSelect.value);

        // Validar longitud máxima de número de documento según tipo de documento
        if (!validarDocumento(numeroDocumento, tipoDocumentoId)) {
            numeroDocumentoInput.classList.add('error');
            numeroDocumentoInput.classList.remove('valid');
            documentError.style.display = 'block';
        } else {
            numeroDocumentoInput.classList.remove('error');
            numeroDocumentoInput.classList.add('valid');
            documentError.style.display = 'none';
        }
    });

    // Manejo del envío del formulario
    const form = document.getElementById('contactForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const numeroDocumento = numeroDocumentoInput.value.trim();
        const telefono = telefonoInput.value.trim();
        const tipoDocumentoId = parseInt(tipoDocumentoSelect.value);

        // Recopilación de datos del formulario
        const data = {
            nombreCompleto: form.nombreCompleto.value.trim(),
            numeroDocumento,
            email: form.email.value.trim(),
            telefono,
            mensaje: form.mensaje.value.trim(),
            tipoDocumentoId,
            tipoClienteId: parseInt(form.tipoCliente.value),
            sucursalId: parseInt(form.sucursal.value)
        };

        // Validación final antes de enviar
        if (!validarTelefono(telefono)) {
            telefonoInput.classList.add('error');
            phoneError.style.display = 'block';
            return;
        } else {
            telefonoInput.classList.remove('error');
            telefonoInput.classList.add('valid');
            phoneError.style.display = 'none';
        }

        if (!validarDocumento(numeroDocumento, tipoDocumentoId)) {
            numeroDocumentoInput.classList.add('error');
            documentError.style.display = 'block';
            return;
        } else {
            numeroDocumentoInput.classList.remove('error');
            numeroDocumentoInput.classList.add('valid');
            documentError.style.display = 'none';
        }

        try {
            const response = await fetch('/enviar-formulario', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();

            if (result.success) {
                mostrarMensajeExito();
                e.target.reset();

                // Limpiar los campos de validación (volver al color inicial)
                numeroDocumentoInput.classList.remove('valid', 'error');
                telefonoInput.classList.remove('valid', 'error');
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error(error);
            alert('Error enviando el formulario.');
        }
    });
});
