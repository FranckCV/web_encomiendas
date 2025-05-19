// JavaScript optimizado con animaciones basadas en clases CSS
document.addEventListener('DOMContentLoaded', function() {
    // Referencia al modal
    const modal = document.getElementById('producto-modal');
    const modalTitle = document.getElementById('modal-producto-titulo');
    const modalDescription = document.getElementById('modal-producto-descripcion');
    const modalClose = modal.querySelector('.modal-close');
    
    // Selección de elementos para animar
    const bannerPrincipal = document.querySelector('.banner-principal');
    const productoCards = document.querySelectorAll('.producto-card');
    const bannerInfo = document.querySelector('.banner-informacion');
    
    // Añadir efectos de clic a las tarjetas para mostrar el modal
    productoCards.forEach(card => {
        card.addEventListener('click', function() {
            const titulo = this.querySelector('.producto-titulo').textContent;
            const descripcion = this.querySelector('.producto-descripcion').textContent;
            
            modalTitle.textContent = titulo;
            modalDescription.textContent = descripcion;
            
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });
    
    // Cerrar el modal
    modalClose.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    // Animaciones de entrada usando clases CSS
    function animateElements() {
        // Animar banner principal
        if (bannerPrincipal) {
            setTimeout(() => {
                bannerPrincipal.classList.add('animated');
            }, 100);
        }
        
        // Animar tarjetas de producto con efecto escalonado
        productoCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('animated');
            }, 200 + (index * 100));
        });
        
        // Animar banner de información
        if (bannerInfo) {
            setTimeout(() => {
                bannerInfo.classList.add('animated');
            }, 200 + (productoCards.length * 100) + 200);
        }
    }
    
    // Iniciar animaciones
    animateElements();
});