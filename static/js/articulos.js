document.addEventListener('DOMContentLoaded', function () {
    // Referencias a elementos del DOM
    const productoImg = document.querySelector('.producto-imagen img');
    const productoTitulo = document.getElementById('producto-titulo');
    const productoDescripcion = document.getElementById('producto-descripcion');
    const productoDimensiones = document.getElementById('producto-dimensiones');
    const precioPrincipal = document.getElementById('precio');
    const preciosVolumen = document.getElementById('precios-volumen');
    const sizeOptions = document.getElementById('size-options');
    const decreaseBtn = document.querySelector('.qty-btn.decrease');
    const increaseBtn = document.querySelector('.qty-btn.increase');
    const qtyInput = document.querySelector('.qty-input');
    const quantityLimit = document.querySelector('.quantity-limit') || createQuantityLimit();
    const addToCartBtn = document.querySelector('.btn-agregar');
    const thumbsContainer = document.getElementById('thumbs-container');
    const productosRelacionadosGrid = document.getElementById('productos-relacionados-grid');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    // Función para crear el elemento de límite de cantidad si no existe
    function createQuantityLimit() {
        const limitElement = document.createElement('div');
        limitElement.classList.add('quantity-limit');
        if (qtyInput && qtyInput.parentNode) {
            qtyInput.parentNode.insertAdjacentElement('afterend', limitElement);
        }
        return limitElement;
    }

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
                { precio: 2.50, cantidad: 12 },
                { precio: 2.80, cantidad: 24 }
            ],
            tamanios: [],
            maxQuantity: 50
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
            maxQuantity: 200
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
            maxQuantity: 30
        },
        {
            id: 4,
            nombre: "Stretch Film",
            descripcion: "Ideal para embalar y proteger todos tus envíos.",
            dimensiones: "Varios tamaños",
            precio: 12.00,
            imagen: "/static/img/stretchfilm.png",
            tamanios: ["9''", "15''"],
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
            tamanioActivo: "9''",
            maxQuantity: 20
        },
        {
            id: 5,
            nombre: "Burbupack",
            descripcion: "Lámina de plástico burbuja para proteger objetos frágiles.",
            dimensiones: "1m x 1m",
            precio: 2.50,
            imagen: "/static/img/burbupack.png",
            tamanios: ["1m x 1m", "1m x 2m", "2m x 2m"],
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
            tamanioActivo: "1m x 1m",
            maxQuantity: 40
        }
    ];

    // Estado actual
    let productoActualIndex = 0;
    let currentQuantity = 1;

    // Inicialización
    function inicializarPagina() {
        // Crear miniaturas para navegación
        crearMiniaturas();

        // Cargar producto inicial
        cargarProducto(productoActualIndex);

        // Cargar productos relacionados
        if (productosRelacionadosGrid) {
            cargarProductosRelacionados();
        }

        // Configurar eventos
        configurarEventos();

        // Inicializar control de cantidad
        inicializarControlCantidad();

        // Añadir estilos para descuentos activos
        añadirEstilosDescuentos();

        // Ajustar responsividad
        ajustarResponsividad();
        window.addEventListener('resize', ajustarResponsividad);
    }

    // Añadir estilos para resaltar los descuentos activos
    function añadirEstilosDescuentos() {
        const style = document.createElement('style');
        style.textContent = `
            .precio-volumen-item.active-discount {
                border: 2px solid #1a3c5b;
                transform: scale(1.05);
                background-color: #e8f4f8;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }
            .quantity-limit.active {
                color: #e74c3c;
                font-weight: bold;
                transform: scale(1.05);
                transition: all 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }

    // Ajustar responsividad según el tamaño de la ventana
    function ajustarResponsividad() {
        const productoDetalle = document.querySelector('.producto-detalle');
        if (productoDetalle) {
            if (window.innerWidth <= 768) {
                productoDetalle.style.flexDirection = 'column';
            } else {
                productoDetalle.style.flexDirection = 'row';
            }
        }
    }

    // Crear miniaturas para navegación
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
                if (productosRelacionadosGrid) {
                    cargarProductosRelacionados();
                }
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

        // Actualizar información básica del producto
        if (productoImg) {
            productoImg.src = producto.imagen;
            productoImg.alt = producto.nombre;
        }

        if (productoTitulo) productoTitulo.textContent = producto.nombre;
        if (productoDescripcion) productoDescripcion.textContent = producto.descripcion;
        if (productoDimensiones) productoDimensiones.textContent = producto.dimensiones;

        // Actualizar opciones de tamaño
        if (sizeOptions) {
            cargarOpcionesTamanio(producto.tamanios, producto.tamanioActivo);
        }

        // Resetear cantidad y actualizar límite
        if (qtyInput) {
            qtyInput.value = 1;
            currentQuantity = 1;
            actualizarLimiteQuantidad(producto.maxQuantity);
            validarCantidad();
        }

        // Actualizar precios según tamaño
        actualizarPrecio();
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
                actualizarPrecio();
            });

            sizeOptions.appendChild(sizeBtn);
        });
    }

    // Actualizar precio según el tamaño y la cantidad (FUNCIÓN MODIFICADA)
    function actualizarPrecio() {
        const producto = productos[productoActualIndex];
        if (!producto) return;

        // Determinar el precio base según el tamaño
        let precioBase = producto.precio;
        let preciosVol = producto.preciosVolumen || [];

        // Si tiene precios por tamaño y un tamaño activo
        if (producto.preciosPorTamanio && producto.tamanioActivo) {
            const precioInfo = producto.preciosPorTamanio[producto.tamanioActivo];
            if (precioInfo) {
                precioBase = precioInfo.precio;
                preciosVol = precioInfo.preciosVolumen || [];
            }
        }

        // Ordenar descuentos de menor a mayor cantidad
        preciosVol.sort((a, b) => a.cantidad - b.cantidad);

        // Aplicar el descuento más alto que sea menor o igual a la cantidad
        let precioFinal = precioBase;
        for (const descuento of preciosVol) {
            if (currentQuantity >= descuento.cantidad) {
                precioFinal = descuento.precio;
            } else {
                break; // Los descuentos están ordenados, podemos salir del bucle
            }
        }

        // Actualizar precio en la interfaz
        if (precioPrincipal) {
            precioPrincipal.textContent = precioFinal.toFixed(2);
        }

        // Actualizar precios volumen
        if (preciosVolumen) {
            cargarPreciosVolumen(preciosVol);
            resaltarDescuentoActivo(currentQuantity, preciosVol);
        }
    }

    // Cargar precios por volumen (función modificada para mantener el orden correcto)
    function cargarPreciosVolumen(precios) {
        if (!preciosVolumen) return;

        preciosVolumen.innerHTML = '';

        // Ordenar de menor a mayor cantidad para mostrar en la UI
        const preciosOrdenados = [...precios].sort((a, b) => a.cantidad - b.cantidad);

        preciosOrdenados.forEach(precio => {
            const precioItem = document.createElement('div');
            precioItem.classList.add('precio-volumen-item');

            precioItem.innerHTML = `
            <span class="etiqueta-precio">S/ ${precio.precio.toFixed(2)}</span>
            <span class="etiqueta-cantidad">a partir de ${precio.cantidad} uds.</span>
        `;

            preciosVolumen.appendChild(precioItem);
        });
    }

    // Resaltar el descuento activo según la cantidad (FUNCIÓN MODIFICADA)
    function resaltarDescuentoActivo(cantidad, preciosVol) {
        const discountItems = document.querySelectorAll('.precio-volumen-item');

        // Quitar resaltado de todos los items
        discountItems.forEach(item => {
            item.classList.remove('active-discount');
        });

        // Si no hay descuentos o no hay elementos visuales, salir
        if (!preciosVol.length || !discountItems.length) return;

        // Encontrar el descuento activo más alto
        let descuentoActivoIndex = -1;
        for (let i = 0; i < preciosVol.length; i++) {
            if (cantidad >= preciosVol[i].cantidad) {
                descuentoActivoIndex = i;
            } else {
                break;
            }
        }

        // Resaltar el descuento activo si se encontró
        if (descuentoActivoIndex !== -1) {
            discountItems[descuentoActivoIndex].classList.add('active-discount');
        }
    }

    // Actualizar mensaje de límite de cantidad
    function actualizarLimiteQuantidad(maxQty) {
        if (quantityLimit) {
            quantityLimit.textContent = `Máximo: ${maxQty} unidades`;
        }
    }

    // Mostrar alerta de límite
    function mostrarAlertaLimite() {
        quantityLimit.classList.add('active');
        setTimeout(() => {
            quantityLimit.classList.remove('active');
        }, 1500);
    }

    // Validar la cantidad
    function validarCantidad() {
        if (!qtyInput) return;

        const producto = productos[productoActualIndex];
        if (!producto) return;

        const maxQty = producto.maxQuantity;
        let cantidad = parseInt(qtyInput.value);

        // Validar valor
        if (isNaN(cantidad) || cantidad < 1) {
            cantidad = 1;
        } else if (cantidad > maxQty) {
            cantidad = maxQty;
            mostrarAlertaLimite();
        }

        // Actualizar input y estado
        qtyInput.value = cantidad;
        currentQuantity = cantidad;

        // Actualizar estado de botones
        if (decreaseBtn) decreaseBtn.disabled = cantidad <= 1;
        if (increaseBtn) increaseBtn.disabled = cantidad >= maxQty;

        // Actualizar precio según cantidad
        actualizarPrecio();
    }

    // Inicializar control de cantidad
    function inicializarControlCantidad() {
        if (!qtyInput) return;

        // Eliminar readonly si existe
        qtyInput.removeAttribute('readonly');
        qtyInput.type = 'number';

        // Manejar cambios en el input
        qtyInput.addEventListener('input', validarCantidad);
        qtyInput.addEventListener('blur', validarCantidad);

        // Para evitar valores no numéricos
        qtyInput.addEventListener('keydown', function (e) {
            // Permitir: backspace, delete, tab, escape, enter
            if ([46, 8, 9, 27, 13].indexOf(e.keyCode) !== -1 ||
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
                const producto = productos[productoActualIndex];

                if (parseInt(newValue) > producto.maxQuantity) {
                    e.preventDefault();
                    mostrarAlertaLimite();
                }
            }
        });
    }

    // Cargar productos relacionados
    function cargarProductosRelacionados() {
        if (!productosRelacionadosGrid) return;

        productosRelacionadosGrid.innerHTML = '';

        // Mostrar productos aleatorios diferentes al actual
        const productosDisponibles = [...productos];
        productosDisponibles.splice(productoActualIndex, 1);

        // Mezclar el array para productos aleatorios
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
                if (nuevoIndex !== -1) {
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
                }
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

    // Configurar eventos principales
    function configurarEventos() {
        // Navegación entre productos
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

        // Control de cantidad
        if (decreaseBtn) {
            decreaseBtn.addEventListener('click', () => {
                if (!qtyInput) return;

                let cantidad = parseInt(qtyInput.value);
                if (cantidad > 1) {
                    qtyInput.value = cantidad - 1;
                    validarCantidad();
                }
            });
        }

        if (increaseBtn) {
            increaseBtn.addEventListener('click', () => {
                if (!qtyInput) return;

                let cantidad = parseInt(qtyInput.value);
                qtyInput.value = cantidad + 1;
                validarCantidad();
            });
        }

        // Botón de agregar al carrito
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', () => {
                const producto = productos[productoActualIndex];
                if (!producto) return;

                const cantidad = parseInt(qtyInput.value);
                if (isNaN(cantidad) || cantidad < 1 || cantidad > producto.maxQuantity) {
                    mostrarAlertaLimite();
                    return;
                }

                // Determinar tamaño seleccionado
                let tamanioSeleccionado = '';
                if (producto.tamanios && producto.tamanios.length > 0 && producto.tamanioActivo) {
                    tamanioSeleccionado = producto.tamanioActivo;
                }

                // Determinar precio unitario
                let precioUnitario = producto.precio;
                let preciosVol = producto.preciosVolumen || [];

                if (producto.preciosPorTamanio && producto.tamanioActivo) {
                    const precioInfo = producto.preciosPorTamanio[producto.tamanioActivo];
                    if (precioInfo) {
                        precioUnitario = precioInfo.precio;
                        preciosVol = precioInfo.preciosVolumen || [];
                    }
                }

                // Ordenar descuentos de menor a mayor cantidad
                preciosVol.sort((a, b) => a.cantidad - b.cantidad);

                // Calcular precio con descuento por volumen si aplica
                for (const descuento of preciosVol) {
                    if (cantidad >= descuento.cantidad) {
                        precioUnitario = descuento.precio;
                    } else {
                        break;
                    }
                }

                // Calcular precio total
                const precioTotal = (precioUnitario * cantidad).toFixed(2);

                // Mensaje de confirmación
                alert(`Se han agregado ${cantidad} unidades de ${producto.nombre} ${tamanioSeleccionado ? '- ' + tamanioSeleccionado : ''} al carrito
Precio unitario: S/ ${precioUnitario.toFixed(2)}
Total: S/ ${precioTotal}`);
            });
        }
    }

    // Iniciar la página
    inicializarPagina();
});