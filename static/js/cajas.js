// Optimización del script para controlar mejor el tamaño y comportamiento
document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos
    const decreaseBtn = document.querySelector('.decrease');
    const increaseBtn = document.querySelector('.increase');
    const qtyInput = document.querySelector('.qty-input');
    const quantityLimit = document.querySelector('.quantity-limit');
    const addToCartBtn = document.querySelector('.btn-agregar');
    const productImage = document.querySelector('.producto-imagen img');
    const priceElement = document.querySelector('.precio');
    const dimensionsElement = document.querySelector('.producto-dimensiones');
    const maxQuantity = 100;
    
    // Datos de los productos por tamaño
    const productSizes = {
        'xxs': {
            price: 1.50,
            dimensions: '15 x 10 x 10 cm',
            image: '/static/img/caja XXS.png',
            discounts: {
                25: 1.20,
                50: 1.00
            }
        },
        'xs': {
            price: 2.00,
            dimensions: '20 x 15 x 15 cm',
            image: '/static/img/caja XS.png',
            discounts: {
                25: 1.70,
                50: 1.40
            }
        },
        's': {
            price: 2.50,
            dimensions: '25 x 20 x 20 cm',
            image: '/static/img/caja S.png',
            discounts: {
                25: 2.20,
                50: 1.90
            }
        },
        'm': {
            price: 3.20,
            dimensions: '30 x 25 x 25 cm',
            image: '/static/img/caja M.png',
            discounts: {
                25: 2.80,
                50: 2.50
            }
        },
        'l': {
            price: 4.00,
            dimensions: '40 x 30 x 30 cm',
            image: '/static/img/caja L.png',
            discounts: {
                25: 3.50,
                50: 3.00
            }
        }
    };
    
    // Estado actual del producto
    let currentSize = 'xxs';
    let currentQuantity = 1;
    
    // Inicialización
    updateQuantity(qtyInput.value);
    updateProductInfo(currentSize);
    
    // Función para actualizar la interfaz según el tamaño seleccionado
    function updateProductInfo(size) {
        currentSize = size;
        const productData = productSizes[size];
        
        // Actualizar imagen
        if (productImage) {
            productImage.src = productData.image;
            productImage.alt = `Caja Shalom - Tamaño ${size.toUpperCase()}`;
        }
        
        // Actualizar dimensiones
        if (dimensionsElement) {
            dimensionsElement.textContent = productData.dimensions;
        }
        
        // Actualizar precio según la cantidad actual
        updatePrice();
    }
    
    // Función para actualizar el precio según el tamaño y la cantidad
    function updatePrice() {
        const productData = productSizes[currentSize];
        let finalPrice = productData.price;
        
        // Aplicar descuentos según la cantidad
        if (currentQuantity >= 50 && productData.discounts[50]) {
            finalPrice = productData.discounts[50];
        } else if (currentQuantity >= 25 && productData.discounts[25]) {
            finalPrice = productData.discounts[25];
        }
        
        // Actualizar el precio en la interfaz
        if (priceElement) {
            priceElement.textContent = finalPrice.toFixed(2);
        }
        
        // Resaltar descuentos aplicados
        highlightDiscount(currentQuantity);
    }
    
    // Resaltar el descuento aplicado
    function highlightDiscount(quantity) {
        const discountItems = document.querySelectorAll('.precio-volumen-item');
        
        discountItems.forEach(item => {
            item.classList.remove('active-discount');
        });
        
        if (quantity >= 50 && discountItems[1]) {
            discountItems[1].classList.add('active-discount');
        } else if (quantity >= 25 && discountItems[0]) {
            discountItems[0].classList.add('active-discount');
        }
    }
    
    // Gestión de la cantidad
    function updateQuantity(value) {
        let newValue = parseInt(value);
        
        // Validar límites
        if (isNaN(newValue) || newValue < 1) {
            newValue = 1;
        } else if (newValue > maxQuantity) {
            newValue = maxQuantity;
            highlightLimit();
        }
        
        // Actualizar valor
        qtyInput.value = newValue;
        currentQuantity = newValue;
        
        // Actualizar estado de botones
        decreaseBtn.disabled = newValue <= 1;
        increaseBtn.disabled = newValue >= maxQuantity;
        
        // Actualizar precio según la nueva cantidad
        updatePrice();
    }
    
    function highlightLimit() {
        quantityLimit.classList.add('active');
        setTimeout(() => {
            quantityLimit.classList.remove('active');
        }, 1500);
    }
    
    // Event listeners para cantidad
    decreaseBtn.addEventListener('click', () => {
        updateQuantity(parseInt(qtyInput.value) - 1);
    });
    
    increaseBtn.addEventListener('click', () => {
        updateQuantity(parseInt(qtyInput.value) + 1);
    });
    
    // Manejar entrada directa en el campo
    qtyInput.addEventListener('change', () => {
        updateQuantity(qtyInput.value);
    });
    
    // Validación en tiempo real mientras se escribe
    qtyInput.addEventListener('input', () => {
        const value = parseInt(qtyInput.value);
        if (!isNaN(value)) {
            if (value > maxQuantity) {
                qtyInput.value = maxQuantity;
                highlightLimit();
            }
            currentQuantity = parseInt(qtyInput.value);
            updatePrice();
        }
    });
    
    // Prevenir caracteres no numéricos y valores mayores que el máximo
    qtyInput.addEventListener('keydown', (e) => {
        // Permitir: backspace, delete, tab, escape, enter y .
        if ([46, 8, 9, 27, 13, 110].indexOf(e.keyCode) !== -1 ||
            // Permitir: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
            (e.keyCode === 65 && e.ctrlKey === true) ||
            (e.keyCode === 67 && e.ctrlKey === true) ||
            (e.keyCode === 86 && e.ctrlKey === true) ||
            (e.keyCode === 88 && e.ctrlKey === true) ||
            // Permitir: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
            return;
        }
        
        // Asegurarse de que sea un número
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && 
            (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
            return;
        }
        
        // Comprobar si excederá el límite máximo
        const currentValue = qtyInput.value;
        const selectionStart = qtyInput.selectionStart;
        const selectionEnd = qtyInput.selectionEnd;
        const keyValue = e.key;
        
        // Si no hay selección (solo se está añadiendo un dígito)
        if (selectionStart === selectionEnd) {
            const newValue = currentValue.slice(0, selectionStart) + keyValue + currentValue.slice(selectionEnd);
            if (parseInt(newValue) > maxQuantity) {
                e.preventDefault();
                highlightLimit();
            }
        }
    });
    
   /*  // Agregar al carrito con validación
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', () => {
            const quantity = parseInt(qtyInput.value);
            if (quantity > 0 && quantity <= maxQuantity) {
                // Calcular precio final
                const productData = productSizes[currentSize];
                let finalPrice = productData.price;
                
                if (quantity >= 50 && productData.discounts[50]) {
                    finalPrice = productData.discounts[50];
                } else if (quantity >= 25 && productData.discounts[25]) {
                    finalPrice = productData.discounts[25];
                }
                
                const totalPrice = (finalPrice * quantity).toFixed(2);
                
                // Aquí iría la lógica para agregar al carrito
                alert(`Se han agregado ${quantity} unidades de caja ${currentSize.toUpperCase()} al carrito\nPrecio unitario: S/ ${finalPrice.toFixed(2)}\nTotal: S/ ${totalPrice}`);
            } else {
                highlightLimit();
            }
        });
    } */
    
    // Botones de tamaño
    const sizeBtns = document.querySelectorAll('.size-btn');
    sizeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Eliminar clase activa de todos los botones
            sizeBtns.forEach(b => b.classList.remove('active'));
            // Añadir clase activa al botón clickeado
            btn.classList.add('active');
            // Obtener el tamaño del botón (del texto o de un atributo data)
            const size = btn.textContent.toLowerCase();
            // Actualizar la información del producto
            updateProductInfo(size);
        });
    });
    
    // Añadir estilos para resaltar el descuento activo
    const style = document.createElement('style');
    style.textContent = `
        .precio-volumen-item.active-discount {
            border: 2px solid #1a3c5b;
            transform: scale(1.05);
            background-color: #e8f4f8;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
    `;
    document.head.appendChild(style);
    
    // Ajuste de responsividad dinámica
    function adjustResponsiveness() {
        const productContainer = document.querySelector('.producto-detalle');
        if (window.innerWidth <= 768) {
            // Ajustes para móviles
            productContainer.style.flexDirection = 'column';
        } else {
            // Ajustes para desktop
            productContainer.style.flexDirection = 'row';
        }
    }
    
    // Ejecutar al cargar y al cambiar tamaño
    adjustResponsiveness();
    window.addEventListener('resize', adjustResponsiveness);
});