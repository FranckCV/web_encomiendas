document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos DOM
    const tarjetaRadio = document.getElementById('tarjeta');
    const bancoRadio = document.getElementById('banco');
    const tarjetaForm = document.getElementById('tarjeta-form');
    const bancoForm = document.getElementById('banco-form');
    const btnPagar = document.getElementById('btn-pagar');
    const validarCuponBtn = document.getElementById('validar-cupon');
    const cuponInput = document.getElementById('cupon');
    const montoPagar = document.getElementById('monto-pagar');
    const total = document.getElementById('total');
    
    // Campos del formulario de tarjeta
    const cardNumber = document.getElementById('card-number');
    const cardExpiry = document.getElementById('card-expiry');
    const cardCvv = document.getElementById('card-cvv');
    const cardName = document.getElementById('card-name');
    
    // Cambiar entre formularios
    tarjetaRadio.addEventListener('change', function() {
        if(this.checked) {
            tarjetaForm.classList.add('active');
            bancoForm.classList.remove('active');
            animateFormTransition(tarjetaForm);
        }
    });
    
    bancoRadio.addEventListener('change', function() {
        if(this.checked) {
            bancoForm.classList.add('active');
            tarjetaForm.classList.remove('active');
            animateFormTransition(bancoForm);
        }
    });
    
    // Formato de número de tarjeta (separado por grupos de 4)
    cardNumber.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        let formattedValue = '';
        
        for(let i = 0; i < value.length; i++) {
            if(i > 0 && i % 4 === 0) {
                formattedValue += ' ';
            }
            formattedValue += value[i];
        }
        
        e.target.value = formattedValue;
        validateCardNumber(e.target);
    });
    
    // Formato de fecha de expiración (MM/AA)
    cardExpiry.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        if (value.length > 0) {
            value = value.match(new RegExp('.{1,2}', 'g')).join('/');
            if (value.length > 5) {
                value = value.substring(0, 5);
            }
        }
        
        e.target.value = value;
        validateCardExpiry(e.target);
    });
    
    // Limitar CVV a solo números
    cardCvv.addEventListener('input', function(e) {
        e.target.value = e.target.value.replace(/\D/g, '');
        validateCardCVV(e.target);
    });
    
    // Convertir nombre a mayúsculas
    cardName.addEventListener('input', function(e) {
        e.target.value = e.target.value.toUpperCase();
        validateCardName(e.target);
    });
    
    // Validar cupón de descuento
    validarCuponBtn.addEventListener('click', function() {
        const cuponValue = cuponInput.value.trim().toUpperCase();
        
        if (!cuponValue) return;
        
        validarCuponBtn.disabled = true;
        validarCuponBtn.classList.add('loading');
        
        // Simular validación de cupón (reemplazar con llamada real a API)
        setTimeout(() => {
            const cupones = {
                'PROMO10': 10,
                'BIENVENIDO': 15,
                'SHALOM25': 25
            };
            
            if (cupones[cuponValue]) {
                const discount = cupones[cuponValue];
                applyCuponDiscount(discount);
                showToast(`¡Cupón aplicado! ${discount}% de descuento`, 'success');
                
                // Añadir elemento de descuento al resumen
                addDiscountToSummary(discount);
            } else {
                showToast('Cupón inválido o expirado', 'error');
                cuponInput.classList.add('error');
                setTimeout(() => cuponInput.classList.remove('error'), 2000);
            }
            
            validarCuponBtn.disabled = false;
            validarCuponBtn.classList.remove('loading');
        }, 1000);
    });
    
    // Botón de pago
    btnPagar.addEventListener('click', function() {
        if (tarjetaRadio.checked) {
            if (validateCardForm()) {
                procesarPago();
            } else {
                showToast('Por favor, completa todos los campos correctamente', 'error');
            }
        } else {
            showToast('Procede con la transferencia bancaria según las instrucciones', 'info');
        }
    });
    
    // Añadir efecto hover a las opciones de pago
    const paymentOptions = document.querySelectorAll('.option-container');
    paymentOptions.forEach(option => {
        option.addEventListener('mouseenter', function() {
            if (!this.querySelector('input').checked) {
                this.querySelector('.option-content').style.borderColor = 'var(--color-accent)';
            }
        });
        
        option.addEventListener('mouseleave', function() {
            if (!this.querySelector('input').checked) {
                this.querySelector('.option-content').style.borderColor = 'var(--color-border)';
            }
        });
    });
    
    // Funciones de validación
    function validateCardNumber(input) {
        const value = input.value.replace(/\s/g, '');
        const valid = /^[0-9]{13,19}$/.test(value);
        
        updateValidationState(input, valid);
        return valid;
    }
    
    function validateCardExpiry(input) {
        const value = input.value;
        let valid = false;
        
        if (/^\d{2}\/\d{2}$/.test(value)) {
            const [month, year] = value.split('/').map(Number);
            const currentDate = new Date();
            const currentYear = currentDate.getFullYear() % 100;
            const currentMonth = currentDate.getMonth() + 1;
            
            valid = month >= 1 && month <= 12 && 
                   (year > currentYear || 
                   (year === currentYear && month >= currentMonth));
        }
        
        updateValidationState(input, valid);
        return valid;
    }
    
    function validateCardCVV(input) {
        const value = input.value;
        const valid = /^\d{3,4}$/.test(value);
        
        updateValidationState(input, valid);
        return valid;
    }
    
    function validateCardName(input) {
        const value = input.value.trim();
        const valid = value.length >= 3 && /^[A-Z\s]+$/.test(value);
        
        updateValidationState(input, valid);
        return valid;
    }
    
    function validateCardForm() {
        const numberValid = validateCardNumber(cardNumber);
        const expiryValid = validateCardExpiry(cardExpiry);
        const cvvValid = validateCardCVV(cardCvv);
        const nameValid = validateCardName(cardName);
        
        return numberValid && expiryValid && cvvValid && nameValid;
    }
    
    function updateValidationState(input, isValid) {
        const formGroup = input.closest('.form-group');
        
        if (input.value) {
            if (isValid) {
                formGroup.classList.remove('error');
                formGroup.classList.add('success');
                removeErrorMessage(formGroup);
            } else {
                formGroup.classList.remove('success');
                formGroup.classList.add('error');
                
                // Mostrar mensaje de error específico según el campo
                let errorMessage = 'Campo inválido';
                
                if (input.id === 'card-number') {
                    errorMessage = 'Número de tarjeta inválido';
                } else if (input.id === 'card-expiry') {
                    errorMessage = 'Formato MM/AA - fecha no válida o expirada';
                } else if (input.id === 'card-cvv') {
                    errorMessage = 'CVV debe tener 3 o 4 dígitos';
                } else if (input.id === 'card-name') {
                    errorMessage = 'Ingrese nombre completo como aparece en la tarjeta';
                }
                
                showErrorMessage(formGroup, errorMessage);
            }
        } else {
            formGroup.classList.remove('error', 'success');
            removeErrorMessage(formGroup);
        }
    }
    
    function showErrorMessage(formGroup, message) {
        removeErrorMessage(formGroup);
        
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.textContent = message;
        formGroup.appendChild(errorElement);
    }
    
    function removeErrorMessage(formGroup) {
        const existingError = formGroup.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
    }
    
    function applyCuponDiscount(discountPercentage) {
        const totalValue = parseFloat(total.textContent.replace('S/ ', ''));
        const discountAmount = totalValue * (discountPercentage / 100);
        const newTotal = totalValue - discountAmount;
        
        // Actualizar el monto en el resumen y botón de pago
        total.textContent = `S/ ${newTotal.toFixed(2)}`;
        montoPagar.textContent = newTotal.toFixed(2);
        
        // Efecto visual de animación de precio
        animatePrice(montoPagar);
    }
    
    function addDiscountToSummary(discountPercentage) {
        // Verificar si ya existe un elemento de descuento y eliminarlo
        const existingDiscount = document.querySelector('.resumen-item.discount');
        if (existingDiscount) existingDiscount.remove();
        
        // Obtener subtotal original
        const subtotalValue = parseFloat(document.getElementById('subtotal').textContent.replace('S/ ', ''));
        const discountAmount = subtotalValue * (discountPercentage / 100);
        
        // Crear nuevo elemento para el descuento
        const discountElement = document.createElement('div');
        discountElement.className = 'resumen-item discount';
        discountElement.innerHTML = `
            <span>Descuento (${discountPercentage}%):</span>
            <span style="color: #27ae60;">- S/ ${discountAmount.toFixed(2)}</span>
        `;
        
        // Insertar antes del divisor
        const divisor = document.querySelector('.resumen-divider');
        divisor.parentNode.insertBefore(discountElement, divisor);
        
        // Animar entrada del elemento
        discountElement.style.opacity = '0';
        discountElement.style.transform = 'translateY(-10px)';
        
        setTimeout(() => {
            discountElement.style.transition = 'all 0.5s ease';
            discountElement.style.opacity = '1';
            discountElement.style.transform = 'translateY(0)';
        }, 50);
    }
    
    function animateFormTransition(form) {
        form.style.animation = 'none';
        form.offsetHeight; // Forzar reflow
        form.style.animation = 'fadeIn 0.3s ease-in-out';
    }
    
    function animatePrice(element) {
        element.style.transition = 'none';
        element.style.transform = 'scale(1.2)';
        element.style.color = '#27ae60';
        
        setTimeout(() => {
            element.style.transition = 'all 0.5s ease';
            element.style.transform = 'scale(1)';
            element.style.color = '';
        }, 50);
    }
    
    function procesarPago() {
        // Simulación de procesamiento de pago
        btnPagar.disabled = true;
        btnPagar.innerHTML = '<span class="loading-text">Procesando</span>';
        btnPagar.classList.add('loading');
        
        setTimeout(() => {
            // Simular resultado exitoso
            showToast('¡Pago procesado con éxito!', 'success');
            btnPagar.disabled = false;
            btnPagar.innerHTML = `PAGO COMPLETADO`;
            btnPagar.classList.remove('loading');
            btnPagar.style.backgroundColor = '#27ae60';
            
            // Redireccionar después de un tiempo
            setTimeout(() => {
                // Aquí redireccionar a página de confirmación
                // window.location.href = '/confirmacion';
                console.log('Redireccionando a página de confirmación');
            }, 2000);
        }, 2000);
    }
    
    // Sistema de notificaciones toast
    function showToast(message, type = 'info') {
        // Eliminar toast anteriores
        const existingToast = document.querySelector('.toast-notification');
        if (existingToast) existingToast.remove();
        
        // Crear nuevo toast
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        
        // Icono según tipo de mensaje
        let icon = '&#9432;'; // info
        if (type === 'success') icon = '&#10004;';
        if (type === 'error') icon = '&#10060;';
        
        toast.innerHTML = `
            <div class="toast-icon">${icon}</div>
            <div class="toast-message">${message}</div>
        `;
        
        document.body.appendChild(toast);
        
        // Animar entrada
        setTimeout(() => {
            toast.style.transform = 'translateY(0)';
            toast.style.opacity = '1';
        }, 10);
        
        // Animar salida y eliminar
        setTimeout(() => {
            toast.style.transform = 'translateY(-20px)';
            toast.style.opacity = '0';
            
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 4000);
    }
    
    // Crear estilos para las notificaciones toast
    createToastStyles();
    
    function createToastStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .toast-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: white;
                border-radius: 8px;
                padding: 12px 20px;
                display: flex;
                align-items: center;
                box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                z-index: 1000;
                transition: all 0.3s ease;
                transform: translateY(-20px);
                opacity: 0;
                max-width: 350px;
            }
            
            .toast-icon {
                margin-right: 12px;
                font-size: 18px;
            }
            
            .toast-success {
                border-left: 4px solid #27ae60;
            }
            
            .toast-error {
                border-left: 4px solid #e74c3c;
            }
            
            .toast-info {
                border-left: 4px solid var(--color-primary);
            }
            
            .toast-success .toast-icon {
                color: #27ae60;
            }
            
            .toast-error .toast-icon {
                color: #e74c3c;
            }
            
            .toast-info .toast-icon {
                color: var(--color-primary);
            }
            
            .form-group input.error {
                border-color: #e74c3c;
                animation: shake 0.5s;
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                20%, 60% { transform: translateX(-5px); }
                40%, 80% { transform: translateX(5px); }
            }
            
            #cupon {
                transition: all 0.3s ease;
            }
            
            #cupon.error {
                border-color: #e74c3c;
                animation: shake 0.5s;
            }
            
            .loading-text:after {
                content: '...';
                animation: dots 1.5s infinite;
            }
            
            @keyframes dots {
                0%, 20% { content: '.'; }
                40%, 60% { content: '..'; }
                80%, 100% { content: '...'; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Efectos de hover para el botón de pago
    btnPagar.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px)';
        this.style.boxShadow = '0 8px 15px rgba(0, 0, 0, 0.2)';
    });
    
    btnPagar.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 4px 10px rgba(0, 0, 0, 0.1)';
    });
    
    // Efecto al hacer scroll para el resumen fijo
    const resumenCompra = document.querySelector('.resumen-compra');
    window.addEventListener('scroll', function() {
        if (window.innerWidth > 992) {
            if (window.scrollY > 100) {
                resumenCompra.style.transition = 'transform 0.3s ease';
                resumenCompra.style.transform = 'translateY(10px)';
            } else {
                resumenCompra.style.transform = 'translateY(0)';
            }
        }
    });
    
    // Mejorar visualización en móviles
    function handleResponsiveLayout() {
        if (window.innerWidth <= 992) {
            resumenCompra.style.transform = 'none';
        }
    }
    
    window.addEventListener('resize', handleResponsiveLayout);
    handleResponsiveLayout();
});