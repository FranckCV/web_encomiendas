document.addEventListener('DOMContentLoaded', function() {
    // Información de los tamaños de cajas
    const sizeInfo = {
        'xxs': { dimensions: '15 x 10 x 10 cm', price: '1.50', image: 'caja XXS.png', maxQuantity: 100 },
        'xs': { dimensions: '20 x 15 x 10 cm', price: '2.00', image: 'caja XS.png', maxQuantity: 80 },
        's': { dimensions: '25 x 20 x 15 cm', price: '2.50', image: 'caja S.png', maxQuantity: 60 },
        'm': { dimensions: '30 x 25 x 20 cm', price: '3.00', image: 'caja M.png', maxQuantity: 40 },
        'l': { dimensions: '40 x 30 x 25 cm', price: '4.00', image: 'caja L.png', maxQuantity: 30 }
    };

    // Elementos del DOM
    const sizeBtns = document.querySelectorAll('.size-btn');
    const productImage = document.querySelector('.producto-imagen img');
    const decreaseBtn = document.querySelector('.qty-btn.decrease');
    const increaseBtn = document.querySelector('.qty-btn.increase');
    const qtyInput = document.querySelector('.qty-input');
    const addToCartBtn = document.querySelector('.btn-agregar');
    const quantityLimit = document.querySelector('.quantity-limit');
    
    // Función para actualizar la información del producto según el tamaño
    function updateProductInfo(sizeKey) {
        const dimensionsElem = document.querySelector('.producto-dimensiones');
        const priceElem = document.querySelector('.precio');
        
        if (sizeInfo[sizeKey]) {
            // Actualizar dimensiones y precio
            dimensionsElem.textContent = sizeInfo[sizeKey].dimensions;
            priceElem.textContent = sizeInfo[sizeKey].price;
            
            // Actualizar imagen
            if (productImage && sizeInfo[sizeKey].image) {
                // Guarda la ruta base
                const basePath = '/static/img/';
                productImage.src = basePath + sizeInfo[sizeKey].image;
                
                // También actualiza el atributo alt para mejor accesibilidad
                productImage.alt = `Caja Shalom ${sizeKey.toUpperCase()}`;
            }
            
            // Actualización de precios por volumen
            const bulkPrices = document.querySelectorAll('.etiqueta-precio');
            if (sizeKey === 'xxs') {
                bulkPrices[0].textContent = 's/. 1.20';
                bulkPrices[1].textContent = 's/. 1.00';
            } else if (sizeKey === 'xs') {
                bulkPrices[0].textContent = 's/. 1.70';
                bulkPrices[1].textContent = 's/. 1.50';
            } else if (sizeKey === 's') {
                bulkPrices[0].textContent = 's/. 2.20';
                bulkPrices[1].textContent = 's/. 2.00';
            } else if (sizeKey === 'm') {
                bulkPrices[0].textContent = 's/. 2.70';
                bulkPrices[1].textContent = 's/. 2.50';
            } else if (sizeKey === 'l') {
                bulkPrices[0].textContent = 's/. 3.70';
                bulkPrices[1].textContent = 's/. 3.50';
            }
            
            // Actualizar mensaje de límite máximo
            if (quantityLimit) {
                quantityLimit.textContent = `Máximo: ${sizeInfo[sizeKey].maxQuantity} unidades`;
            }
            
            // Validar que la cantidad actual no exceda el nuevo límite
            validateQuantity();
        }
    }

    // Función para validar la cantidad
    function validateQuantity() {
        const activeSize = document.querySelector('.size-btn.active');
        if (!activeSize) return;
        
        const sizeClass = Array.from(activeSize.classList)
            .find(cls => ['xxs', 'xs', 's', 'm', 'l'].includes(cls));
            
        if (!sizeClass || !sizeInfo[sizeClass]) return;
        
        const maxQty = sizeInfo[sizeClass].maxQuantity;
        let currentQty = parseInt(qtyInput.value);
        
        // Si no es un número o es menor que 1, establecer a 1
        if (isNaN(currentQty) || currentQty < 1) {
            currentQty = 1;
        }
        
        // Si excede el máximo, establecer al máximo
        if (currentQty > maxQty) {
            currentQty = maxQty;
            
            // Mostrar mensaje de alerta temporal
            quantityLimit.classList.add('active');
            setTimeout(() => {
                quantityLimit.classList.remove('active');
            }, 3000);
        }
        
        // Actualizar el input
        qtyInput.value = currentQty;
        
        // Actualizar estado de los botones
        decreaseBtn.disabled = currentQty <= 1;
        increaseBtn.disabled = currentQty >= maxQty;
    }

    // Event listeners para botones de tamaño
    sizeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remover clase active de todos los botones
            sizeBtns.forEach(b => b.classList.remove('active'));
            
            // Añadir clase active al botón clickeado
            this.classList.add('active');
            
            // Actualizar información del producto según tamaño seleccionado
            const sizeClass = Array.from(this.classList)
                .find(cls => ['xxs', 'xs', 's', 'm', 'l'].includes(cls));
                
            if (sizeClass) {
                updateProductInfo(sizeClass);
            }
        });
    });
    
    // Event listeners para selector de cantidad
    if (decreaseBtn) {
        decreaseBtn.addEventListener('click', function() {
            let currentQty = parseInt(qtyInput.value);
            if (currentQty > 1) {
                qtyInput.value = currentQty - 1;
                validateQuantity();
                updateTotalPrice();
            }
        });
    }

    if (increaseBtn) {
        increaseBtn.addEventListener('click', function() {
            let currentQty = parseInt(qtyInput.value);
            qtyInput.value = currentQty + 1;
            validateQuantity();
            updateTotalPrice();
        });
    }
    
    // Hacer que el input sea editable
    if (qtyInput) {
        // Eliminar el atributo readonly
        qtyInput.removeAttribute('readonly');
        
        // Manejar cambios en el input
        qtyInput.addEventListener('input', function() {
            validateQuantity();
            updateTotalPrice();
        });
        
        // Manejar el evento blur (cuando pierde el foco)
        qtyInput.addEventListener('blur', function() {
            validateQuantity();
            updateTotalPrice();
        });
        
        // Para evitar valores no numéricos
        qtyInput.addEventListener('keydown', function(e) {
            // Permitir: backspace, delete, tab, escape, enter y .
            if ([46, 8, 9, 27, 13, 110, 190].indexOf(e.keyCode) !== -1 ||
                // Permitir: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true) ||
                // Permitir: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)) {
                return;
            }
            // Asegurarse de que sea un número y detener el keypress
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && 
                (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
    }

    // Función para actualizar el precio total
    function updateTotalPrice() {
        const activeSize = document.querySelector('.size-btn.active');
        if (!activeSize) return;
        
        const sizeClass = Array.from(activeSize.classList)
            .find(cls => ['xxs', 'xs', 's', 'm', 'l'].includes(cls));
            
        if (!sizeClass || !sizeInfo[sizeClass]) return;
        
        const price = parseFloat(sizeInfo[sizeClass].price);
        const quantity = parseInt(qtyInput.value);
        
        // Si tienes un elemento para mostrar el precio total, puedes descomentar esto
        // const totalPriceElem = document.querySelector('.precio-total');
        // if (totalPriceElem) {
        //     totalPriceElem.textContent = `S/ ${(price * quantity).toFixed(2)}`;
        // }
        
        // También puedes actualizar el texto del botón "Agregar al carrito" para incluir el total
        if (addToCartBtn) {
            const originalText = "Agregar al carrito";
            addToCartBtn.innerHTML = `${originalText} <i class="fa-solid fa-cart-shopping"></i>`;
        }
    }
    
    // Event listener para botón "Agregar al carrito"
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function() {
            const activeSize = document.querySelector('.size-btn.active');
            if (!activeSize) return;
            
            const sizeClass = Array.from(activeSize.classList)
                .find(cls => ['xxs', 'xs', 's', 'm', 'l'].includes(cls));
                
            if (!sizeClass || !sizeInfo[sizeClass]) return;
            
            const sizeLabel = activeSize.textContent.toUpperCase();
            const dimensions = sizeInfo[sizeClass].dimensions;
            const price = sizeInfo[sizeClass].price;
            const quantity = parseInt(qtyInput.value);
            const total = (parseFloat(price) * quantity).toFixed(2);
            
            // Muestra mensaje de confirmación
            alert(`Producto agregado al carrito:
            - Caja Shalom ${sizeLabel} (${dimensions})
            - Cantidad: ${quantity}
            - Precio unitario: S/ ${price}
            - Total: S/ ${total}`);
            
            // Aquí iría el código para realmente agregar al carrito
            console.log('Producto agregado:', {
                name: 'Caja Shalom',
                size: sizeClass,
                sizeLabel: sizeLabel,
                dimensions: dimensions,
                price: price,
                quantity: quantity,
                total: total
            });
        });
    }
    
    // Inicializar con el tamaño que tenga la clase active al cargar
    const activeSizeBtn = document.querySelector('.size-btn.active');
    if (activeSizeBtn) {
        const activeSize = Array.from(activeSizeBtn.classList)
            .find(cls => ['xxs', 'xs', 's', 'm', 'l'].includes(cls));
        if (activeSize) {
            updateProductInfo(activeSize);
        }
    }

});