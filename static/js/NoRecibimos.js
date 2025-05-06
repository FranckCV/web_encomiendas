// JavaScript para la página "No recibimos"
document.addEventListener('DOMContentLoaded', function() {
    // Añadir efectos de hover a las tarjetas
    const productoCards = document.querySelectorAll('.producto-card');
    
    productoCards.forEach(card => {
        // Efecto de hover animado
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
        
        // Añadir efecto de clic para mostrar más información
        card.addEventListener('click', function() {
            // Obtener el título y descripción del producto
            const titulo = this.querySelector('.producto-titulo').textContent;
            const descripcion = this.querySelector('.producto-descripcion').textContent;
            
            // Mostrar un cuadro de diálogo con más información
            mostrarInformacionAdicional(titulo, descripcion);
        });
    });
    
    // Función para mostrar más información sobre el producto
    function mostrarInformacionAdicional(titulo, descripcion) {
        // Verificar si ya existe un modal y eliminarlo
        const modalExistente = document.getElementById('modal-info');
        if (modalExistente) {
            modalExistente.remove();
        }
        
        // Crear el modal
        const modal = document.createElement('div');
        modal.id = 'modal-info';
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        modal.style.display = 'flex';
        modal.style.justifyContent = 'center';
        modal.style.alignItems = 'center';
        modal.style.zIndex = '1000';
        
        // Crear el contenido del modal
        const modalContent = document.createElement('div');
        modalContent.style.backgroundColor = '#fff';
        modalContent.style.padding = '30px';
        modalContent.style.borderRadius = '8px';
        modalContent.style.maxWidth = '500px';
        modalContent.style.width = '80%';
        modalContent.style.position = 'relative';
        
        // Botón de cerrar
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.position = 'absolute';
        closeBtn.style.top = '10px';
        closeBtn.style.right = '10px';
        closeBtn.style.border = 'none';
        closeBtn.style.background = 'none';
        closeBtn.style.fontSize = '24px';
        closeBtn.style.cursor = 'pointer';
        closeBtn.onclick = function() {
            modal.remove();
        };
        
        // Título del modal
        const modalTitle = document.createElement('h3');
        modalTitle.textContent = `No recibimos: ${titulo}`;
        modalTitle.style.color = '#e63946';
        modalTitle.style.marginBottom = '15px';
        
        // Descripción del modal
        const modalDesc = document.createElement('p');
        modalDesc.textContent = descripcion;
        
        // Información adicional
        const additionalInfo = document.createElement('div');
        additionalInfo.innerHTML = `
            <h4 style="margin-top: 20px;">¿Por qué no recibimos este artículo?</h4>
            <p>Estos artículos representan un riesgo durante el transporte o requieren condiciones especiales que no podemos garantizar. Nuestro objetivo es asegurar que todos los envíos lleguen en perfectas condiciones.</p>
            <h4>¿Alternativas?</h4>
            <p>Para más información sobre alternativas de envío para este tipo de artículo, por favor contacta con nuestro servicio de atención al cliente.</p>
        `;
        
        // Ensamblar el modal
        modalContent.appendChild(closeBtn);
        modalContent.appendChild(modalTitle);
        modalContent.appendChild(modalDesc);
        modalContent.appendChild(additionalInfo);
        modal.appendChild(modalContent);
        
        // Añadir el modal al documento
        document.body.appendChild(modal);
        
        // Cerrar el modal al hacer clic fuera de él
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }
    
    // Añadir animación de entrada para los elementos de la página
    function animateElements() {
        const bannerPrincipal = document.querySelector('.banner-principal');
        const productoCards = document.querySelectorAll('.producto-card');
        const bannerInfo = document.querySelector('.banner-informacion');
        
        // Animar entrada del banner principal
        if (bannerPrincipal) {
            bannerPrincipal.style.opacity = '0';
            bannerPrincipal.style.transform = 'translateY(-20px)';
            bannerPrincipal.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                bannerPrincipal.style.opacity = '1';
                bannerPrincipal.style.transform = 'translateY(0)';
            }, 100);
        }
        
        // Animar entrada de las tarjetas de producto
        productoCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 200 + (index * 100)); // Efecto escalonado
        });
        
        // Animar entrada del banner de información
        if (bannerInfo) {
            bannerInfo.style.opacity = '0';
            bannerInfo.style.transform = 'translateY(20px)';
            bannerInfo.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                bannerInfo.style.opacity = '1';
                bannerInfo.style.transform = 'translateY(0)';
            }, 200 + (productoCards.length * 100) + 200);
        }
    }
    
    // Ejecutar animaciones al cargar la página
    animateElements();
});