document.addEventListener('DOMContentLoaded', function() {
    // Inicializar validación del formulario
    initFormValidation();
});

/**
 * Inicializa la validación del formulario de contacto
 */
function initFormValidation() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        // Validación al enviar el formulario
        contactForm.addEventListener('submit', function(event) {
            if (!validateForm()) {
                event.preventDefault();
                showErrorMessage('Por favor, completa todos los campos requeridos.');
            }
        });

        // Validación en tiempo real para los campos
        const formInputs = contactForm.querySelectorAll('input, select');
        formInputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('change', function() {
                validateField(this);
            });
        });
    }
}

/**
 * Valida todos los campos del formulario
 * @returns {boolean} True si todos los campos son válidos, false en caso contrario
 */
function validateForm() {
    let isValid = true;
    const requiredFields = document.querySelectorAll('#contactForm [required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Valida un campo específico
 * @param {HTMLElement} field - El campo a validar
 * @returns {boolean} True si el campo es válido, false en caso contrario
 */
function validateField(field) {
    let isValid = true;
    
    // Eliminar clases de error previas
    field.classList.remove('error');
    
    // Validación según el tipo de campo
    if (field.hasAttribute('required') && !field.value.trim()) {
        isValid = false;
    } else if (field.type === 'email' && field.value.trim()) {
        isValid = validateEmail(field.value);
    } else if (field.id === 'telefono' && field.value.trim()) {
        isValid = validatePhone(field.value);
    } else if (field.type === 'checkbox' && field.hasAttribute('required')) {
        isValid = field.checked;
    }
    
    // Mostrar error si no es válido
    if (!isValid) {
        field.classList.add('error');
    }
    
    return isValid;
}

/**
 * Valida un formato de email
 * @param {string} email - El email a validar
 * @returns {boolean} True si el formato es válido
 */
function validateEmail(email) {
    const re = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
    return re.test(String(email).toLowerCase());
}

/**
 * Valida un formato de teléfono (básico)
 * @param {string} phone - El teléfono a validar
 * @returns {boolean} True si el formato es válido
 */
function validatePhone(phone) {
    // Permitir solo números y algunos caracteres especiales
    const re = /^[0-9+\-\s()]{7,15}$/;
    return re.test(phone);
}

/**
 * Muestra un mensaje de error
 * @param {string} message - El mensaje de error a mostrar
 */
function showErrorMessage(message) {
    alert(message);
    
    // Alternativa: mostrar un mensaje en la página
    // const errorDiv = document.createElement('div');
    // errorDiv.className = 'error-message';
    // errorDiv.textContent = message;
    
    // const form = document.getElementById('contactForm');
    // form.prepend(errorDiv);
    
    // setTimeout(() => {
    //     errorDiv.remove();
    // }, 5000);
}