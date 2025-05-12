document.addEventListener('DOMContentLoaded', function () {
    // Datos de productos
    const productos = [
        {
            id: 1,
            nombre: "Plumón Indeleble",
            descripcion: "Marcador permanente con punta gruesa redondeada que posee una tinta color negro resistente al agua y la luz.",
            dimensiones: "Multimark Jumbo 23",
            precio: 3.00,
            imagen: "/static/img/plumon.png",
            preciosVolumen: [
                { precio: 2.80, cantidad: 12 },
                { precio: 2.50, cantidad: 24 }
            ],
            tamanios: [],
            maxQuantity: 50 // Cantidad máxima para este producto
        },
        {
            id: 2,
            nombre: "Sobre A4",
            descripcion: "Ideal para el traslado de tus documentos.",
            dimensiones: "21 x 29.7 cm",
            precio: 1.00,
            imagen: "/static/img/sobre.png",
            preciosVolumen: [
                { precio: 0.90, cantidad: 50 },
                { precio: 0.80, cantidad: 100 }
            ],
            tamanios: [],
            maxQuantity: 200 // Cantidad máxima para este producto
        },
        {
            id: 3,
            nombre: "Cinta de Embalaje",
            descripcion: "Cinta adhesiva resistente para todo tipo de paquetes.",
            dimensiones: "48mm x 40m",
            precio: 5.90,
            imagen: "/static/img/cintaEmbalaje.png",
            preciosVolumen: [
                { precio: 5.50, cantidad: 6 },
                { precio: 5.00, cantidad: 12 }
            ],
            tamanios: [],
            maxQuantity: 30 // Cantidad máxima para este producto
        },
        {
            id: 4,
            nombre: "Stretch Film",
            descripcion: "Ideal para embalar y proteger todos tus envíos.",
            dimensiones: "Varios tamaños",
            precio: 12.00,
            imagen: "/static/img/stretchfilm.png",
            preciosVolumen: [
                { precio: 11.00, cantidad: 5 },
                { precio: 10.00, cantidad: 10 }
            ],
            tamanios: ["9''", "15''"],
                 // Agregar precios específicos por tamaño
                 preciosPorTamanio: {
                    "9''": {
                        precio: 12.00,
                        preciosVolumen: [
                            { precio: 11.00, cantidad: 5 },
                            { precio: 10.00, cantidad: 10 }
                        ]
                    },
                    "15''": {
                        precio: 18.00,
                        preciosVolumen: [
                            { precio: 16.50, cantidad: 5 },
                            { precio: 15.00, cantidad: 10 }
                        ]
                    }
                },
                tamanioActivo: "9''", // Establecer el tamaño por defecto
                maxQuantity: 20 // Cantidad máxima para este producto
        },
        {
            id: 5,
            nombre: "Burbupack",
            descripcion: "Lámina de plástico burbuja para proteger objetos frágiles.",
            dimensiones: "1m x 1m",
            precio: 2.50,
            imagen: "/static/img/burbupack.png",
            preciosVolumen: [
                { precio: 2.30, cantidad: 10 },
                { precio: 2.00, cantidad: 20 }
            ],
            tamanios: ["1m x 1m", "1m x 2m", "2m x 2m"],
            // Agregar precios específicos por tamaño
            preciosPorTamanio: {
                "1m x 1m": {
                    precio: 2.50,
                    preciosVolumen: [
                        { precio: 2.30, cantidad: 10 },
                        { precio: 2.00, cantidad: 20 }
                    ]
                },
                "1m x 2m": {
                    precio: 4.50,
                    preciosVolumen: [
                        { precio: 4.20, cantidad: 10 },
                        { precio: 3.80, cantidad: 20 }
                    ]
                },
                "2m x 2m": {
                    precio: 8.00,
                    preciosVolumen: [
                        { precio: 7.50, cantidad: 10 },
                        { precio: 7.00, cantidad: 20 }
                    ]
                }
            },
            tamanioActivo: "1m x 1m", // Establecer el tamaño por defecto
            maxQuantity: 40 // Cantidad máxima para este producto
        }
    ];

    // Elementos del DOM
    const productoImg = document.getElementById('producto-img');
    const productoTitulo = document.getElementById('producto-titulo');
    const productoDescripcion = document.getElementById('producto-descripcion');
    const productoDimensiones = document.getElementById('producto-dimensiones');
    const precioPrincipal = document.getElementById('precio');
    const preciosVolumen = document.getElementById('precios-volumen');
    const sizeOptions = document.getElementById('size-options');
    const thumbsContainer = document.getElementById('thumbs-container');
    const productosRelacionadosGrid = document.getElementById('productos-relacionados-grid');

    // Control de cantidad - FIX: Asegurarse de que estos elementos existan
    const decreaseBtn = document.querySelector('.qty-btn.decrease');
    const increaseBtn = document.querySelector('.qty-btn.increase');
    const qtyInput = document.querySelector('.qty-input');
    
    // Mensaje para límite de cantidad
    let quantityLimit = document.querySelector('.quantity-limit');
    if (!quantityLimit) {
        quantityLimit = document.createElement('div');
        quantityLimit.classList.add('quantity-limit');
        // Insertar después del input de cantidad
        if (qtyInput && qtyInput.parentNode) {
            qtyInput.parentNode.insertAdjacentElement('afterend', quantityLimit);
        }
    }

    // Índice del producto actual
    let productoActualIndex = 0;

    // Inicializar la página
    function inicializarPagina() {
        // Crear miniaturas de productos
        crearMiniaturas();

        // Cargar producto inicial
        cargarProducto(productoActualIndex);

        // Cargar productos relacionados
        if (productosRelacionadosGrid) {
            cargarProductosRelacionados();
        }

        // Configurar eventos
        configurarEventos();
        
        // FIX: Asegurarse de que este elemento exista
        if (qtyInput) {
            // Inicializar el control de cantidad
            initializeQuantityControl();
        }
    }

    // Crear miniaturas de navegación
    function crearMiniaturas() {
        if (!thumbsContainer) return;
        
        thumbsContainer.innerHTML = '';

        productos.forEach((producto, index) => {
            const thumbItem = document.createElement('div');
            thumbItem.classList.add('thumb-item');
            if (index === productoActualIndex) {
                thumbItem.classList.add('active');
            }

            thumbItem.innerHTML = `
                <img src="${producto.imagen}" alt="${producto.nombre}">
                <p>${producto.nombre}</p>
            `;

            thumbItem.addEventListener('click', () => {
                productoActualIndex = index;
                cargarProducto(index);
                actualizarMiniaturaActiva();
            });

            thumbsContainer.appendChild(thumbItem);
        });
    }

    // Actualizar miniatura activa
    function actualizarMiniaturaActiva() {
        const thumbItems = document.querySelectorAll('.thumb-item');
        thumbItems.forEach((item, index) => {
            if (index === productoActualIndex) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    // Cargar datos del producto
    function cargarProducto(index) {
        const producto = productos[index];

        // Verificar que los elementos existan antes de actualizar
        if (productoImg) {
            productoImg.src = producto.imagen;
            productoImg.alt = producto.nombre;
        }
        
        if (productoTitulo) productoTitulo.textContent = producto.nombre;
        if (productoDescripcion) productoDescripcion.textContent = producto.descripcion;
        if (productoDimensiones) productoDimensiones.textContent = producto.dimensiones;
        
        // Actualizar precio según tamaño si existe
        actualizarPrecioSegunTamanio(producto);

        // Actualizar opciones de tamaño
        if (sizeOptions) {
            cargarOpcionesTamanio(producto.tamanios, producto.tamanioActivo);
        }

        // Resetear cantidad y actualizar límite
        if (qtyInput) {
            qtyInput.value = 1;
            updateQuantityLimit(producto.maxQuantity);
            validateQuantity();
        }
    }

    // Nueva función: Actualizar precio según el tamaño seleccionado
    function actualizarPrecioSegunTamanio(producto) {
        if (!precioPrincipal) return;
        
        // Si el producto tiene precios por tamaño y un tamaño activo
        if (producto.preciosPorTamanio && producto.tamanioActivo) {
            const precioInfo = producto.preciosPorTamanio[producto.tamanioActivo];
            if (precioInfo) {
                // Actualizar precio principal
                precioPrincipal.textContent = precioInfo.precio.toFixed(2);
                
                // Actualizar precios por volumen
                if (preciosVolumen) {
                    cargarPreciosVolumen(precioInfo.preciosVolumen);
                }
                return;
            }
        }
        
        // Si no tiene precios por tamaño o no se encontró el tamaño activo, usar el precio normal
        precioPrincipal.textContent = producto.precio.toFixed(2);
        
        // Actualizar precios por volumen
        if (preciosVolumen) {
            cargarPreciosVolumen(producto.preciosVolumen);
        }
    }

    // Actualizar mensaje de límite de cantidad
    function updateQuantityLimit(maxQty) {
        if (quantityLimit) {
            quantityLimit.textContent = `Máximo: ${maxQty} unidades`;
        }
    }

    // Función para validar la cantidad
    function validateQuantity() {
        if (!qtyInput) return;
        
        const producto = productos[productoActualIndex];
        if (!producto) return;
        
        const maxQty = producto.maxQuantity;
        let currentQty = parseInt(qtyInput.value);
        
        // Si no es un número o es menor que 1, establecer a 1
        if (isNaN(currentQty) || currentQty < 1) {
            currentQty = 1;
        }
        
        // Si excede el máximo, establecer al máximo
        if (currentQty > maxQty) {
            currentQty = maxQty;
            
            // Mostrar mensaje de alerta temporal
            if (quantityLimit) {
                quantityLimit.classList.add('active');
                setTimeout(() => {
                    quantityLimit.classList.remove('active');
                }, 3000);
            }
        }
        
        // Actualizar el input
        qtyInput.value = currentQty;
        
        // Actualizar estado de los botones
        if (decreaseBtn) decreaseBtn.disabled = currentQty <= 1;
        if (increaseBtn) increaseBtn.disabled = currentQty >= maxQty;
        
        // Actualizar precio total si existe esa función
        updateTotalPrice();
    }

    // Función para actualizar el precio total
    function updateTotalPrice() {
        const producto = productos[productoActualIndex];
        if (!producto) return;
        
        // Determinar el precio correcto según el tamaño
        let price = producto.precio;
        if (producto.preciosPorTamanio && producto.tamanioActivo) {
            const precioInfo = producto.preciosPorTamanio[producto.tamanioActivo];
            if (precioInfo) {
                price = precioInfo.precio;
            }
        }
        
        const quantity = parseInt(qtyInput.value);
        
        // Si tienes un elemento para mostrar el precio total, puedes descomentar esto
        // const totalPriceElem = document.querySelector('.precio-total');
        // if (totalPriceElem) {
        //     totalPriceElem.textContent = `S/ ${(price * quantity).toFixed(2)}`;
        // }
        
        // También puedes actualizar el texto del botón "Agregar al carrito" para incluir el total
        const addToCartBtn = document.querySelector('.btn-agregar');
        if (addToCartBtn) {
            const originalText = "Agregar al carrito";
            addToCartBtn.innerHTML = `${originalText} <i class="fa-solid fa-cart-shopping"></i>`;
        }
    }

    // Inicializar control de cantidad
    function initializeQuantityControl() {
        if (!qtyInput) return;
        
        // Eliminar el atributo readonly si existe
        qtyInput.removeAttribute('readonly');
        
        // Asegurarse de que la entrada sea un número
        qtyInput.type = 'number';
        
        // Manejar cambios en el input
        qtyInput.addEventListener('input', function() {
            validateQuantity();
        });
        
        // Manejar el evento blur (cuando pierde el foco)
        qtyInput.addEventListener('blur', function() {
            validateQuantity();
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

    // Cargar precios por volumen
    function cargarPreciosVolumen(precios) {
        if (!preciosVolumen) return;
        
        preciosVolumen.innerHTML = '';

        precios.forEach(precio => {
            const precioItem = document.createElement('div');
            precioItem.classList.add('precio-volumen-item');

            precioItem.innerHTML = `
                <span class="etiqueta-precio">S/ ${precio.precio.toFixed(2)}</span>
                <span class="etiqueta-cantidad">a partir de ${precio.cantidad} uds.</span>
            `;

            preciosVolumen.appendChild(precioItem);
        });
    }

    // Cargar opciones de tamaño
    function cargarOpcionesTamanio(tamanios, tamanioActivo) {
        if (!sizeOptions) return;
        
        sizeOptions.innerHTML = '';

        if (tamanios.length === 0) {
            sizeOptions.style.display = 'none';
            return;
        }

        sizeOptions.style.display = 'flex';

        tamanios.forEach(tamanio => {
            const sizeBtn = document.createElement('button');
            sizeBtn.classList.add('size-btn');
            sizeBtn.textContent = tamanio;

            if (tamanio === tamanioActivo) {
                sizeBtn.classList.add('active');
            }

            sizeBtn.addEventListener('click', () => {
                // Actualizar tamaño activo en el objeto del producto
                productos[productoActualIndex].tamanioActivo = tamanio;

                // Actualizar UI
                document.querySelectorAll('.size-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                sizeBtn.classList.add('active');
                
                // Actualizar precio según el tamaño seleccionado
                actualizarPrecioSegunTamanio(productos[productoActualIndex]);
                
                // Actualizar precio total si existe
                updateTotalPrice();
            });

            sizeOptions.appendChild(sizeBtn);
        });
    }

    // Cargar productos relacionados
    function cargarProductosRelacionados() {
        if (!productosRelacionadosGrid) return;
        
        productosRelacionadosGrid.innerHTML = '';

        // Mostrar 4 productos aleatorios diferentes al actual
        const productosDisponibles = [...productos];
        productosDisponibles.splice(productoActualIndex, 1);

        // Mezclar el array para mostrar productos aleatorios
        const productosAleatorios = mezclarArray(productosDisponibles).slice(0, 4);

        productosAleatorios.forEach(producto => {
            const productoItem = document.createElement('div');
            productoItem.classList.add('producto-item');

            productoItem.innerHTML = `
                <img src="${producto.imagen}" alt="${producto.nombre}">
                <h3>${producto.nombre}</h3>
                <p>S/ ${producto.precio.toFixed(2)}</p>
            `;

            productoItem.addEventListener('click', () => {
                // Encontrar índice del producto seleccionado
                const nuevoIndex = productos.findIndex(p => p.id === producto.id);
                productoActualIndex = nuevoIndex;
                cargarProducto(nuevoIndex);
                actualizarMiniaturaActiva();

                // Hacer scroll hacia arriba para mostrar el producto
                const productoDetalle = document.querySelector('.producto-detalle');
                if (productoDetalle) {
                    productoDetalle.scrollIntoView({
                        behavior: 'smooth'
                    });
                }

                // Recargar productos relacionados
                cargarProductosRelacionados();
            });

            productosRelacionadosGrid.appendChild(productoItem);
        });
    }

    // Mezclar array (algoritmo Fisher-Yates)
    function mezclarArray(array) {
        const newArray = [...array];
        for (let i = newArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
        }
        return newArray;
    }

    // Configurar eventos
    function configurarEventos() {
        // Botones de navegación
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                productoActualIndex = (productoActualIndex - 1 + productos.length) % productos.length;
                cargarProducto(productoActualIndex);
                actualizarMiniaturaActiva();
                if (productosRelacionadosGrid) {
                    cargarProductosRelacionados();
                }
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                productoActualIndex = (productoActualIndex + 1) % productos.length;
                cargarProducto(productoActualIndex);
                actualizarMiniaturaActiva();
                if (productosRelacionadosGrid) {
                    cargarProductosRelacionados();
                }
            });
        }

        // Event listeners para selector de cantidad
        if (decreaseBtn) {
            decreaseBtn.addEventListener('click', function() {
                if (!qtyInput) return;
                
                let currentQty = parseInt(qtyInput.value);
                if (currentQty > 1) {
                    qtyInput.value = currentQty - 1;
                    validateQuantity();
                }
            });
        }

        if (increaseBtn) {
            increaseBtn.addEventListener('click', function() {
                if (!qtyInput) return;
                
                let currentQty = parseInt(qtyInput.value);
                qtyInput.value = currentQty + 1;
                validateQuantity();
            });
        }

        // Botón de agregar al carrito
        const addToCartBtn = document.querySelector('.btn-agregar');
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', () => {
                const producto = productos[productoActualIndex];
                const cantidad = parseInt(qtyInput.value);
                let tamanioSeleccionado = '';

                if (producto.tamanios && producto.tamanios.length > 0) {
                    tamanioSeleccionado = producto.tamanioActivo;
                }

                // Aquí se implementaría la lógica para agregar al carrito
                console.log(`Agregando al carrito: ${cantidad} ${producto.nombre} ${tamanioSeleccionado ? '- ' + tamanioSeleccionado : ''}`);

                // Mostrar mensaje de confirmación
                alert(`¡${cantidad} ${producto.nombre} ${tamanioSeleccionado ? '- ' + tamanioSeleccionado : ''} agregado al carrito!`);
            });
        }
    }

    // Iniciar la página
    inicializarPagina();
});