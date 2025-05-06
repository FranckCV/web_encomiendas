document.addEventListener('DOMContentLoaded', function() {
    // Datos de productos
    const productos = [
        {
            id: 1,
            nombre: "Caja Shalom",
            descripcion: "Ideal para envíos pequeños y seguros.",
            dimensiones: "15 x 10 x 10 cm",
            precio: 1.50,
            imagen: "/static/img/caja XXS.png",
            preciosVolumen: [
                { precio: 1.20, cantidad: 25 },
                { precio: 1.00, cantidad: 50 }
            ],
            tamanios: ["XXS", "XS", "S", "M", "L"],
            tamanioActivo: "XXS"
        },
        {
            id: 2,
            nombre: "Plumón Indeleble",
            descripcion: "Marcador permanente con punta gruesa redondeada que posee una tinta color negro resistente al agua y la luz.",
            dimensiones: "Multimark Jumbo 23",
            precio: 3.00,
            imagen: "/static/img/plumon.png",
            preciosVolumen: [
                { precio: 2.80, cantidad: 12 },
                { precio: 2.50, cantidad: 24 }
            ],
            tamanios: []
        },
        {
            id: 3,
            nombre: "Sobre A4",
            descripcion: "Ideal para el traslado de tus documentos.",
            dimensiones: "21 x 29.7 cm",
            precio: 1.00,
            imagen: "/static/img/sobre.png",
            preciosVolumen: [
                { precio: 0.90, cantidad: 50 },
                { precio: 0.80, cantidad: 100 }
            ],
            tamanios: []
        },
        {
            id: 4,
            nombre: "Cinta de Embalaje",
            descripcion: "Cinta adhesiva resistente para todo tipo de paquetes.",
            dimensiones: "48mm x 40m",
            precio: 5.90,
            imagen: "/static/img/cintaEmbalaje.png",
            preciosVolumen: [
                { precio: 5.50, cantidad: 6 },
                { precio: 5.00, cantidad: 12 }
            ],
            tamanios: []
        },
        {
            id: 5,
            nombre: "Stretch Film",
            descripcion: "Ideal para embalar y proteger todos tus envíos.",
            dimensiones: "Varios tamaños",
            precio: 12.00,
            imagen: "/static/img/stretchfilm.png",
            preciosVolumen: [
                { precio: 11.00, cantidad: 5 },
                { precio: 10.00, cantidad: 10 }
            ],
            tamanios: ["9''", "15''"]
        },
        {
            id: 6,
            nombre: "Burbupack",
            descripcion: "Lámina de plástico burbuja para proteger objetos frágiles.",
            dimensiones: "1m x 1m",
            precio: 2.50,
            imagen: "/static/img/burbupack.png",
            preciosVolumen: [
                { precio: 2.30, cantidad: 10 },
                { precio: 2.00, cantidad: 20 }
            ],
            tamanios: ["1m x 1m", "1m x 2m", "2m x 2m"]
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
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const thumbsContainer = document.getElementById('thumbs-container');
    const productosRelacionadosGrid = document.getElementById('productos-relacionados-grid');
    
    // Control de cantidad
    const decreaseBtn = document.querySelector('.qty-btn.decrease');
    const increaseBtn = document.querySelector('.qty-btn.increase');
    const qtyInput = document.querySelector('.qty-input');
    
    // Índice del producto actual
    let productoActualIndex = 0;
    
    // Inicializar la página
    function inicializarPagina() {
        // Crear miniaturas de productos
        crearMiniaturas();
        
        // Cargar producto inicial
        cargarProducto(productoActualIndex);
        
        // Cargar productos relacionados
        cargarProductosRelacionados();
        
        // Configurar eventos
        configurarEventos();
    }
    
    // Crear miniaturas de navegación
    function crearMiniaturas() {
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
        
        // Actualizar imagen y textos
        productoImg.src = producto.imagen;
        productoImg.alt = producto.nombre;
        productoTitulo.textContent = producto.nombre;
        productoDescripcion.textContent = producto.descripcion;
        productoDimensiones.textContent = producto.dimensiones;
        precioPrincipal.textContent = producto.precio.toFixed(2);
        
        // Actualizar precios por volumen
        cargarPreciosVolumen(producto.preciosVolumen);
        
        // Actualizar opciones de tamaño
        cargarOpcionesTamanio(producto.tamanios, producto.tamanioActivo);
        
        // Resetear cantidad
        qtyInput.value = 1;
    }
    
    // Cargar precios por volumen
    function cargarPreciosVolumen(precios) {
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
            });
            
            sizeOptions.appendChild(sizeBtn);
        });
    }
    
    // Cargar productos relacionados
    function cargarProductosRelacionados() {
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
                document.querySelector('.producto-detalle').scrollIntoView({
                    behavior: 'smooth'
                });
                
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
        prevBtn.addEventListener('click', () => {
            productoActualIndex = (productoActualIndex - 1 + productos.length) % productos.length;
            cargarProducto(productoActualIndex);
            actualizarMiniaturaActiva();
            cargarProductosRelacionados();
        });
        
        nextBtn.addEventListener('click', () => {
            productoActualIndex = (productoActualIndex + 1) % productos.length;
            cargarProducto(productoActualIndex);
            actualizarMiniaturaActiva();
            cargarProductosRelacionados();
        });
        
        // Botones de cantidad
        decreaseBtn.addEventListener('click', () => {
            let cantidad = parseInt(qtyInput.value);
            if (cantidad > 1) {
                qtyInput.value = cantidad - 1;
            }
        });
        
        increaseBtn.addEventListener('click', () => {
            let cantidad = parseInt(qtyInput.value);
            qtyInput.value = cantidad + 1;
        });
        
        // Botón de agregar al carrito
        document.querySelector('.btn-agregar').addEventListener('click', () => {
            const producto = productos[productoActualIndex];
            const cantidad = parseInt(qtyInput.value);
            let tamanioSeleccionado = '';
            
            if (producto.tamanios.length > 0) {
                tamanioSeleccionado = producto.tamanioActivo;
            }
            
            // Aquí se implementaría la lógica para agregar al carrito
            console.log(`Agregando al carrito: ${cantidad} ${producto.nombre} ${tamanioSeleccionado ? '- ' + tamanioSeleccionado : ''}`);
            
            // Mostrar mensaje de confirmación
            alert(`¡${cantidad} ${producto.nombre} ${tamanioSeleccionado ? '- ' + tamanioSeleccionado : ''} agregado al carrito!`);
        });
    }
    
    // Iniciar la página
    inicializarPagina();
});