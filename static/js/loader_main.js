
(function(window, document) {
    'use strict';
    if (typeof window.Loader !== 'undefined' && !!document.getElementById('loading-overlay')) {
        return; 
    }
    
    let Loader = {
        overlayElement: null,
        isVisible: false,

        createOverlay: function() {
            // Crear el elemento de overlay si no existe
            if (!document.getElementById('loading-overlay')) {
                const overlay = document.createElement('div');
                overlay.id = 'loading-overlay';
                overlay.classList.add('loading-overlay', 'hidden');
                overlay.innerHTML = `
                     <div class="loader-container">
                        <div class="loader-circle loader-circle-outer"></div>
                        <div class="loader-circle loader-circle-inner"></div>
                        <div class="loader-circle loader-circle-center"></div>
                    </div>
                `;
                document.body.appendChild(overlay);
            }
        },

        init: function() {
            this.createOverlay();
            this.overlayElement = document.getElementById('loading-overlay');
            
            if (!this.overlayElement) {
                console.error('Error: No se pudo crear el elemento de carga.');
                return;
            }
            this.isVisible = this.overlayElement.classList.contains('visible');
        },

        show: function() {
            if (!this.overlayElement || this.isVisible) {
                return; 
            }
            this.overlayElement.style.display = 'flex';
            this.overlayElement.getBoundingClientRect(); 
            this.overlayElement.classList.remove('hidden');
            this.overlayElement.classList.add('visible');
            document.body.style.overflow = 'hidden';
            this.isVisible = true;
        },

        hide: function() {
            if (!this.overlayElement || !this.isVisible) {
                return; 
            }
            this.overlayElement.classList.remove('visible');
            this.overlayElement.classList.add('hidden');
            this.isVisible = false;
            setTimeout(() => {
                if (!this.isVisible) {
                    this.overlayElement.style.display = 'none';
                    document.body.style.overflow = '';
                }
            }, 300); 
        },

        toggle: function(forceState) {            
            const shouldShow = (typeof forceState === 'boolean') ? forceState : !this.isVisible;            
            if (shouldShow) {
                this.show();
            } else {
                this.hide();
            }
        }
    };
    window.Loader = Loader;
    /*
    function autoInitLoader() {
        Loader.init();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', autoInitLoader);
    } else {
        autoInitLoader();
    }*/
})(window, document);
