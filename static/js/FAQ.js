document.addEventListener('DOMContentLoaded', function() {
    // Inicializar acordeón
    initAccordion();
    
    // Inicializar sistema de valoración
    initRating();
});

// Función para inicializar el acordeón
function initAccordion() {
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    
    accordionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            toggleAccordion(this);
        });
    });
}

// Función para alternar el estado del acordeón
function toggleAccordion(header) {
    // Verificar si este elemento ya está activo
    const isActive = header.classList.contains('active');
    
    // Cerrar todos los acordeones abiertos
    const allHeaders = document.querySelectorAll('.accordion-header');
    const allContents = document.querySelectorAll('.accordion-content');
    
    allHeaders.forEach(h => h.classList.remove('active'));
    allContents.forEach(c => c.classList.remove('show'));
    
    // Si el elemento clickeado no estaba activo, ábrelo
    if (!isActive) {
        const content = header.nextElementSibling;
        header.classList.add('active');
        content.classList.add('show'); 
    }
}

// Función para inicializar el sistema de valoración
function initRating() {
    const ratingOptions = document.querySelectorAll('.rating-option');
    
    ratingOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Quitar la selección de todas las opciones
            ratingOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Añadir la clase seleccionada a la opción clickeada
            this.classList.add('selected');
            
            // Obtener el valor de la valoración
            const rating = this.getAttribute('data-rating');
            
            // Enviar la valoración (puedes implementar esto según tu sistema)
            sendRating(rating);
        });
    });
}

// Función para enviar la valoración
function sendRating(rating) {
    console.log('Valoración enviada:', rating);
    
    // Aquí puedes implementar una llamada AJAX para enviar la valoración al servidor
    // Por ejemplo:
    /*
    fetch('/api/submit-rating', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rating: rating })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Éxito:', data);
        // Mostrar un mensaje de agradecimiento
        showThankYouMessage();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    */
    
    // Para propósitos de demostración, simplemente mostramos un mensaje de agradecimiento
    setTimeout(showThankYouMessage, 500);
}

// Función para mostrar un mensaje de agradecimiento después de la valoración
function showThankYouMessage() {
    const ratingSection = document.querySelector('.rating-section');
    const originalContent = ratingSection.innerHTML;
    
    // Guardar el contenido original para restaurarlo más tarde si es necesario
    ratingSection.setAttribute('data-original-content', originalContent);
    
    // Reemplazar con mensaje de agradecimiento
    ratingSection.innerHTML = `
        <div class="thank-you-message">
            <i class="fa-solid fa-circle-check" style="font-size: 48px; color: #27ae60; margin-bottom: 15px;"></i>
            <h3>¡Gracias por tu valoración!</h3>
            <p>Tu opinión nos ayuda a mejorar nuestros servicios.</p>
        </div>
    `;
    
    // Aplicar estilo al mensaje de agradecimiento
    const thankYouMessage = ratingSection.querySelector('.thank-you-message');
    thankYouMessage.style.textAlign = 'center';
    thankYouMessage.style.padding = '30px 0';
}

// Función para mostrar contenido dinámicamente (si es necesario en el futuro)
function loadDynamicContent(url, targetSelector) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            const targetElement = document.querySelector(targetSelector);
            if (targetElement) {
                targetElement.innerHTML = data;
            }
        })
        .catch(error => {
            console.error('Error al cargar contenido:', error);
        });
}